from .Stoffparameter_H2O import rgas_water
from .gamma0pireg2 import gamma0pireg2
from .gammarpireg2 import gammarpireg2


def volreg2(temp, press):
    # volreg2(temp, press)
    #
    # volreg2      specific volume in region 2  m**3/kg
    # temp         temperature                  K
    # press        pressure                     bar
    #
    # J.A. Feb. 2003

    tau = 540.0 / temp
    pic = 0.1 * press / 1

    return rgas_water * temp * pic * (gamma0pireg2(tau, pic) + gammarpireg2(tau, pic)) / (press * 100000)
