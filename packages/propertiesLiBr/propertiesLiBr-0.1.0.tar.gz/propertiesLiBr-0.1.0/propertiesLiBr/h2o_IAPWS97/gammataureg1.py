# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import nreg1, ireg1, jreg1


def gammataureg1(tau, pic):
    # gammataureg1(tau, pic)
    #
    # tau    reduced temperature     dimensionless
    # pic    reduced pressure        dimensionless
    #
    # IAPWS water properties 1997

    # Unterfunktion zu den Stoffwerten für Wasser
    # Stefan Petersen 10/10/02

    tau = tau - 1.222
    pic = 7.1 - pic
    gamma = 0
    for i in range(len(nreg1)):
        gamma += nreg1[i] * pic ** ireg1[i] * jreg1[i] * tau ** (jreg1[i] - 1)
    return gamma
