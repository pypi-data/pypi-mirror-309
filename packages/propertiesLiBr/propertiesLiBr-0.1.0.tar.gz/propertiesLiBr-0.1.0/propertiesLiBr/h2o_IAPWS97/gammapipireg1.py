from .Stoffparameter_H2O import nreg1, ireg1, jreg1


def gammapipireg1(tau, pic):
    # gammapipireg1(tau, pic)
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
    gammareg1 = 0
    for i in range(len(nreg1)):
        gammareg1 += nreg1[i] * ireg1[i] * (ireg1[i] - 1) * pic ** (ireg1[i] - 2) * tau ** jreg1[i]
    return gammareg1
