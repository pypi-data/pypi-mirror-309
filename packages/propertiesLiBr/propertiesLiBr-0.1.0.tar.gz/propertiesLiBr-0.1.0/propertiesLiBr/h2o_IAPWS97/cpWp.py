# -*- coding: utf-8 -*-

import numpy as np


def cpWp(temp):
    # cpWp(temp)
    #
    # cpWp          specific heat                 kJ/kg-K
    # temp          temperature                   K
    #
    # J.A. April 2003  Änderung der Eingangstemperartur auf Kelvin
    #
    # This def calculates the specific isobaric heat of water (cp in kJ/(kg*K) )
    # Although it is recommended to use the IAPWS97 methods for calculation of the properties of water
    # in technical aspects the following regressions (developed by ISE Freiburg) are used.
    # By means the same property data are used in the modells for ab- and adsorption chillers.
    # The difference to the IAPWS-values is lower then 0.1# in the interesting range between 0 and 100°C
    # and 1 to 10 bar respectively.

    a = [-5.92948717948624E-11, 1.81199009323988E-08, -2.13494318181802E-06, 1.29190887237757E-04,
         -3.80061034018061E-03, 4.21936117560825]

    #     Cp_Was=a(1)+a(2)*Tb+a(3)*Tb**2+a(4)*Tb**3+a(5)*Tb**4+a(6)*Tb**5
    return np.polyval(a, temp - 273.15)
