#!/usr/bin/env python

import os.path
import pytest

homedir = os.path.dirname(os.path.abspath(__file__))
shakedir = os.path.abspath(os.path.join(homedir, "..", ".."))

from validate import ValidateError

import ps2ff.config as config
from ps2ff.constants import MagScaling, Mechanism


def test_config():

    #
    # Break the config
    #
    ctest = {}
    ctest["min_seis_depth"] = 10.0
    ctest["max_seis_depth"] = 5.0
    with pytest.raises(ValidateError):
        config.check_config(ctest)
    ctest["max_seis_depth"] = 20.0

    ctest["mindip_deg"] = 10.0
    ctest["maxdip_deg"] = 5.0
    with pytest.raises(ValidateError):
        config.check_config(ctest)

    ctest["maxdip_deg"] = 10.0
    ctest["ndip"] = 5
    with pytest.raises(ValidateError):
        config.check_config(ctest)
    ctest["ndip"] = 1

    ctest["minmag"] = 10.0
    ctest["maxmag"] = 5.0
    with pytest.raises(ValidateError):
        config.check_config(ctest)
    ctest["maxmag"] = 15.0

    ctest["minepi"] = 10.0
    ctest["maxepi"] = 5.0
    with pytest.raises(ValidateError):
        config.check_config(ctest)

    ctest["maxepi"] = 10.0
    ctest["nepi"] = 5.0
    with pytest.raises(ValidateError):
        config.check_config(ctest)

    ctest["nepi"] = 1.0

    config.check_config(ctest)

    #
    # magScalingType()
    #
    with pytest.raises(ValidateError):
        res = config.magScalingType(["1", "2"])
    with pytest.raises(ValidateError):
        res = config.magScalingType("NotAThing")
    res = config.magScalingType("WC94")
    assert res is MagScaling.WC94

    #
    # mechType()
    #
    with pytest.raises(ValidateError):
        res = config.mechType(["1", "2"])
    with pytest.raises(ValidateError):
        res = config.mechType("NotAThing")
    res = config.mechType("R")
    assert res is Mechanism.R


if __name__ == "__main__":
    test_config()
