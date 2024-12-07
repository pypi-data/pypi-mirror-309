# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import rgas_water
from .gammataureg1 import gammataureg1
from .gammareg1 import gammareg1


def entropyreg1(temp, press):
    # specific entropy in region 1
    # Spezifische Enthalpie für Wasser im flüssigen Zustand
    # entropyreg1   in kJ/kgK
    # temp          in K
    # press         in bar
    #
    # erstellt von Jan Albers
    # 09.02.2005
    #

    tau = 1386 / temp
    pic = 0.1 * press / 16.53
    return 0.001 * rgas_water * (tau * gammataureg1(tau, pic) - gammareg1(tau, pic))
