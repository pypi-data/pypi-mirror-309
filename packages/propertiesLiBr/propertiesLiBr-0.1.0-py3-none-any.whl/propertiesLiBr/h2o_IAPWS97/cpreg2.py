# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import rgas_water
from .gamma0tautaureg2 import gamma0tautaureg2
from .gammartautaureg2 import gammartautaureg2


def cpreg2(temp, press):
    # specific isobaric heat capacity in region 2
    # cpreg2 in kJ/(kg K)
    # temperature in K
    # pressure in bar
    #

    tau = 540 / temp
    pic = 0.1 * press
    return -0.001 * rgas_water * tau ** 2 * (gamma0tautaureg2(tau, pic) + gammartautaureg2(tau, pic))
