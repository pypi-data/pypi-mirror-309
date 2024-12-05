import pandas as pd
import shutil
from ps2ff.cmd import get_command_output


def test_single():
    cmd = "run_ps2ff_single_event tests/config/test_single.ini"
    rc, so, se = get_command_output(cmd)

    rjb1 = pd.read_csv(
        "tests/TestData/single_test/test_single/Rjb_bytheta_Ratios.csv", header=6
    )
    vjb1 = pd.read_csv(
        "tests/TestData/single_test/test_single/Rjb_bytheta_Var.csv", header=6
    )
    rjb2 = pd.read_csv(
        "TestData/single_test/test_single/Rjb_bytheta_Ratios.csv", header=6
    )
    vjb2 = pd.read_csv("TestData/single_test/test_single/Rjb_bytheta_Var.csv", header=6)

    rrup1 = pd.read_csv(
        "tests/TestData/single_test/test_single/Rrup_bytheta_Ratios.csv", header=6
    )
    vrup1 = pd.read_csv(
        "tests/TestData/single_test/test_single/Rrup_bytheta_Var.csv", header=6
    )
    rrup2 = pd.read_csv(
        "TestData/single_test/test_single/Rrup_bytheta_Ratios.csv", header=6
    )
    vrup2 = pd.read_csv(
        "TestData/single_test/test_single/Rrup_bytheta_Var.csv", header=6
    )

    # pd.testing.assert_frame_equal(rjb1, rjb2)
    pd.testing.assert_frame_equal(vjb1, vjb2)
    pd.testing.assert_frame_equal(rrup1, rrup2)
    pd.testing.assert_frame_equal(vrup1, vrup2)

    # Clean up
    shutil.rmtree("TestData")


def test_single_by_theta_false():
    cmd = "run_ps2ff_single_event tests/config/test_single_by_theta_false.ini"
    rc, so, se = get_command_output(cmd)

    rjb1 = pd.read_csv(
        "tests/TestData/single_test/test_single_by_theta_false/Rjb_Ratios.csv",
        header=6,
    )
    vjb1 = pd.read_csv(
        "tests/TestData/single_test/test_single_by_theta_false/Rjb_Var.csv",
        header=6,
    )
    rjb2 = pd.read_csv(
        "TestData/single_test/test_single_by_theta_false/Rjb_Ratios.csv",
        header=6,
    )
    vjb2 = pd.read_csv(
        "TestData/single_test/test_single_by_theta_false/Rjb_Var.csv",
        header=6,
    )

    rrup1 = pd.read_csv(
        "tests/TestData/single_test/test_single_by_theta_false/Rrup_Ratios.csv",
        header=6,
    )
    vrup1 = pd.read_csv(
        "tests/TestData/single_test/test_single_by_theta_false/Rrup_Var.csv",
        header=6,
    )
    rrup2 = pd.read_csv(
        "TestData/single_test/test_single_by_theta_false/Rrup_Ratios.csv",
        header=6,
    )
    vrup2 = pd.read_csv(
        "TestData/single_test/test_single_by_theta_false/Rrup_Var.csv",
        header=6,
    )

    pd.testing.assert_frame_equal(rjb1, rjb2)
    pd.testing.assert_frame_equal(vjb1, vjb2)
    pd.testing.assert_frame_equal(rrup1, rrup2)
    pd.testing.assert_frame_equal(vrup1, vrup2)

    # Clean up
    shutil.rmtree("TestData")


def test_single_N1():
    cmd = "run_ps2ff_single_event tests/config/test_single_N1.ini"
    rc, so, se = get_command_output(cmd)

    rjb1 = pd.read_csv(
        "tests/TestData/single_test/test_single_N1/Rjb_bytheta_Ratios.csv", header=6
    )
    vjb1 = pd.read_csv(
        "tests/TestData/single_test/test_single_N1/Rjb_bytheta_Var.csv", header=6
    )
    rjb2 = pd.read_csv(
        "TestData/single_test/test_single_N1/Rjb_bytheta_Ratios.csv", header=6
    )
    vjb2 = pd.read_csv(
        "TestData/single_test/test_single_N1/Rjb_bytheta_Var.csv", header=6
    )

    rrup1 = pd.read_csv(
        "tests/TestData/single_test/test_single_N1/Rrup_bytheta_Ratios.csv", header=6
    )
    vrup1 = pd.read_csv(
        "tests/TestData/single_test/test_single_N1/Rrup_bytheta_Var.csv", header=6
    )
    rrup2 = pd.read_csv(
        "TestData/single_test/test_single_N1/Rrup_bytheta_Ratios.csv", header=6
    )
    vrup2 = pd.read_csv(
        "TestData/single_test/test_single_N1/Rrup_bytheta_Var.csv", header=6
    )

    pd.testing.assert_frame_equal(rjb1, rjb2)
    pd.testing.assert_frame_equal(vjb1, vjb2)
    pd.testing.assert_frame_equal(rrup1, rrup2)
    pd.testing.assert_frame_equal(vrup1, vrup2)

    # Clean up
    shutil.rmtree("TestData")


if __name__ == "__main__":
    test_single()
    test_single_by_theta_false()
    test_single_N1()
