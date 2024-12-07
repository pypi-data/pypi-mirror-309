# -*- coding: utf-8 -*-

from .pSatW import pSatW
from .volreg1 import volreg1


def densSatLiqTW(temp):
    # densSatLiqTW(temp)
    # Density of saturated liquid water as a def of temperature
    #
    # densSatLiqTW  density of water in region 1  kg/m**3
    # temp          temperature                   K
    #
    # J.A. Feb. 2005  erstellt
    # J.A. Mar. 2005 logical index ergänzt für Interationen, ggf.ist jetzt auch Vertauschung überflüssig

    # Wenn temp keine Spaltenvektor ist, temporär umwendeln (am Ende zurück)

    # region 1
    press = pSatW(temp)

    if 273.15 <= temp <= 623.15 and pSatW(temp) <= press <= 1000:
        return 1 / volreg1(temp, press)
    elif 273.15 <= temp <= 623.15:
        return 1 / volreg1(temp, press)
    # return 1  /  densreg3(temp, press) ?
    elif temp >= 623.15 or press < 0 or press > 1000:
        return -1
    else:
        return -2
