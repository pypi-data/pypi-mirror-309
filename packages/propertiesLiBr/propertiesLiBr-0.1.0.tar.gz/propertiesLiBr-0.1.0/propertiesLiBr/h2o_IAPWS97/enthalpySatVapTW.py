from .pSatW import pSatW
from .enthalpyreg2 import enthalpyreg2


def enthalpySatVapTW(temp):
    #  enthalpySatVapTW=enthalpySatVapTW(temp)
    #
    #  specific enthalpy of saturated steam as a def of temperature
    #
    #  enthalpySatVapTW   in kJ/kg
    #  temp               in K

    press = pSatW(temp)
    # region 2
    if 273.15 <= temp <= 623.15:
        return enthalpyreg2(temp, press)

    return -1

