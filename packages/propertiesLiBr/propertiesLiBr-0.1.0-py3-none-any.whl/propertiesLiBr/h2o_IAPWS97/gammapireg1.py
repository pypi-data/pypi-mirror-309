# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import nreg1, ireg1, jreg1


def gammapireg1(tau, pic):
    # gammapireg1(tau, pic)
    #
    # tau    reduced temperature     dimensionless
    # pic    reduced pressure        dimensionless
    #
    # IAPWS water properties 1997
    # First derivative of fundamental equation in pi for region 1
    #
    # S.P. Sep. 2002
    tau = tau - 1.222
    pic = 7.1 - pic
    gammareg1 = 0
    for i in range(len(nreg1)):
        gammareg1 += nreg1[i] * ireg1[i] * pic ** (ireg1[i] - 1) * tau ** jreg1[i]
    return gammareg1
