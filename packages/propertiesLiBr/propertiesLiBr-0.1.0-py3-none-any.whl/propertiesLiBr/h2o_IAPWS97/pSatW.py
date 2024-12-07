# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import nreg4


def pSatW(temp):
    # diese Funktion berechnet den Gleichgewichtsdruck von H2O
    # in bar
    # mit der Temperatur in K
    #
    # erstellt von Stefan Petersen, Berlin 08/02
    # entsprechend dem MS-Excel AddIn
    # gültig von 273 K bis 647 K
    # erstellt von Stefan Petersen
    # 08/10/02

    Del = temp + nreg4[8] / (temp - nreg4[9])
    Aco = Del ** 2 + nreg4[0] * Del + nreg4[1]
    Bco = nreg4[2] * Del ** 2 + nreg4[3] * Del + nreg4[4]
    Cco = nreg4[5] * Del ** 2 + nreg4[6] * Del + nreg4[7]
    return (2 * Cco / (-Bco + (Bco ** 2 - 4 * Aco * Cco) ** 0.5)) ** 4 * 10
