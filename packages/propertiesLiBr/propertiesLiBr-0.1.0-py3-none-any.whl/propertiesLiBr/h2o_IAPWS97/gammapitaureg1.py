from .Stoffparameter_H2O import nreg1, ireg1, jreg1


def gammapitaureg1(tau, pic):
    # gammapireg1(tau, pic)
    #
    # tau    reduced temperature     dimensionless
    # pic    reduced pressure        dimensionless
    #
    # IAPWS water properties 1997
    #
    #
    # J.A. Nov. 2003
    tau = tau - 1.222
    pic = 7.1 - pic
    gamma = 0
    for i in range(len(nreg1)):
        gamma += nreg1[i] * ireg1[i] * pic ** (ireg1[i] - 1) * jreg1[i] * tau ** (jreg1[i] - 1)
    return gamma
