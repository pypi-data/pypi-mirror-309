from .densW import densW
from .psivisc import psivisc


def viscW(temp, press):
    # viscW=viscW(temp, press)
    #
    # viscW    dynamic viscosity of water or steam (eta) in Pa s
    # temp     temperature in K
    # press    pressure in bar
    #
    # viscW = -1: temperature and/or pressure outside range
    #
    if 273.15 <= temp <= 1073.15 and 0 < press <= 1000:
        density = densW(temp, press)
        delta = density / 317.763
        tau = 647.226 / temp
        return 0.000055071 * psivisc(tau, delta)
    else:
        #  outside range
        return -1
