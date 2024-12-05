#!/usr/bin/env python
docustring = """
This program produces tables of Rrup-to-Repi and Rjb-to-Repi
ratios and variances for a single event. This means that the magnitdue and
hypocentral depth are available, simplifying the integration. It optionally
tabulates the adjustment factors as a function of backazimuth. An example
configuration file for this program is given in
``tests/config/test_single.ini`` `here <https://github.com/usgs/ps2ff/blob/master/tests/config/test_single.ini>`_.


The configuration parameters are:

- **M** -- The earthquake magnitude.

- **zhyp** -- The hypocentral depth of the earthquake.

- **bytheta** -- Tabulate factors for bins of theta (bool; default=False).

- **NP** -- The number of processors (cores) to use. Minimum 1.

- **datadir** --- The directory into which the output files are written. If
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

- **min_seis_depth** - The minimum seismogenic depth (km).

- **max_seis_depth** - The maximum seismogenic depth (km).

- **mindip_deg** - The minimum rupture dip in degrees (0 min, 90 max).

- **maxdip_deg** - The maximum rupture dip in degrees (0 min 90 max).

- **ndip** - The number of integration steps in dip.

- **ntheta** - The number of integration steps in theta.

- **nxny** - The number of integration steps in x and y (minimum is 2).

- **trunc** - For the integration in area (or length and width), this is the
  truncation of the normal distribution (in standard deviation units).

- **neps** - The number of integration steps for area (or length and width)
  from --trunc to +trunc. Larger numbers increase the accuracy of the result,
  but take longer to run.

- **minepi** - The minimum epicentral distance for which to compute results.

- **maxepi** - The maximum epicentral distance for which to compute results.

- **nepi** - The number of steps from minepi to max epi. The steps will be
   uniformly sized in log space.

"""

import sys
import os
import os.path
import datetime
import time as time
import numpy as np
import argparse
from configobj import ConfigObj

from ps2ff.integration_loops import single_event_loop
from ps2ff.config import (
    get_configspec,
    get_custom_validator,
    check_config,
    config_error,
)


def get_parser():
    if __name__ == "__main__":
        description = """
Produces tables of Rrup-to-Repi and Rjb-to-Repi
ratios and variances for a single event. This means that the magnitdue and
hypocentral depth are available, simplifying the integration. It optionally
tabulates the adjustment factors as a function of backazimuth. An example
configuration file for this program is given in
`tests/config/test_single.ini`.
        """
    else:
        description = docustring

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("config_file", help="The configuration file.")
    return parser


class App:
    @staticmethod
    def main(config_file):

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

        if "datadir" in config:
            datadir = config["datadir"]
        else:
            datadir = "data"

        if os.path.isdir(datadir) is False:
            os.makedirs(datadir, exist_ok=True)

        theta_string = ""
        if config["bytheta"] is True:
            theta_string = "_bytheta"

        rjb_filename = os.path.join(datadir, "Rjb%s" % (theta_string))
        rrup_filename = os.path.join(datadir, "Rrup%s" % (theta_string))

        config["mindip"] = config["mindip_deg"] * np.pi / 180.0
        config["maxdip"] = config["maxdip_deg"] * np.pi / 180.0
        Repi = np.logspace(
            np.log10(config["minepi"]), np.log10(config["maxepi"]), config["nepi"]
        )

        for iP in range(0, config["NP"]):
            if os.fork() == 0:
                single_event_loop(
                    config,
                    iP=iP,
                    rjb_filename=rjb_filename,
                    rrup_filename=rrup_filename,
                    M=config["M"],
                    Repi=Repi,
                )

        for iP in range(0, config["NP"]):
            pid, status = os.waitpid(-1, 0)

        fd = [None] * 4
        fd[0] = open("%s_Ratios.csv" % (rjb_filename), "w")
        fd[1] = open("%s_Var.csv" % (rjb_filename), "w")
        fd[2] = open("%s_Ratios.csv" % (rrup_filename), "w")
        fd[3] = open("%s_Var.csv" % (rrup_filename), "w")

        for i in range(0, 4):
            fd[i].write("# Program: %s\n" % sys.argv[0])
            fd[i].write("# Config file: %s\n" % config_file)
            fd[i].write("# Process start: %s\n" % start_datetime)
            fd[i].write("# Process finish: %s\n" % datetime.datetime.now().isoformat())
            fd[i].write(
                "# M = %f, zhyp = %f, bytheta = %s, rup_dim_model = %s, "
                "mech = %s, AR = %s, ndip = %d, mindip = %f, maxdip = %f\n"
                % (
                    config["M"],
                    config["zhyp"],
                    config["bytheta"],
                    config["rup_dim_model"],
                    config["mech"],
                    config["AR"],
                    config["ndip"],
                    config["mindip"],
                    config["maxdip"],
                )
            )
            fd[i].write(
                "# ntheta = %d, nxny = %d, neps = %d, trunc = %f, "
                "min_seis_depth = %f, max_seis_depth = %f\n"
                % (
                    config["ntheta"],
                    config["nxny"],
                    config["neps"],
                    config["trunc"],
                    config["min_seis_depth"],
                    config["max_seis_depth"],
                )
            )
            fd[i].write('"Repi_km",')

        if config["bytheta"] is True:
            theta = np.linspace(0, 2 * np.pi, config["ntheta"])
            for i in range(0, 4):
                for j in range(0, config["ntheta"]):
                    fd[i].write('"%g"' % (theta[j]))
                    if j < config["ntheta"] - 1:
                        fd[i].write(",")
                fd[i].write("\n")
        else:
            fd[0].write('"R%g"\n' % config["M"])
            fd[1].write('"V%g"\n' % config["M"])
            fd[2].write('"R%g"\n' % config["M"])
            fd[3].write('"V%g"\n' % config["M"])

        rjb_rat_file = [None] * config["NP"]
        rjb_var_file = [None] * config["NP"]
        rrup_rat_file = [None] * config["NP"]
        rrup_var_file = [None] * config["NP"]
        rjb_frs = [None] * config["NP"]
        rjb_fvs = [None] * config["NP"]
        rrup_frs = [None] * config["NP"]
        rrup_fvs = [None] * config["NP"]
        for iP in range(0, config["NP"]):
            rjb_rat_file[iP] = "%sRatios_%02d.csv" % (rjb_filename, iP)
            rjb_var_file[iP] = "%sVar_%02d.csv" % (rjb_filename, iP)
            rrup_rat_file[iP] = "%sRatios_%02d.csv" % (rrup_filename, iP)
            rrup_var_file[iP] = "%sVar_%02d.csv" % (rrup_filename, iP)
            rjb_frs[iP] = open(rjb_rat_file[iP], "r")
            rjb_fvs[iP] = open(rjb_var_file[iP], "r")
            rrup_frs[iP] = open(rrup_rat_file[iP], "r")
            rrup_fvs[iP] = open(rrup_var_file[iP], "r")

        for line in rjb_frs[0]:
            fd[0].write(line)
            line = rjb_fvs[0].readline()
            fd[1].write(line)
            line = rrup_frs[0].readline()
            fd[2].write(line)
            line = rrup_fvs[0].readline()
            fd[3].write(line)
            for iP in range(1, config["NP"]):
                line = rjb_frs[iP].readline()
                if line:
                    fd[0].write(line)
                line = rjb_fvs[iP].readline()
                if line:
                    fd[1].write(line)
                line = rrup_frs[iP].readline()
                if line:
                    fd[2].write(line)
                line = rrup_fvs[iP].readline()
                if line:
                    fd[3].write(line)

        for iP in range(0, config["NP"]):
            rjb_frs[iP].close()
            rjb_fvs[iP].close()
            rrup_frs[iP].close()
            rrup_fvs[iP].close()
            os.unlink(rjb_rat_file[iP])
            os.unlink(rjb_var_file[iP])
            os.unlink(rrup_rat_file[iP])
            os.unlink(rrup_var_file[iP])

        for i in range(0, 4):
            fd[i].close()


def cli():
    parser = get_parser()
    pargs = parser.parse_args()
    app = App()
    app.main(pargs.config_file)


if __name__ == "__main__":
    cli()
    sys.exit(0)
