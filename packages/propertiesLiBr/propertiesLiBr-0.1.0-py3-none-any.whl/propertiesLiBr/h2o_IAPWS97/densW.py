import numpy as np
from .volreg1 import volreg1
from .pSatW import pSatW
from .volreg2 import volreg2


def densW(temp, press):
    # densW(temp, press)
    #
    # densW        density of water in region 1  kg/m**3
    # temp         temperature                   K
    # press        pressure                      bar
    #
    # J.A. Nov. 2003
    # 01.02.2012 Fehler beim 'Rest' gefunden. Anstelle des richtige and (und) stand hier ein or (oder)
    #            Neben dieser Korrektur wurde der Fall mit NaN-Aufruf abgefangen

    if temp is None or np.isnan(temp):
        return -3

    # region 1
    if 273.15 <= temp <= 623.15 and pSatW(temp) <= press <= 1000:
        return 1.0 / volreg1(temp, press)

    # region 2
    if 273.15 <= temp <= 623.15 and 0 < press <= pSatW(temp):
        return 1.0 / volreg2(temp, press)

    # region 3 or out of boundaries
    if temp >= 623.15 or press < 0 or press > 1000:
        return -1

    return -2
