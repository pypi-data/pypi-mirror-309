# -*- coding: utf-8 -*-

from .gamma0taureg2 import gamma0taureg2
from .gammartaureg2 import gammartaureg2
from .Stoffparameter_H2O import rgas_water


def enthalpyreg2(temp, press):
    #
    #  specific enthalpy in region 2
    #  enthalpyreg2 in kJ/kg
    #  temperature in K
    #  pressure in bar

    tau = 540 / temp
    pic = 0.1 * press

    return 0.001 * rgas_water * temp * tau * (gamma0taureg2(tau, pic) + gammartaureg2(tau, pic))
