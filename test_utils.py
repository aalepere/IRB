""" Unit tests for all the functions in utils.py """
import numpy as np

import pandas as pd
from utils import get_average_PD, get_maturity_adjusment, get_maturity_slope, get_rho_asset_correlation


class TestAveragePD:
    """
        Tests around calculating average PD
    """

    def test_get_average_PD(self):
        """
            Test that the functions correctly returns average PD.
            In this is example avg_PD = (0.0 + 1.0) / 2 = 0.5
        """
        dict_frame = {"exp": [100, 200], "PD": [0.0, 1.0]}
        df = pd.DataFrame(data=dict_frame)
        avg_PD = get_average_PD(df, col="PD")
        assert avg_PD == 0.5


class TestAssetCorrelation:
    """
        Tests around calculating asset correlation:
        - PD = 0%
        - PD = 100%
        - PD = 1%

        Test that the fco works also when imput is an array
    """

    def test_rho_pd_0(self):
        """
            Test rho calculation when PD = 0%.
            Expected result 24%
        """
        rho = get_rho_asset_correlation(np.array(0.0))
        assert rho == 0.24

    def test_rho_pd_100(self):
        """
            Test rho calculation when PD = 100%
            Expected result 12%
        """
        rho = get_rho_asset_correlation(np.array(1.0))
        assert rho == 0.12

    def test_rho_pd_1(self):
        """
            Test rho calcularion when PD = 1%
            Expected results:
            exponential_weights = (1 - exp(-0.5)) / (1 - exp(-50))
            exponential weights = 0.393469340287367
            rho = 0.12 * exponential_weights + 0.24 * (1 - exponential_weights)
            rho = 0.192783679165516
        """
        exponential_weights = (1 - np.exp(-50 * 0.01)) / (1 - np.exp(-50))
        rho = 0.12 * (exponential_weights) + 0.24 * (1 - exponential_weights)
        rho_calc = get_rho_asset_correlation(np.array(0.01))
        assert rho == rho_calc
        assert rho_calc == 0.192783679165516

    def test_with_array(self):
        """
            Test that when we have an array with the 3 above we get the same results.
        """
        input = np.array([0.0, 1.0, 0.01])
        output = np.array([0.24, 0.12, 0.192783679165516])
        rho_calc = get_rho_asset_correlation(input)
        test = np.testing.assert_array_equal(rho_calc, output)
        assert test is None


class TestMaturity:
    """
        Test the function that computes maturity adjustement:
        - for an exposure
        - for multiple exposures
    """

    def test_slope_one_value(self):
        """
        """
        slope = get_maturity_slope(0.1)
        test_slope = (0.11852 - 0.05478 * np.log(0.1)) ** 2
        slope2 = get_maturity_slope(0.2)
        test_slope2 = (0.11852 - 0.05478 * np.log(0.2)) ** 2
        assert test_slope == slope
        assert test_slope2 == slope2

    def test_slope_multiple_values(self):
        """
        """
        test_slope = (0.11852 - 0.05478 * np.log(0.1)) ** 2
        test_slope2 = (0.11852 - 0.05478 * np.log(0.2)) ** 2
        test_array = np.array([test_slope, test_slope2])
        slope_array = get_maturity_slope(np.array([0.1, 0.2]))
        test = np.testing.assert_array_equal(test_array, slope_array)
        assert test is None

    def test_maturity_adj_one_value(self):
        """
        """
        test_slope = (0.11852 - 0.05478 * np.log(0.1)) ** 2
        test_ma = (1 + (1 - 2.5) * test_slope) / (1 - 1.5 * test_slope)
        ma = get_maturity_adjusment(0.1, 1)
        test_slope2 = (0.11852 - 0.05478 * np.log(0.2)) ** 2
        test_ma2 = (1 + (1 - 2.5) * test_slope2) / (1 - 1.5 * test_slope2)
        ma2 = get_maturity_adjusment(0.2, 1)
        assert test_ma == ma
        assert test_ma2 == ma2

    def test_maturity_adj_multi_value(self):
        """
        """
        test_slope = (0.11852 - 0.05478 * np.log(0.1)) ** 2
        test_ma = (1 + (1 - 2.5) * test_slope) / (1 - 1.5 * test_slope)
        test_slope2 = (0.11852 - 0.05478 * np.log(0.2)) ** 2
        test_ma2 = (1 + (1 - 2.5) * test_slope2) / (1 - 1.5 * test_slope2)
        ma_array = get_maturity_adjusment(pd=np.array([0.1, 0.2]), m=np.array([1, 1]))
        test_array = np.array([test_ma, test_ma2])
        test = np.testing.assert_array_equal(test_array, ma_array)
        assert test is None
