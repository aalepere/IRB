""" Set of functions that will support any calc for the IRB approach """
import numpy as np


def get_average_PD(df, col="PD"):
    """
        DESCRIPTION:
        ------------
        This function computes the average PD from all the exposures.

        The implementation of the ASRF model developed for Basel II makes use of average PDs
        that reflect expected default rates under normal business conditions.

        REF: https://www.bis.org/bcbs/irbriskweight.pdf

        PARAMS:
        -------
        :param df: dataframe containing the exposures
        :param col: name of the column containing the PD
        :return: average PD in the dataframe
    """
    return np.mean(df[col])


def get_rho_asset_correlation(pd, k_factor=-50, rho_min=0.12, rho_max=0.24):
    """
        DESCRIPTION:
        -----------
        The single systematic risk factor needed in the ASRF model may be interpreted as reflecting
        the state of the global economy. The degree of the obligor’s exposure to the systematic risk
        factor is expressed by the asset correlation. The asset correlations, in short, show how the
        asset value (e.g. sum of all asset values of a firm) of one borrower depends on the asset
        value of another borrower.

        The asset correlation function is built of two limit correlations of 12% and 24% for very
        high and very low PDs (100% and 0%, respectively). Correlations between these limits are
        modelled by an exponential weighting function that displays the dependency on PD. The
        exponential function decreases rather fast; its pace is determined by the so-called
        “k-factor”, which is set at 50 for corporate exposures.

        PARAMS:
        -------
        :param k_factor: Set to 50 for corporates exposures
        :param rho_min: 12% min limit, for PDs = 100%
        :param rho_max: 14% max limit, for PDs = 0%
        :return rho: assets correlation
    """
    exponential_weights = (1 - np.exp(k_factor * pd)) / (1 - np.exp(k_factor))
    return rho_min * exponential_weights + rho_max * (1 - exponential_weights)
