from .Stoffparameter_H2O import tc_water
from .pSatW import pSatW
from .volreg2 import volreg2


def densSatVapTW(temp):
    # densSatVapTW(temp)
    # Density of saturated liquid water as a def of temperature
    #
    # densSatVapTW  density of water in region 1  kg/m**3
    # temp          temperature                   K
    #
    # J.A. Feb. 2005

    # region 2
    press = pSatW(temp)
    if 273.15 <= temp <= 623.15:
        return 1 / volreg2(temp, press)

    # region 3 or out of boundaries
    if temp > 623.15 and temp > tc_water:
        return -1
    return -2
