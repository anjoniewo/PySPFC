from unittest import TestCase
from main.admittance import Admittance
from main.impedance import Impedance


class TestAdmittance(TestCase):

    # Test fuer die Addition zweier Admittanzen
    def test_addition(self):
        admittance_1 = Admittance(Impedance(5, 2))
        admittance_2 = Admittance(Impedance(3, 6))

        admittance_1 += admittance_2

        print("")
        print("G = " + str(admittance_1.get_g()))
        print("B = " + str(admittance_1.get_b()))

    # Test fuer die Subtraktion zweier Admittanzen
    def test_subtraction(self):
        admittance_1 = Admittance(Impedance(5, 2))
        admittance_2 = Admittance(Impedance(3, 6))

        admittance_1 -= admittance_2

        print("")
        print("G = " + str(admittance_1.get_g()))
        print("B = " + str(admittance_1.get_b()))


