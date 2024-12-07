from .pSatW import pSatW
from .entropyreg1 import entropyreg1
from .Stoffparameter_H2O import tc_water
from .entropyreg3 import entropyreg3
from .densreg3 import densreg3


def entropySatLiqTW(temp):
    # entropySatLiqTW=entropySatLiqTW(temp)
    # specific entropy of saturated liquid water as a def of temperature
    #
    # entropySatLiqTW    in kJ/kg
    # temp                in K
    #

    press = pSatW(temp)
    # region 1
    if 273.15 <= temp <= 623.15:
        return entropyreg1(temp, press)

    # region 3
    if 623.15 < temp <= tc_water:
        density = densreg3(temp, press)
        return entropyreg3(temp, density)

    # outside range
    if temp < 273.15 or temp > 623.15:
        return -1
