from .pSatW import pSatW
from .entropyreg2 import entropyreg2
from .densreg3 import densreg3
from .entropyreg3 import entropyreg3

def entropySatVapTW(temp):
    #  entropySatVapTW=entropySatVapTW(temp)
    #
    #  specific entropy of saturated steam as a def of temperature
    #
    #  entropySatVapTW   in kJ/kg
    #  temp               in K

    press = pSatW(temp)
    # region 2
    if 273.15 <= temp <= 623.15:
        return entropyreg2(temp, press)

    # region 3
    if 623.15 < temp <= 647.096:
        density = densreg3(temp, press)
        return entropyreg3(temp, density)

    # outside range
    return -1
# tbad=find(temp<273.15 or temp>623.15)
# entropySatVapTW(tbad,1) = -1
