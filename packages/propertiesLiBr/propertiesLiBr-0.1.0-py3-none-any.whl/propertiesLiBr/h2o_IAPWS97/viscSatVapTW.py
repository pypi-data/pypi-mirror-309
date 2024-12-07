from .densSatVapTW import densSatVapTW
from .psivisc import psivisc


def viscSatVapTW(temp, press):
    # viscW=viscW(temp, press)
    #
    # viscSatVapTW    dynamic viscosity of saturated steam (eta) in Pa s = kg/(s-m)
    # temp            temperature in K
    #
    # viscSatVapTW = -1: temperature and/or pressure outside range
    #
    if 273.15 <= temp <= 623.15:  # region 2
        density = densSatVapTW(temp)
        delta = density / 317.763
        tau = 647.226 / temp
        return 0.000055071 * psivisc(tau, delta)
    else:
        #  outside range
        return -1
