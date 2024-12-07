# -*- coding: utf-8 -*-

from .gammataureg1 import gammataureg1
from .Stoffparameter_H2O import rgas_water


def enthalpyreg1(temp, press):
    # specific enthalpy in region 1
    # Spezifische Enthalpie für Wasser im flüssigen Zustand
    # enthalpyreg1  in kJ/kg
    # temp          in K
    # press         in bar
    #
    # erstellt von Stefan Petersn
    # 10/10/02
    #

    tau = 1386 / temp
    pic = 0.1 * press / 16.53

    return 0.001 * rgas_water * temp * tau * gammataureg1(tau, pic)
