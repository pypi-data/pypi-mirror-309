# -*- coding: utf-8 -*-


from .Stoffparameter_H2O import nreg2, ireg2, jreg2


def gammarpireg2(tau, pic):
    # gammarpireg2(tau, pic)
    #
    # tau    reduced temperature     dimensionless
    # pic    reduced pressure        dimensionless
    #
    # IAPWS water properties 1997
    # First derivative of fundamental equation in pi for region 1
    #
    # J.A. Feb. 2003

    tau = tau - 0.5
    gamma = 0
    for i in range(len(nreg2)):
        gamma += nreg2[i] * ireg2[i] * (pic ** (ireg2[i] - 1)) * tau ** jreg2[i]
    return gamma
