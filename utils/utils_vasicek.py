""" MonteCarlo simulation utils based on Vasicek one-factor Gaussian copula model """
import numpy as np
from scipy.stats import norm, uniform

from utils_irb import get_rho_asset_correlation


def conditional_pd(pd, rho, y):
    """
        DESCRIPTION:
        ------------
        The Vasicek model is a one period default model, i.e., loss only occurs when an 
        obligor defaults in a fixed time horizon. Based on Merton‘s firm-value model, to describe 
        the obligor’s default and its correlation structure, we assign each obligor a random
        variable called firm-value.

        The firm-value of obligor n is represented by a common, standard normally distributed factor
        Y component and an idiosyncratic standard normal noise component n.
        The Y factor is the state of the world or business cycle, usually called systematic factor.

        The probability of default of obligor n conditional to a realization of Y = y is given by
        this function.

        REFERENCE:
        ----------
        https://core.ac.uk/download/pdf/41778167.pdf

        PARAMS:
        -------
        :param pd: probability of default of obligor n
        :param rho: asset correlation, to be computed from IRB approach
        :param y: The Y factor is the state of the world or business cycle, usually called
        systematic factor.
        :return pd_conditional: conditional probability of default of obligor n to a realization of
        Y.
    """

    numerator = np.subtract(norm.ppf(pd), np.multiply(np.sqrt(rho), y))
    denominator = np.sqrt(1 - rho)
    return norm.cdf(np.divide(numerator, denominator))


def run_simulation(pd, ead, lgd, num_simulations=1000):
    """
        DESCRIPTION:
        ------------
        This functions runs a montecarlo simulation using the conditional PD computed through the
        vasicek model.

        1) y is randomly generated from a normal distribution
        2) conditional_pd is computed with the vasicek formula
        3) we generate a uniform continuous random variable
        4) we compare the random variable to conditional_pd to define if default there is
        5) if default compute loss = default_indicator * EAD * LGD
        6) aggregate all losses

        PARAMS:
        -------
        :param pd: probability of default
        :param ead: exposure at risk
        :param lgd: loss given default
        :param num_simulations: number of simulation/iteration to be performed
        :return scenario_losses: array of losses
    """
    scenario_losses = np.array([])
    rho = get_rho_asset_correlation(pd)
    for _ in range(num_simulations):
        y = np.random.normal(size=1)
        pd_cond = conditional_pd(pd, rho, y)
        uniform_random_variable = uniform.rvs(size=pd.size)
        default_indicator = (uniform_random_variable < pd_cond) * 1.0
        loss = np.multiply(default_indicator, ead, lgd)
        total_loss = loss.sum()
        scenario_losses.append(total_loss)
    return scenario_losses
