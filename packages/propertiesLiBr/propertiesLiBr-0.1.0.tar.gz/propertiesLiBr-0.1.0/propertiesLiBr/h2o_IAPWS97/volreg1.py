from .Stoffparameter_H2O import rgas_water
from .gammapireg1 import gammapireg1


def volreg1(temp, press):
    # volreg1(temp, press)
    #
    # volreg1      specific volume in region 1  m**3/kg
    # temp         temperature                  K
    # press        pressure                     bar
    #
    # S.P. Sep. 2002

    tau = 1386.0 / temp
    pic = 0.1 * press / 16.53
    return rgas_water * temp * pic * gammapireg1(tau, pic) / (press * 100000)
