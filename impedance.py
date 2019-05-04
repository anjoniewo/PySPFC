from loadflowreporter import LoadFlowReporter
from complexutils import *


class Impedance:

	def __init__(self, r, x):

		# Realteil der Impedanz
		self.__r = r

		# Imaginaerteil der Impedanz
		self.__x = x
		self.haha

	def get_magnitude(self):
		return get_complex_magnitude(self.__r, self.__x)