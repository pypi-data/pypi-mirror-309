from .Stoffparameter_H2O import n0reg2, j0reg2


def gamma0taureg2(tau, pic):
    # First derivative in tau of ideal-gas part of fundamental equation for region 2
    # Stefan Petersen
    # 10/10/02

    gammareg1 = 0
    for i in range(len(n0reg2)):
        gammareg1 += n0reg2[i] * j0reg2[i] * tau ** (j0reg2[i] - 1)
    return gammareg1
