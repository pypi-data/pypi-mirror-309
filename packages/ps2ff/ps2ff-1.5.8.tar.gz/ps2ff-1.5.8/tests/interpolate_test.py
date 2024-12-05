#!/usr/bin/env python

# stdlib imports
import os.path
import sys
import numpy as np
import pytest
import importlib.resources

from ps2ff.constants import DistType, MagScaling, Mechanism
from ps2ff.interpolate import PS2FF

homedir = os.path.dirname(os.path.abspath(__file__))  # where is this script?
shakedir = os.path.abspath(os.path.join(homedir, "..", ".."))
sys.path.insert(0, shakedir)


def test_interpolate():

    p2f = PS2FF.fromParams(
        dist_type=DistType.Rjb,
        mag_scaling=MagScaling.HB08,
        mechanism=Mechanism.SS,
        AR=1.7,
        min_seis_depth=0,
        max_seis_depth=20,
    )
    repi = np.logspace(-1, 3, 20)
    mags = np.full_like(repi, 6.8)

    rrup = p2f.r2r(repi, mags)
    #    print(repr(rrup))

    rrup_test = np.array(
        [
            1.22075000e-02,
            2.07138668e-02,
            3.60665169e-02,
            6.50678328e-02,
            1.23306770e-01,
            2.47816822e-01,
            5.22124828e-01,
            1.09623305e00,
            2.21513765e00,
            4.23411465e00,
            7.74294257e00,
            1.38913234e01,
            2.48691256e01,
            4.42042870e01,
            7.70915466e01,
            1.31640910e02,
            2.20949016e02,
            3.66402928e02,
            6.02849289e02,
            9.86939600e02,
        ]
    )

    assert np.allclose(rrup, rrup_test)

    variance = p2f.var(repi, mags)
    #    print(repr(variance))

    variance_test = np.array(
        [
            7.97600000e-04,
            2.16995770e-03,
            5.96208721e-03,
            1.65978167e-02,
            4.67916345e-02,
            1.32523279e-01,
            3.67092965e-01,
            9.71121058e-01,
            2.39523815e00,
            5.74419775e00,
            1.37536376e01,
            3.09969430e01,
            5.88516850e01,
            9.10504010e01,
            1.18993353e02,
            1.36292747e02,
            1.45063689e02,
            1.49579770e02,
            1.52095682e02,
            1.53568280e02,
        ]
    )

    assert np.allclose(variance, variance_test)

    rats = p2f.rat(repi, mags)
    #    print(repr(rats))

    rats_test = np.array(
        [
            0.122075,
            0.12756598,
            0.13678913,
            0.15198033,
            0.17737061,
            0.21953269,
            0.28485015,
            0.36831438,
            0.45834257,
            0.53954264,
            0.60763514,
            0.67135797,
            0.74019258,
            0.81025605,
            0.87023859,
            0.91515813,
            0.94595618,
            0.96607661,
            0.97889265,
            0.9869396,
        ]
    )

    assert np.allclose(rats, rats_test)

    tables = PS2FF.getValidFiles()
    datadir = importlib.resources.files("ps2ff") / "tables"
    for table in tables:
        assert (datadir / table).is_file()

    rfile, vfile = p2f.files()

    #
    # Test the fromFile method with a bad file name to exercise
    # its error handling
    #
    badrfile = rfile.replace("20", "5176")
    with pytest.raises(ValueError):
        p2f = PS2FF.fromFile(badrfile)

    #
    # Put in a bad max_seis_depth to exercise the error handling
    #
    with pytest.raises(ValueError):
        p2f = PS2FF.fromParams(
            dist_type=DistType.Rrup,
            mag_scaling=MagScaling.HB08,
            mechanism=Mechanism.SS,
            AR=1.0,
            min_seis_depth=0,
            max_seis_depth=5172,
        )


if __name__ == "__main__":
    test_interpolate()
