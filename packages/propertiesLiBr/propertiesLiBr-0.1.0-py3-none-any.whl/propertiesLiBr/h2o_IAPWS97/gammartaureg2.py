# -*- coding: utf-8 -*-


from .Stoffparameter_H2O import nreg2, ireg2, jreg2


def gammartaureg2(tau, pic):
    # Second derivative in tau of residual part of fundamental equation for region 2
    # Stefan Petersen
    # 10/10/02

    tau = tau - 0.5
    gamma = 0
    for i in range(len(nreg2)):
        gamma += nreg2[i] * pic ** ireg2[i] * jreg2[i] * tau ** (jreg2[i] - 1)
    return gamma
