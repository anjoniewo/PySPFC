from complexutils import *


class Impedance:
	
	def __init__(self, r, x):
		# Realteil der Impedanz
		self.r = r
		
		# Imaginaerteil der Impedanz
		self.x = x
	
	def get_magnitude(self):
		return get_complex_magnitude(self.r, self.x)