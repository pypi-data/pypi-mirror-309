
from .pBound import pBound
from .tBound import tBound
from .entropyreg1 import entropyreg1
from .entropyreg2 import entropyreg2
from .entropyreg3 import entropyreg3
from .densreg3 import densreg3
from .pSatW import pSatW

def entropyW(temp, press):
	# die Funktion entropyW(temp, press) berechnet 
	# die spez. Enthalpie von Wasser oder Dampf
	# Temperatur in K
	# Druck in bar
	# spez. Entropie in kJ/kgK
	# erstellt von Jan Albers
	# 09.02.2005


	if 273.15 <= temp <= 623.15 and pSatW(temp) <= press <= 1000:
		# region 1
		return entropyreg1(temp, press)
	elif (273.15 <= temp <= 623.15 and 0 < press <= pSatW(temp)) or (
			623.15 <= temp <= 863.15 and 0 < press <= pBound(temp)) or (
			863.15 <= temp <= 1073.15 and press > 0 and press <= 1000):
		# region 2
		return entropyreg2(temp, press)
	elif 623.15 <= temp <= tBound(press) and pBound(temp) <= press <= 1000:
		# region 3
		density = densreg3(temp, press)
		return entropyreg3(temp, density)
	else:
		# outside range
		return -1
