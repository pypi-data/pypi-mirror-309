from .volreg2 import volreg2


def densS(temp, press):
    # densS(temp, press)
    #
    # densS        density of Steam in region 2  kg/m**3
    # temp         temperature                   K
    # press        pressure                      bar
    #
    # J.A. Feb. 2003

    return 1 / volreg2(temp, press)
