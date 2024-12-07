# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import nreg2, ireg2, jreg2


def gammarpitaureg2(tau, pic):
    # Jan Albers
    # 15/12/2003

    tau = tau - 0.5
    gamma = 0
    for i in range(len(nreg2)):
        gamma += nreg2[i] * ireg2[i] * pic ** (ireg2[i] - 1) * jreg2[i] * tau ** (jreg2[i] - 1)
    return gamma
