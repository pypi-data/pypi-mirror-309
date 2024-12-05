import pandas as pd
import shutil
from ps2ff.cmd import get_command_output


def test_rrup_Sea10_slab():
    conf = "fast_Sea10_slab.ini"
    cmd = "run_ps2ff -w rrup tests/config/%s" % conf
    rc, so, se = get_command_output(cmd)
    r1 = pd.read_csv(
        "tests/TestData/fast_test/Sea10_slab/Rrup_Sea10_slab_mechA_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v1 = pd.read_csv(
        "tests/TestData/fast_test/Sea10_slab/Rrup_Sea10_slab_mechA_ar1p0_seis0_15_Var.csv",
        header=6,
    )
    r2 = pd.read_csv(
        "TestData/fast_test/Sea10_slab/Rrup_Sea10_slab_mechA_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v2 = pd.read_csv(
        "TestData/fast_test/Sea10_slab/Rrup_Sea10_slab_mechA_ar1p0_seis0_15_Var.csv",
        header=6,
    )

    pd.testing.assert_frame_equal(r1, r2)
    pd.testing.assert_frame_equal(v1, v2)

    # Clean up
    shutil.rmtree("TestData")


def test_rrup_Sea10_interface():
    conf = "fast_Sea10_interface.ini"
    cmd = "run_ps2ff -w rrup tests/config/%s" % conf
    rc, so, se = get_command_output(cmd)
    r1 = pd.read_csv(
        "tests/TestData/fast_test/Sea10_interface/Rrup_Sea10_interface_mechA_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v1 = pd.read_csv(
        "tests/TestData/fast_test/Sea10_interface/Rrup_Sea10_interface_mechA_ar1p0_seis0_15_Var.csv",
        header=6,
    )
    r2 = pd.read_csv(
        "TestData/fast_test/Sea10_interface/Rrup_Sea10_interface_mechA_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v2 = pd.read_csv(
        "TestData/fast_test/Sea10_interface/Rrup_Sea10_interface_mechA_ar1p0_seis0_15_Var.csv",
        header=6,
    )

    pd.testing.assert_frame_equal(r1, r2)
    pd.testing.assert_frame_equal(v1, v2)

    # Clean up
    shutil.rmtree("TestData")


def test_rrup_HB08():
    conf = "fast_HB08.ini"
    cmd = "run_ps2ff -w rrup tests/config/%s" % conf
    rc, so, se = get_command_output(cmd)
    r1 = pd.read_csv(
        "tests/TestData/fast_test/HB08/Rrup_HB08_mechA_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v1 = pd.read_csv(
        "tests/TestData/fast_test/HB08/Rrup_HB08_mechA_ar1p0_seis0_15_Var.csv", header=6
    )
    r2 = pd.read_csv(
        "TestData/fast_test/HB08/Rrup_HB08_mechA_ar1p0_seis0_15_Ratios.csv", header=6
    )
    v2 = pd.read_csv(
        "TestData/fast_test/HB08/Rrup_HB08_mechA_ar1p0_seis0_15_Var.csv", header=6
    )

    pd.testing.assert_frame_equal(r1, r2)
    pd.testing.assert_frame_equal(v1, v2)

    # Clean up
    shutil.rmtree("TestData")


def test_rrup_WC94_SS_F():
    conf = "fast_WC94_SS_F.ini"
    cmd = "run_ps2ff -w rrup tests/config/%s" % conf
    rc, so, se = get_command_output(cmd)
    r1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_SS_F/Rrup_WC94_mechSS_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_SS_F/Rrup_WC94_mechSS_ar1p0_seis0_15_Var.csv",
        header=6,
    )
    r2 = pd.read_csv(
        "TestData/fast_test/WC94_SS_F/Rrup_WC94_mechSS_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v2 = pd.read_csv(
        "TestData/fast_test/WC94_SS_F/Rrup_WC94_mechSS_ar1p0_seis0_15_Var.csv", header=6
    )

    pd.testing.assert_frame_equal(r1, r2)
    pd.testing.assert_frame_equal(v1, v2)

    # Clean up
    shutil.rmtree("TestData")


def test_rjb_WC94_SS_F():
    conf = "fast_WC94_SS_F.ini"
    cmd = "run_ps2ff -w rjb tests/config/%s" % conf
    rc, so, se = get_command_output(cmd)
    r1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_SS_F/Rjb_WC94_mechSS_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_SS_F/Rjb_WC94_mechSS_ar1p0_seis0_15_Var.csv",
        header=6,
    )
    r2 = pd.read_csv(
        "TestData/fast_test/WC94_SS_F/Rjb_WC94_mechSS_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v2 = pd.read_csv(
        "TestData/fast_test/WC94_SS_F/Rjb_WC94_mechSS_ar1p0_seis0_15_Var.csv", header=6
    )

    pd.testing.assert_frame_equal(r1, r2)
    pd.testing.assert_frame_equal(v1, v2)

    # Clean up
    shutil.rmtree("TestData")


def test_rrup_WC94_SS_T():
    conf = "fast_WC94_SS_T.ini"
    cmd = "run_ps2ff -w rrup tests/config/%s" % conf
    rc, so, se = get_command_output(cmd)
    r1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_SS_T/Rrup_WC94_mechSS_LW_seis0_15_Ratios.csv",
        header=6,
    )
    v1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_SS_T/Rrup_WC94_mechSS_LW_seis0_15_Var.csv",
        header=6,
    )
    r2 = pd.read_csv(
        "TestData/fast_test/WC94_SS_T/Rrup_WC94_mechSS_LW_seis0_15_Ratios.csv", header=6
    )
    v2 = pd.read_csv(
        "TestData/fast_test/WC94_SS_T/Rrup_WC94_mechSS_LW_seis0_15_Var.csv", header=6
    )

    pd.testing.assert_frame_equal(r1, r2)
    pd.testing.assert_frame_equal(v1, v2)

    # Clean up
    shutil.rmtree("TestData")


def test_rjb_WC94_SS_T():
    conf = "fast_WC94_SS_T.ini"
    cmd = "run_ps2ff -w rjb tests/config/%s" % conf
    rc, so, se = get_command_output(cmd)
    r1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_SS_T/Rjb_WC94_mechSS_LW_seis0_15_Ratios.csv",
        header=6,
    )
    v1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_SS_T/Rjb_WC94_mechSS_LW_seis0_15_Var.csv",
        header=6,
    )
    r2 = pd.read_csv(
        "TestData/fast_test/WC94_SS_T/Rjb_WC94_mechSS_LW_seis0_15_Ratios.csv", header=6
    )
    v2 = pd.read_csv(
        "TestData/fast_test/WC94_SS_T/Rjb_WC94_mechSS_LW_seis0_15_Var.csv", header=6
    )

    pd.testing.assert_frame_equal(r1, r2)
    pd.testing.assert_frame_equal(v1, v2)

    # Clean up
    shutil.rmtree("TestData")


def test_rrup_WC94_R_T():
    conf = "fast_WC94_R_T.ini"
    cmd = "run_ps2ff -w rrup tests/config/%s" % conf
    rc, so, se = get_command_output(cmd)
    r1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_R_T/Rrup_WC94_mechR_LW_seis0_15_Ratios.csv",
        header=6,
    )
    v1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_R_T/Rrup_WC94_mechR_LW_seis0_15_Var.csv",
        header=6,
    )
    r2 = pd.read_csv(
        "TestData/fast_test/WC94_R_T/Rrup_WC94_mechR_LW_seis0_15_Ratios.csv", header=6
    )
    v2 = pd.read_csv(
        "TestData/fast_test/WC94_R_T/Rrup_WC94_mechR_LW_seis0_15_Var.csv", header=6
    )

    pd.testing.assert_frame_equal(r1, r2)
    pd.testing.assert_frame_equal(v1, v2)

    # Clean up
    shutil.rmtree("TestData")


def test_rjb_WC94_R_T():
    conf = "fast_WC94_R_T.ini"
    cmd = "run_ps2ff -w rjb tests/config/%s" % conf
    rc, so, se = get_command_output(cmd)
    r1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_R_T/Rjb_WC94_mechR_LW_seis0_15_Ratios.csv",
        header=6,
    )
    v1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_R_T/Rjb_WC94_mechR_LW_seis0_15_Var.csv",
        header=6,
    )
    r2 = pd.read_csv(
        "TestData/fast_test/WC94_R_T/Rjb_WC94_mechR_LW_seis0_15_Ratios.csv", header=6
    )
    v2 = pd.read_csv(
        "TestData/fast_test/WC94_R_T/Rjb_WC94_mechR_LW_seis0_15_Var.csv", header=6
    )

    pd.testing.assert_frame_equal(r1, r2)
    pd.testing.assert_frame_equal(v1, v2)

    # Clean up
    shutil.rmtree("TestData")


def test_rrup_WC94_R_F():
    conf = "fast_WC94_R_F.ini"
    cmd = "run_ps2ff -w rrup tests/config/%s" % conf
    rc, so, se = get_command_output(cmd)
    r1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_R_F/Rrup_WC94_mechR_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_R_F/Rrup_WC94_mechR_ar1p0_seis0_15_Var.csv",
        header=6,
    )
    r2 = pd.read_csv(
        "TestData/fast_test/WC94_R_F/Rrup_WC94_mechR_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v2 = pd.read_csv(
        "TestData/fast_test/WC94_R_F/Rrup_WC94_mechR_ar1p0_seis0_15_Var.csv", header=6
    )

    pd.testing.assert_frame_equal(r1, r2)
    pd.testing.assert_frame_equal(v1, v2)

    # Clean up
    shutil.rmtree("TestData")


def test_rjb_WC94_R_F():
    conf = "fast_WC94_R_F.ini"
    cmd = "run_ps2ff -w rjb tests/config/%s" % conf
    rc, so, se = get_command_output(cmd)
    r1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_R_F/Rjb_WC94_mechR_ar1p0_seis0_15_Ratios.csv",
        header=6,
    )
    v1 = pd.read_csv(
        "tests/TestData/fast_test/WC94_R_F/Rjb_WC94_mechR_ar1p0_seis0_15_Var.csv",
        header=6,
    )
    r2 = pd.read_csv(
        "TestData/fast_test/WC94_R_F/Rjb_WC94_mechR_ar1p0_seis0_15_Ratios.csv", header=6
    )
    v2 = pd.read_csv(
        "TestData/fast_test/WC94_R_F/Rjb_WC94_mechR_ar1p0_seis0_15_Var.csv", header=6
    )

    pd.testing.assert_frame_equal(r1, r2)
    pd.testing.assert_frame_equal(v1, v2)

    # Clean up
    shutil.rmtree("TestData")
