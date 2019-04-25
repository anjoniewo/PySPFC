from complexutils import *


class Admittance:
	
	def __init__(self, impedance):
		
		# Realteil der Admittanz
		self.g = None
		
		# Imaginaerteil der Admittanz
		self.b = None
		
		# Wenn Querbelaege bekannt
		if impedance.get_magnitude():
			# g und b der Admittanz berechnen
			self.calculate_g_and_b(impedance)

		
	# Methode berechnet die Konduktanz sowie die Suszeptanz
	def calculate_g_and_b(self, impedance):
		self.g = (impedance.r / ((impedance.r * impedance.r) + (impedance.x * impedance.x)))
		self.b = - (impedance.x / ((impedance.r * impedance.r) + (impedance.x * impedance.x)))
		
	# Methode
	def get_magnitude(self):
		return get_complex_magnitude(self.g, self.b)
		
		
	