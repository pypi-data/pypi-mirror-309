from .Stoffparameter_H2O import n0reg2, j0reg2
import numpy as np


def gamma0reg2(tau, pic):
    # gamma0reg2(tau, pic)
    #
    # tau    reduced temperature     dimensionless
    # pic    reduced pressure        dimensionless
    #
    # IAPWS water properties 1997
    # First derivative of fundamental equation in pi for region 1
    #
    # Jan Albers 09.02.2005

    gamma = np.log(pic)
    for i in range(9):
        gamma += n0reg2[i] * tau ** j0reg2[i]
    return gamma
