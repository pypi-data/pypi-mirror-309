# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import rgas_water
from .gammarpireg2 import gammarpireg2
from .gammarpipireg2 import gammarpipireg2
from .gammarpitaureg2 import gammarpitaureg2
from .gamma0tautaureg2 import gamma0tautaureg2
from .gammartautaureg2 import gammartautaureg2


def spsoundreg2(temp, press):
    # speed of sound in region 2
    # spsoundreg2 in m/s
    # temperature in K
    # pressure in bar
    #

    tau = 540 / temp
    pic = 0.1 * press
    gamma_1 = gammarpireg2(tau, pic)
    return (rgas_water * temp * (1 + 2 * pic * gamma_1 + pic ** 2 * gamma_1 ** 2) / (
                (1 - pic ** 2 * gammarpipireg2(tau, pic)) + (
                    1 + pic * gamma_1 - tau * pic * gammarpitaureg2(tau, pic)) ** 2 / (
                            tau ** 2 * (gamma0tautaureg2(tau, pic) + gammartautaureg2(tau, pic))))) ** 0.5
