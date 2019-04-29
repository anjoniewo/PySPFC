from loadflowreporter import LoadFlowReporter
from complexutils import *


class Impedance:

	def __init__(self, r, x):

		# Realteil der Impedanz
		self.r = r if r is not None else 0

		# Imaginaerteil der Impedanz
		self.x = x if x is not None else 0

	def get_magnitude(self):
		return get_complex_magnitude(self.r, self.x)