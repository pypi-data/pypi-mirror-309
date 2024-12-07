
from .Stoffparameter_H2O import nreg1, ireg1, jreg1
def gammareg1(tau, pic):
	# gammareg1(tau, pic)
	#
	# tau    reduced temperature     dimensionless
	# pic    reduced pressure        dimensionless
	#
	# IAPWS water properties 1997
	# First derivative of fundamental equation in pi for region 1
	#
	# Jan Albers 09.02.2005
	
	gammareg1 = 0
	for i in range(len(nreg1)):
		gammareg1 += nreg1[i] * (7.1 - pi) ** ireg1[i] * (tau - 1.222) ** jreg1[i]
	return gammareg1
