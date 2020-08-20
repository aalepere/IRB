""" Class IRB Model """

import numpy as np


class IRBModel:
    """
        XXXX
    """

    def __init__(self, exp_list):
        """
            XXXX
        """
        self.exp_list = exp_list

    def get_average_PD(self):
        """
            XXX
        """
        self.average_PD = np.mean(self.exp_list["PD"])

    def get_rho_asset_correlation(
        self, k_factor=-50, rho_low=0.12, rho_high=0.24
    ):
        """
            REF: https://www.bis.org/bcbs/irbriskweight.pdf
        """
        exponential_weights = (1 - np.exp(k_factor * self.average_PD)) / (
            1 - np.exp(k_factor)
        )
        self.rho = rho_low * exponential_weights + rho_high * (
            1 - exponential_weights
        )

    def get_smooth_maturity_adj(a=0.11852, b=-0.05478):
        """
            XXXX
        """

        self.smooth_maturity_adj = (a + b * np.log(self.average_PD)) ^ 2
