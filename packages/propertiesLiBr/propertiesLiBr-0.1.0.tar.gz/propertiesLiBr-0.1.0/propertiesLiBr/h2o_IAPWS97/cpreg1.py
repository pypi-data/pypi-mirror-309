# -*- coding: utf-8 -*-

from .gammatautaureg1 import gammatautaureg1
from .Stoffparameter_H2O import rgas_water


def cpreg1(temp, press):
    # specific isobaric heat capacity in region 1
    # cpreg1 in kJ/(kg K)
    # temperature in K
    # pressure in bar
    #

    tau = 1386 / temp
    pic = 0.1 * press / 16.53
    return -0.001 * rgas_water * tau ** 2 * gammatautaureg1(tau, pic)
