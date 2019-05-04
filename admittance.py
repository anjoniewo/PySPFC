from loadflowreporter import LoadFlowReporter
from complexutils import *


class Admittance:

    def __init__(self, impedance=None):

        # Realteil der Admittanz
        # X = Re{Z}
        # Y = Im{Z}
        # G = X / (X^2 + Y^2)
        self.__g = None

        # Imaginaerteil der Admittanz
        # X = Re{Z}
        # Y = Im{Z}
        # B = -Y / (X^2 + Y^2)
        self.__b = None

        if impedance is None:
            self.__g = self.__b = 0

        elif impedance.get_magnitude():
            # g und b der Admittanz berechnen
            self.calculate_g_and_b(impedance)

    # getter-Methoden
    def get_g(self):
        return self.__g

    def get_b(self):
        return self.__b

    # setter-Methoden
    def set_g(self, g):
        self.__g = g

    def set_b(self, b):
        self.__b = b

    # Methode berechnet die Konduktanz sowie die Suszeptanz
    def calculate_g_and_b(self, impedance):
        self.__g = (impedance.get_r() / ((impedance.get_r() ** 2) + (impedance.get_x() ** 2)))
        self.__b = - (impedance.get_x() / ((impedance.get_x() ** 2) + (impedance.get_x() ** 2)))

    # Methode gibt den Betrag der Admittanz wieder
    def get_magnitude(self):
        return get_complex_magnitude(self.__g, self.__b)

    # Methode addiert aus einem übergebenen Admittance-Objekte deren Werte auf die eigenen Werte
    def addition(self, admittance_obj):

        self.__g = self.__g + admittance_obj.__g
        self.__b = self.__b + admittance_obj.__b

    # Methode ueberschreibt den "+" Operator fuer die Klasse Admittance
    def __add__(self, admittance_obj):
        self.__g = self.__g + admittance_obj.__g
        self.__b = self.__b + admittance_obj.__b

        return self

    # Methode subtrahiert aus einem übergebenen Admittance-Objekte deren Werte von den eigenen Werten
    def subtraction(self, admittance_obj):
        self.__g = self.__g - admittance_obj.__g
        self.__b = self.__b - admittance_obj.__b

    # Methode ueberschreibt den "-" Operator fuer die Klasse Admittance
    def __sub__(self, admittance_obj):
        self.__g = self.__g - admittance_obj.__g
        self.__b = self.__b - admittance_obj.__b

        return self

    # Methode multipliziert aus einem übergebenen Admittance-Objekte deren Werte mit den eigenen Werten
    def multiplication(self, admittance_obj):
        self.__g = self.__g * admittance_obj.__g - self.__b * admittance_obj.__b
        self.__b = self.__g * admittance_obj.__b + self.__b * admittance_obj.__g

    # Methode dividiert aus einem übergebenen Admittance-Objekte deren Werte mit den eigenen Werten
    def division(self, admittance_obj):
        self.__g = (self.__g * admittance_obj.__g + self.__b * admittance_obj.__b) / (admittance_obj.__g ** 2 + admittance_obj.__b ** 2)
        self.__b = (self.__b * admittance_obj.__g - self.__g * admittance_obj.__b) / (admittance_obj.__g ** 2 + admittance_obj.__b ** 2)