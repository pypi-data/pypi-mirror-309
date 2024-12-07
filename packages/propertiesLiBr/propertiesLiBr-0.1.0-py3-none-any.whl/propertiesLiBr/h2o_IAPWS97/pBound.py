# -*- coding: utf-8 -*-

from .Stoffparameter_H2O import nbound


def pBound(temp):
    # boundary pressure between regions 2 and 3
    # pBound in bar
    # temperature in K
    #
    # pBound = -1: temperature outside range
    #
    #

    if temp < 623.15 or temp > 863.15:
        return -1
    else:
        return (nbound[0] + nbound[1] * temp + nbound[2] * temp ** 2) * 10
