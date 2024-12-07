# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import n0thcon, nthcon, rgas_water
import numpy as np
from .gammapitaureg1 import gammapitaureg1
from .gammapireg1 import gammapireg1
from .gammapipireg1 import gammapipireg1
from .gamma0pitaureg2 import gamma0pitaureg2
from .gammarpitaureg2 import gammarpitaureg2
from .gamma0pireg2 import gamma0pireg2
from .pBound import pBound
from .gammarpireg2 import gammarpireg2
from .pSatW import pSatW
from .gamma0pipireg2 import gamma0pipireg2
from .gammarpipireg2 import gammarpipireg2
from .psivisc import psivisc


def lambthcon(temp, press, tau, delta):
    #
    # Reduced thermal conductivity
    #

    lamb0 = 0
    lamb1 = 0
    # for MATLAB index from 1 to 4 instead of 0 to 3
    for k in range(len(n0thcon)):
        lamb0 += n0thcon(k) * tau ** (k - 1)
    lamb0 = 1 / (tau ** 0.5 * lamb0)
    # for MATLAB index from 1 to 5 instead of 0 to 4
    for k in range(len(nthcon)):
        # for MATLAB index from 1 to 6 instead of 0 to 5
        for m in range(len(nthcon[k])):
            lamb1 += nthcon[k][m] * (tau - 1) ** k * (delta - 1) ** m
    lamb1 = np.exp(delta * lamb1)

    dpidtau = 0
    ddeltadpi = 0

    if 273.15 <= temp <= 623.15 and pSatW(temp) <= press <= 1000:
        taus = 1386 / temp
        pis = press / 165.3
        dpidtau = (647.226 * 165.3 * (gammapitaureg1(taus, pis) * 1386 - gammapireg1(taus, pis) * temp)) / (
                221.15 * temp ** 2 * gammapipireg1(taus, pis))
        ddeltadpi = -(22115000 * gammapipireg1(taus, pis)) / (317.763 * rgas_water * temp * gammapireg1(taus, pis) ** 2)

    #  region 2 Dampf unterkritisch

    if (273.15 <= temp <= 623.15 and 0 <= press <= pSatW(temp)) \
            or (623.15 <= temp <= 863.15 and 0 < press <= pBound(temp)) \
            or (863.15 <= temp <= 1073.15 and 0 < press <= 1000):
        taus = 540 / temp
        pis = press / 10
        dpidtau = (647.226 * 10 * ((gamma0pitaureg2(taus, pis) + gammarpitaureg2(taus, pis)) * 540 - (
                gamma0pireg2(taus, pis) + gammarpireg2(taus, pis)) * temp)) / (
                          221.15 * temp ** 2 * (gamma0pipireg2(taus, pis) + gammarpipireg2(taus, pis)))
        ddeltadpi = -(22115000 * (gamma0pipireg2(taus, pis) + gammarpipireg2(taus, pis))) / (
                317.763 * rgas_water * temp * (gamma0pireg2(taus, pis) + gammarpireg2(taus, pis)) ** 2)

    lamb2 = 0.0013848 / psivisc(tau, delta) * (tau * delta) ** (-2) * dpidtau ** 2 * (
            delta * ddeltadpi) ** 0.4678 * delta ** 0.5 * np.exp(-18.66 * (1 / tau - 1) ** 2 - (delta - 1) ** 4)

    return lamb0 * lamb1 + lamb2
