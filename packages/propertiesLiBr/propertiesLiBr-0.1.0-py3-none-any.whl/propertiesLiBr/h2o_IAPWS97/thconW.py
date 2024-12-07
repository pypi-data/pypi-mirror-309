from .densW import densW
from .lambthcon import lambthcon


def thconW(temp, press):
    # thconW=thconW(temp, press)
    #
    # thconW    thermal conductivity of water or steam   in W/(m K)
    # temp      temperature in K
    # press     pressure in bar
    #
    # thconW = -1: temperature and/or pressure outside range
    #

    if 273.15 <= temp <= 1073.15 and 0 < press <= 1000:
        density = densW(temp, press)
        delta = density / 317.763
        tau = 647.226 / temp
        return 0.4945 * lambthcon(temp, press, tau, delta)
    else:
        return -1
