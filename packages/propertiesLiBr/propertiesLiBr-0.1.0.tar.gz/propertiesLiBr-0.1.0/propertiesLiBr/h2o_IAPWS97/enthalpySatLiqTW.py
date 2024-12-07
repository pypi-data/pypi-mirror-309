from .enthalpyreg1 import enthalpyreg1
from .pSatW import pSatW


def enthalpySatLiqTW(temp):
    # enthalpySatLiqTW=enthalpySatLiqTW(temp)
    # specific enthalpy of saturated liquid water as a def of temperature
    #
    # enthalpySatLiqTW    in kJ/kg
    # temp                in K
    #

    press = pSatW(temp)
    # region 1
    if 273.15 <= temp <= 623.15:
        return enthalpyreg1(temp, press)

    # region X

    # outside range
    return -1

