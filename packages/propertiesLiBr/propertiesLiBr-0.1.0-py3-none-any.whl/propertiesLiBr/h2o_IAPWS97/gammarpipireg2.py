
from Stoffparameter_H2O import nreg2, ireg2, jreg2
def gammarpipireg2(tau,pic):
	# Jan Albers
	# 15/12/2003

	# todo tau, pic prüfen 

	gammareg1 = 0
	for i in range(len(nreg1)):
		gammareg1 += nreg2[i] * ireg2[i] * (ireg2[i]-1) * pic**(ireg2[i]-2) * tau**jreg2[i]
	return gammareg1
