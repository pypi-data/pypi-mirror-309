# -*- coding: utf-8 -*-

from .enthalpyreg1 import enthalpyreg1
from .enthalpyreg2 import enthalpyreg2
#from enthalpyreg3 import enthalpyreg3
#from densreg3 import densreg3
#from tBound import tBound
from .pBound import pBound
from .pSatW import pSatW


def enthalpyW(temp, press):
    # die Funktion enthalpyW(temp, press) berechnet
    # die spez. Enthalpie von Wasser oder Dampf
    # Temperatur in K
    # Druck in bar
    # spez. Enthalpie in kJ/kg
    # erstellt von Stefan Petersen
    # 10/10/02
    # Hinweis: nur soweit nutzbar, wie notwendig für BPA_AKA1

    if 273.15 <= temp <= 623.15 and pSatW(temp) <= press <= 1000:  # region 1
        return enthalpyreg1(temp, press)
    elif (273.15 <= temp <= 623.15 and 0 < press <= pSatW(temp)) or (
            623.15 <= temp <= 863.15 and 0 < press <= pBound(temp)) or (
            863.15 <= temp <= 1073.15 and 0 < press <= 1000):
        # region 2
        return enthalpyreg2(temp, press)
        """    
        elif 623.15 <= temp <= tBound(press) and pBound(temp) <= press <= 1000:
            # region 3
            density = densreg3(temp, press)
            return enthalpyreg3(temp, density)
        """
    else:
        return -1
