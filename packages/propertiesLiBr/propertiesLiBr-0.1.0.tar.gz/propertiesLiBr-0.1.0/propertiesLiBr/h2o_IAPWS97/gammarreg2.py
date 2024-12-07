# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import nreg2, ireg2, jreg2


def gammarreg2(tau, pic):
    # Jan Albers
    # 09.02.2005

    gamma = 0
    for i in range(len(nreg2)):
        gamma += nreg2[i] * pic ** ireg2[i] * (tau - 0.5) ** jreg2[i]
    return gamma
