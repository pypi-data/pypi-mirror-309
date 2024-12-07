# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import rgas_water
from .gammapireg1 import gammapireg1
from .gammapitaureg1 import gammapitaureg1
from .gammatautaureg1 import gammatautaureg1
from .gammapipireg1 import gammapipireg1


def spsoundreg1(temp, press):
    # speed of sound in region 1
    # spsoundreg1 in m/s
    # temperature in K
    # pressure in bar
    #

    tau = 1386 / temp
    pic = 0.1 * press / 16.53
    gamma_1 = gammapireg1(tau, pic)
    return (rgas_water * temp * (gamma_1 ** 2 / ((gamma_1 - tau * gammapitaureg1(tau, pic)) ** 2 / (
                tau ** 2 * gammatautaureg1(tau, pic)) - gammapipireg1(tau, pic)))) ** 0.5
