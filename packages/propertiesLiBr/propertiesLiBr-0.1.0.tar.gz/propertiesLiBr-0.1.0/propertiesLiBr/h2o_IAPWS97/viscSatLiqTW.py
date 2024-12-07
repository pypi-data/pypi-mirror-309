from .psivisc import psivisc
from .densSatLiqTW import densSatLiqTW


def viscSatLiqTW(temp):
    # viscSatLiqTW=viscSatLiqTW(temp)
    #
    # viscSatLiqTW        dynamic viscosity of saturated water (eta) in Pa s = kg/(s-m)
    # temp                temperature in K
    #
    # viscSatLiqTW = -1:  temperature and/or pressure outside range
    #

    # region 1
    if 273.15 <= temp <= 623.15:
        density = densSatLiqTW(temp)
        delta = density / 317.763
        tau = 647.226 / temp
        return 0.000055071 * psivisc(tau, delta)
    else:
        return -1
