# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import nreg4


def tSatW(press):
    # tSatW=tSatW(press)
    # Diese Funktion ermittelt die Gleichgewichtstemperatur von gesättigten Wasser
    #
    # tsatW = Sättigungstemperatur    in K
    # press = Druck                   in bar
    #
    # erstellt von Stefan Petersen
    # 08/10/02
    # ehemalige Gültigkeitsgrenzen 6,11213mbar bis 220 bar, neu 5 mbar bis 220 mbar

    if press >= 0.005 or press <= 220.64:
        bet = (0.1 * press) ** 0.25
        eco = bet ** 2 + nreg4[2] * bet + nreg4[5]
        fco = nreg4[0] * bet ** 2 + nreg4[3] * bet + nreg4[6]
        gco = nreg4[1] * bet ** 2 + nreg4[4] * bet + nreg4[7]
        dco = 2 * gco / (-fco - (fco ** 2 - 4 * eco * gco) ** 0.5)
        return 0.5 * (nreg4[9] + dco - ((nreg4[9] + dco) ** 2 - 4 * (nreg4[8] + nreg4[9] * dco)) ** 0.5)
    else:
        return -1
