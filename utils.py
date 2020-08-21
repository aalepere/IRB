""" Set of functions that will support any calc for the IRB approach """
import numpy as np
from scipy.stats import norm


def get_average_PD(df, col="PD"):
    """
        DESCRIPTION:
        ------------
        This function computes the average PD from all the exposures.

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

        REFERENCE:
        ----------
        https://www.bis.org/bcbs/irbriskweight.pdf
        5.2. Supervisory estimates of asset correlations for corporate, bank and sovereign exposures

        PARAMS:
        -------
        :param pd: average PD from portfolio
        :param k_factor: Set to 50 for corporates exposures
        :param rho_min: 12% min limit, for PDs = 100%
        :param rho_max: 14% max limit, for PDs = 0%
        :return rho: assets correlation
    """
    exponential_weights = np.divide((1 - np.exp(k_factor * pd)), (1 - np.exp(k_factor)))
    return rho_min * exponential_weights + rho_max * (1 - exponential_weights)


def get_maturity_slope(pd, a=0.11852, b=-0.05478):
    """
        DESCRIPTION:
        ------------
        Credit portfolios consist of instruments with different maturities. Both intuition and
        empirical evidence indicate that long-term credits are riskier than short-term credits. As a
        consequence, the capital requirement should increase with maturity.

        In order to derive the Basel maturity adjustment function, the grid of relative VaR figures
        (in relation to 2.5 years maturity) was smoothed by a statistical regression model.
        This includes the slope of the adjustment function with respect to M decreases as
        the PD increases.

        REFERENCE:
        ----------
        https://www.bis.org/bcbs/irbriskweight.pdf
        4.6. Maturity adjustments

        PARAMS:
        -------
        :param pd: pd associated to the exposure [0, 1]
        :param a: slope adjustment coefficient 1
        :param b: slope adjustement coefficient 2
        :return maturity_slope: Smoothed (regression) maturity adjustment (smoothed over PDs)
    """
    return np.power((a + b * np.log(pd)), 2)


def get_maturity_adjusment(pd, m, y=2.5):
    """
        DESCRIPTION:
        ------------
        Maturity adjustments are the ratios of each of these VaR figures to the VaR
        of a “standard” maturity, which was set at 2.5 years, for each maturity and each rating grade.

        REFERENCE:
        ----------
        https://www.bis.org/bcbs/irbriskweight.pdf
        4.6. Maturity adjustments

        PARAMS:
        -------
        :params pd:
        :params tenor:
        :params y:
        :return maturity_adj:
    """
    slope = get_maturity_slope(pd)
    return np.divide(1 + (m - y) * slope, 1 - (y - 1) * slope)


def get_basel_K(pd, m, lgd, alpha):
    """
        DESCRIPTION:
        ------------
        Capital requirement (K) = 
        [LGD * N [(1 - R)^-0.5 * G (PD) + (R / (1 - R))^0.5 * G (0.999)] - PD * LGD] 
        * (1 - 1.5 x b(PD))^ -1 × (1 + (M - 2.5) * b (PD)

        Standard normal distribution(N) applied to threshold and conservative value of systematic
        factor.
        Inverse of the standard normal distribution (G, ppf) applied to PD to derive default threshold.
        Inverse of the standard normal distribution (G, ppf) applied to confidence level to derive
        conservative value of systematic factor

        REFERENCE:
        ----------
        4.2. Average and conditional PDs

        PARAMS:
        -------
    """
    rho = get_rho_asset_correlation(pd)
    ma = get_maturity_adjusment(pd, m)
    term_1 = np.add(((1 - rho) ^ (-0.5)), norm.ppf(pd))
    term_2 = np.multiply((((rho) / (1 - rho)) ^ 0.5), norm.ppf(alpha))
    term_3 = norm.cdf(np.add(term_1, term_2))
    return (lgd * term_3 - pd * lgd) * ma
