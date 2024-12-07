from .Stoffparameter_H2O import rgas_water
from .gamma0taureg2 import gamma0taureg2
from .gammartaureg2 import gammartaureg2
from .gamma0reg2 import gamma0reg2
from .gammarreg2 import gammarreg2


def entropyreg2(temp, press):
    # '
    # ' specific enthalpy in region 2
    # ' enthalpyreg2 in kJ/kg
    # ' temperature in K
    # ' pressure in bar

    tau = 540 / temp
    pic = 0.1 * press
    return 0.001 * rgas_water * (tau * (gamma0taureg2(tau, pic) + gammartaureg2(tau, pic)) - (
                gamma0reg2(tau, pic) + gammarreg2(tau, pic)))
