import numpy as np
from .cpreg1 import cpreg1
from .cpreg2 import cpreg2
from .pSatW import pSatW


def cpW(temp, press):
    # cpW(temp, press)
    #
    # cpW          specific isobaric heat capacity of water or steam       kJ/kg-K
    # temp         temperature                                             K
    # press        pressure                                                bar
    #
    # J.A. Dec. 2003
    # 01.02.2012 Fehler beim 'Rest' gefunden. Anstelle des richtige and (und) stand hier ein or (oder)
    #            Neben dieser Korrektur wurde der Fall mit NaN-Aufruf abgefangen

    if temp is None or np.isnan(temp):
        return -3

    # region 1
    if temp >= 273.15 and temp <= 623.15 and press >= pSatW(temp) and press <= 1000:
        return cpreg1(temp, press)

    # region 2
    if temp >= 273.15 and temp <= 623.15 and press > 0 and press <= pSatW(temp):
        return cpreg2(temp, press)

    # region 3 or out of boundaries
    if temp >= 623.15 or press < 0 or press > 1000:
        return -1

    # Rest
    # k4=find(temp<273.15 and press < pSatW(temp))
    return -2
