# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import nvisc, ivisc, jvisc, n0visc
import numpy as np


def psivisc(tau, delta):
    #
    # Reduced dynamic viscosity
    #

    psi0 = 0
    psi1 = 0
    for k in range(len(n0visc)):
        psi0 = psi0 + n0visc[k] * tau ** k

    psi0 = 1 / (tau ** 0.5 * psi0)
    for k in range(len(nvisc)):
        psi1 = psi1 + nvisc[k] * (delta - 1) ** ivisc[k] * (tau - 1) ** jvisc[k]

    psi1 = np.exp(delta * psi1)
    return psi0 * psi1
