from loadflowreporter import LoadFlowReporter
from complexutils import *


class Admittance:

    def __init__(self, impedance=None):

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

        if impedance is None:
            self.g = self.b = 0

        elif impedance.get_magnitude():
            # g und b der Admittanz berechnen
            self.calculate_g_and_b(impedance)

    # Methode berechnet die Konduktanz sowie die Suszeptanz
    def calculate_g_and_b(self, impedance):
        self.g = (impedance.r / ((impedance.r ** 2) + (impedance.x ** 2)))
        self.b = - (impedance.x / ((impedance.r ** 2) + (impedance.x ** 2)))

    # Methode gibt den Betrag der Admittanz wieder
    def get_magnitude(self):
        return get_complex_magnitude(self.g, self.b)

    # Methode addiert aus einem übergebenen Admittance-Objekte deren Werte auf die eigenen Werte
    def addition(self, admittance_obj):

        self.g = self.g + admittance_obj.g
        self.b = self.b + admittance_obj.b

    # Methode subtrahiert aus einem übergebenen Admittance-Objekte deren Werte von den eigenen Werten
    def subtraction(self, admittance_obj):
        self.g = self.g - admittance_obj.g
        self.b = self.b - admittance_obj.b

    # Methode multipliziert aus einem übergebenen Admittance-Objekte deren Werte mit den eigenen Werten
    def multiplication(self, admittance_obj):
        self.g = self.g * admittance_obj.g - self.b * admittance_obj.b
        self.b = self.g * admittance_obj.b + self.b * admittance_obj.g

    # Methode dividiert aus einem übergebenen Admittance-Objekte deren Werte mit den eigenen Werten
    def division(self, admittance_obj):
        self.g = (self.g * admittance_obj.g + self.b * admittance_obj.b) / (admittance_obj.g ** 2 + admittance_obj.b ** 2)
        self.b = (self.b * admittance_obj.g - self.g * admittance_obj.b) / (admittance_obj.g ** 2 + admittance_obj.b ** 2)