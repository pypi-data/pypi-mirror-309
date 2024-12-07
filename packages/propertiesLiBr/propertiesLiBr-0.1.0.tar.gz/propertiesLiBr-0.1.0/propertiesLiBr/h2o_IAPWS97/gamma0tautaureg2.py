from .Stoffparameter_H2O import j0reg2, n0reg2


def gamma0tautaureg2(tau, pic):
    # 15/12/2003

    gammareg1 = 0
    for i in range(len(n0reg2)):
        gammareg1 += n0reg2[i] * j0reg2[i] * (j0reg2[i] - 1) * tau ** (j0reg2[i] - 2)
    return gammareg1
