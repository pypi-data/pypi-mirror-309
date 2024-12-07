# -*- coding: utf-8 -*-


from .Stoffparameter_H2O import nreg2, ireg2, jreg2


def gammartautaureg2(tau, pic):
    # Second derivative in tau of residual part of fundamental equation for region 2
    # 15/12/02

    tau = tau - 0.5
    gamma = 0
    for i in range(len(nreg2)):
        gamma = nreg2 * pic ** ireg2 * jreg2 * (jreg2 - 1) * tau ** (jreg2 - 2)

    return tau
