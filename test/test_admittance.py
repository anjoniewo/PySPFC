from unittest import TestCase

from pyspfc.gridelements.admittance import Admittance
from pyspfc.gridelements.impedance import Impedance


class TestAdmittance(TestCase):
	
	# Test fuer die Addition zweier Admittanzen
	def test_addition(self):
		admittance_1 = Admittance(impedance=Impedance(5, 2))
		admittance_2 = Admittance(impedance=Impedance(3, 6))
		
		admittance_1 += admittance_2
		
		print("")
		print("G = " + str(admittance_1.get_real_part()))
		print("B = " + str(admittance_1.get_imaginary_part()))
	
	# Test fuer die Subtraktion zweier Admittanzen
	def test_subtraction(self):
		admittance_1 = Admittance(g=5, b=2)
		admittance_2 = Admittance(g=3, b=6)
		
		admittance_1 -= admittance_2
		
		print("")
		print("G = " + str(admittance_1.get_real_part()))
		print("B = " + str(admittance_1.get_imaginary_part()))
	
	def test_multiplication(self):
		admittance_1 = Admittance(impedance=Impedance(5, 2))
		admittance_2 = Admittance(impedance=Impedance(3, 6))
		
		admittance_1 *= admittance_2
		
		print("")
		print("G = " + str(admittance_1.get_real_part()))
		print("B = " + str(admittance_1.get_imaginary_part()))
	
	def test_division(self):
		admittance_1 = Admittance(impedance=Impedance(0.16, -0.12))
		admittance_2 = Admittance(g=2, b=2)
		
		admittance_1 /= admittance_2
		
		print("")
		print("G = " + str(admittance_1.get_real_part()))
		print("B = " + str(admittance_1.get_imaginary_part()))
