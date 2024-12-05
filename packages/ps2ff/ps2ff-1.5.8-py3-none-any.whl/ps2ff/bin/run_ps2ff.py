#!/usr/bin/env python
docustring = """
This program produces tables of Rjb-to-Repi or Rrup-to-Repi ratios and
variances. Example configuration files are given in the
``ps2ff/config/`` `directory <https://github.com/usgs/ps2ff/tree/master/ps2ff/config>`_.

The parameters in the config file are:

- **NP** -- The number of processors (cores) to use. Minimum 1.

- **datadir** -- The directory into which the output files are written. If
  unspecified, it uses ``./data``.

- **rup_dim_model** -- String to select the magnitude scaling relationship.
    Currently supported values are:

  - WC94 -- Wells, D. L., & Coppersmith, K. J. (1994). New empirical
    relationships among magnitude, rupture length, rupture width, rupture area,
    and surface displacement, *Bulletin of the Seismological Society of
    America*, 84(4), 974--1002.
  - S14 -- Somerville, P. (2014). Scaling Relations between Seismic Moment and
    Rupture Area of Earthquakes in Stable Continental Regions, *PEER Report*
    2014/14.
  - HB08 -- Hanks, T. C. and Bakun, W. H. (2008). M-logA observations for
    recent large earthquakes, *Bulletin of the Seismological Society of
    America*, 98(1), 490--494.
  - Sea10_interface -- Interface coefficients of Strasser, F. O., Arango,
    M. C., & Bommer, J. J. (2010). Scaling of the source dimensions of
    interface and intraslab subduction-zone earthquakes with moment magnitude,
    *Seismological Research Letters*, 81(6), 941--950.
  - Sea10_slab: Slab coefficients from the paper in previous bullet.

- **mech** -- The rupture mechanism, only used by some scaling relationships:

  - A -- all/unknown mechanisms,
  - SS -- strike-slip,
  - N -- normal,
  - R -- reverse.

- **LW** -- Boolean for whether to separately select rupture length and width
  distributions, otherwise select the rupture area and compute length and
  width from it and an assumed aspect ratio.

- **AR** -- Aspect ratio (Length/Width) of the rupture. The aspect ratio is
  maintained until the rupture width spans the seismogenic zone, after
  which only the rupture length will increase.

- **min_seis_depth** -- The minimum seismogenic depth (km).

- **max_seis_depth** -- The maximum seismogenic depth (km).

- **mindip_deg** -- The minimum rupture dip in degrees (0 min, 90 max).

- **maxdip_deg** -- The maximum rupture dip in degrees (0 min 90 max).

- **ndip** -- The number of integration steps in dip.

- **ntheta** -- The number of integration steps in theta.

- **nxny** -- The number of integration steps in x and y (minimum is 2).

- **trunc** -- For the integration in area (or length and width), this is the
  truncation of the normal distribution (in standard deviation units).

- **neps** -- The number of integration steps for area (or length and width)
  from --trunc to +trunc. Larger numbers increase the accuracy of the result,
  but take longer to run.

- **minmag** -- The minimum magnitude for which to compute results.

- **maxmag** -- The maximum magnitude for which to compute results.

- **dmag** -- The size of the steps from minmag to maxmag.

- **minepi** -- The minimum epicentral distance for which to compute results.

- **maxepi** -- The maximum epicentral distance for which to compute results.

- **nepi** -- The number of steps from minepi to max epi. The steps will be
   uniformly sized in log space.

- **nz** -- The number of integration steps in depth for Ztor. For any given
  rupture width and dip in the integration, Ztor ranges from
  ``(max_seis_depth - width * sin(dip))`` to ``min_seis_depth``. Only used for
  for Rrup calculations.

"""

import sys
import os
import os.path
import datetime
import copy
import time as time
import argparse

from configobj import ConfigObj

import numpy as np

from ps2ff.integration_loops import mag_dist_loop
from ps2ff.config import (
    get_configspec,
    get_custom_validator,
    check_config,
    config_error,
)
from ps2ff.constants import DistType


def get_parser():
    if __name__ == "__main__":
        description = """
        Produces tables of Rjb-to-Repi or Rrup-to-Repi ratios and
        variances.
        """
    else:
        description = docustring

    parser = argparse.ArgumentParser(
        description=description,
        add_help=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser._optionals.title = "named arguments"
    parser.add_argument("config_file", help="The configuration file.")
    parser.add_argument(
        "-w",
        "--what",
        choices=["rjb", "rrup"],
        required=True,
        help="(required) select the distance measure to calculate",
    )
    return parser


class App:

    @staticmethod
    def main(what, config_file):

        start_datetime = datetime.datetime.now().isoformat()

        if not os.path.exists(config_file):
            raise Exception("Config file %s doesn't exist" % (config_file))

        spec_file = get_configspec()
        validator = get_custom_validator()
        config = ConfigObj(str(config_file), configspec=str(spec_file))

        results = config.validate(validator)
        if not isinstance(results, bool) or not results:
            config_error(config, results)

        check_config(config)

        if what == "rjb":
            config["what"] = DistType.Rjb
        elif what == "rrup":
            config["what"] = DistType.Rrup
        else:
            print("Unknown parameter to -w: This can't happen!")
            sys.exit(1)

        filebase = copy.copy(config["what"].value)
        if "datadir" in config:
            datadir = config["datadir"]
        else:
            datadir = "data"

        if os.path.isdir(datadir) is False:
            os.makedirs(datadir, exist_ok=True)

        if config["LW"] is True:
            filename = "%s_%s_mech%s_LW_seis%g_%g" % (
                filebase,
                config["rup_dim_model"].value,
                config["mech"].value,
                config["min_seis_depth"],
                config["max_seis_depth"],
            )
        else:
            filename = "%s_%s_mech%s_ar%.1f_seis%g_%g" % (
                filebase,
                config["rup_dim_model"].value,
                config["mech"].value,
                config["AR"],
                config["min_seis_depth"],
                config["max_seis_depth"],
            )

        filename = filename.replace(".", "p")
        filename = os.path.join(datadir, filename)

        config["mindip"] = config["mindip_deg"] * np.pi / 180.0
        config["maxdip"] = config["maxdip_deg"] * np.pi / 180.0
        M = np.arange(config["minmag"], config["maxmag"] + 0.001, config["dmag"])
        Repi = np.logspace(
            np.log10(config["minepi"]), np.log10(config["maxepi"]), config["nepi"]
        )
        #
        # This is where the work happens. Fork off NP subprocesses to
        # do the integration on subsets of the Repi range
        #
        for iP in range(config["NP"]):
            if os.fork() == 0:
                mag_dist_loop(config, iP=iP, filename=filename, M=M, Repi=Repi)

        #
        # Wait for all of the subprocesses to finish
        #
        for iP in range(config["NP"]):
            pid, status = os.waitpid(-1, 0)

        #
        # First assemble the ratios file from the sub-files, then do
        # the variances
        #
        nmag = np.size(M)
        for sym, fname in (("R", "Ratios"), ("V", "Var")):
            f = open("%s_%s.csv" % (filename, fname), "w")
            f.write("# Program: %s\n" % sys.argv[0])
            f.write("# Config file: %s\n" % config_file)
            f.write("# Process start: %s\n" % start_datetime)
            f.write("# Process finish: %s\n" % datetime.datetime.now().isoformat())
            f.write(
                "# rup_dim_model = %s, mech = %s, LW = %s, AR = %s, "
                "ndip = %d, mindip = %f, maxdip = %f, ntheta = %d, "
                "nxny = %d\n"
                % (
                    config["rup_dim_model"].value,
                    config["mech"].value,
                    config["LW"],
                    config["AR"],
                    config["ndip"],
                    config["mindip"],
                    config["maxdip"],
                    config["ntheta"],
                    config["nxny"],
                )
            )
            f.write(
                "# neps = %d, trunc = %f, min_seis_depth = %f, "
                "max_seis_depth = %f\n"
                % (
                    config["neps"],
                    config["trunc"],
                    config["min_seis_depth"],
                    config["max_seis_depth"],
                )
            )
            f.write('"Repi_km",')

            for j in range(nmag):
                f.write('"%s%g"' % (sym, M[j]))
                if j < nmag - 1:
                    f.write(",")
            f.write("\n")

            sub_file = [None] * config["NP"]
            fs = [None] * config["NP"]
            for iP in range(config["NP"]):
                sub_file[iP] = "%s%s_%02d.csv" % (filename, fname, iP)
                fs[iP] = open(sub_file[iP], "r")

            for line in fs[0]:
                f.write(line)
                for iP in range(1, config["NP"]):
                    line = fs[iP].readline()
                    if line:
                        f.write(line)

            for iP in range(config["NP"]):
                fs[iP].close()
                os.unlink(sub_file[iP])
            f.close()


def cli():

    parser = get_parser()
    pargs = parser.parse_args()

    app = App()
    app.main(pargs.what, pargs.config_file)


if __name__ == "__main__":
    cli()
    sys.exit(0)
