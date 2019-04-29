from loadflowreporter import LoadFlowReporter
from complexutils import *


class Admittance:
	
	def __init__(self, impedance):
		
		# Realteil der Admittanz
		# X = Re{Z}
		# Y = Im{Z}
		# G = X / (X^2 + Y^2)
		self.g = None
		
		# Imaginaerteil der Admittanz
		# X = Re{Z}
		# Y = Im{Z}
		# B = -Y / (X^2 + Y^2)
		self.b = None
		
		# Wenn Querbelaege bekannt
		if impedance.get_magnitude():
			# g und b der Admittanz berechnen
			self.calculate_g_and_b(impedance)

	# Methode berechnet die Konduktanz sowie die Suszeptanz
	def calculate_g_and_b(self, impedance):
		self.g = (impedance.r / ((impedance.r ** 2) + (impedance.x ** 2)))
		self.b = - (impedance.x / ((impedance.r ** 2) + (impedance.x ** 2)))
		
	# Methode
	def get_magnitude(self):
		return get_complex_magnitude(self.g, self.b)