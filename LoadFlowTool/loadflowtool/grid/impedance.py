from LoadFlowTool.loadflowtool.utils.complexutils import *


class Impedance:
	# Parameter: r -> Realteil, x -> Imaginärteil, in_serie -> sind Real- und Imaginärteil in serie oder parallel [default: in serie]
	def __init__(self, r, x, in_series=True, admittance=None):
		
		self.__r = None
		self.__x = None
		
		if admittance:
			self.calc_impedance_from_admittance(admittance)
			
		elif in_series:
			# Realteil der Impedanz
			self.__r = r
			# Imaginaerteil der Impedanz
			self.__x = x
		else:
			if not r and x:
				self.__x = x
			
			if r and not x:
				self.__r = r
			
			if r and x:
				# Realteil der Impedanz
				self.__r = (r * (x ** 2)) / (r ** 2 + x ** 2)
				# Imaginaerteil der Impedanz
				self.__x = ((r ** 2) * x) / (r ** 2 + x ** 2)
	
	# getter-Methoden
	def get_real_part(self):
		return self.__r
	
	def get_imaginary_part(self):
		return self.__x
	
	# setter-Methoden
	def set_real_part(self, r):
		self.__r = r
	
	def set_imaginary_part(self, x):
		self.__x = x
	
	def get_magnitude(self):
		return get_complex_magnitude(self.__r, self.__x)
	
	# Methode berechnet die Konduktanz sowie die Suszeptanz
	def calc_impedance_from_admittance(self, admittance):
		impedance = calculate_complex_reciprocal(admittance.get_real_part(), admittance.get_imaginary_part())
		
		self.__r = impedance["real"]
		self.__x = impedance["imaginary"]
