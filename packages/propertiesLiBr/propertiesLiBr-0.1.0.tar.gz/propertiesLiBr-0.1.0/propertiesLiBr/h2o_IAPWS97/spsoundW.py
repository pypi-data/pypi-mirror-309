# -*- coding: utf-8 -*-

from .spsoundreg1 import spsoundreg1
from .spsoundreg2 import spsoundreg2
from .pSatW import pSatW


def spsoundW(temp, press):
    # spsoundW(temp, press)
    #
    # spsoundW     speed of sound in water or steam                        m/s
    # temp         temperature                                             K
    # press        pressure                                                bar
    #
    # J.A. Nov. 2006

    # region 1
    if 273.15 <= temp <= 623.15 and pSatW(temp) <= press <= 1000:
        return spsoundreg1(temp, press)

    # region 2
    if 273.15 <= temp <= 623.15 and 0 < press <= pSatW(temp):
        return spsoundreg2(temp, press)

    # region 3 or out of boundaries
    if temp >= 623.15 or press < 0 or press > 1000:
        return -1

    return -2
