from LoadFlowTool.loadflowtool.utils.complexutils import *


class Admittance:

    def __init__(self, impedance=None, g=0, b=0):

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
            self.__g = g
            self.__b = b

        elif impedance.get_real_part() or impedance.get_imaginary_part():
            # g und b der Admittanz berechnen
            self.calc_admittance_from_impedance(impedance)

    # getter-Methoden
    def get_real_part(self):
        return self.__g

    def get_imaginary_part(self):
        return self.__b

    # setter-Methoden
    def set_real_part(self, g):
        self.__g = g

    def set_imaginary_part(self, b):
        self.__b = b

    # Methode berechnet die Konduktanz sowie die Suszeptanz
    def calc_admittance_from_impedance(self, impedance):
        admittance = calculate_complex_reciprocal(impedance.get_real_part(), impedance.get_imaginary_part())

        self.__g = admittance["real"]
        self.__b = admittance["imaginary"]

    # Methode gibt den Betrag der Admittanz wieder
    def get_magnitude(self):
        return get_complex_magnitude(self.__g, self.__b)

    # Methode addiert aus einem übergebenen Admittance-Objekte deren Werte auf die eigenen Werte
    # Methode ueberschreibt den "+" Operator fuer die Klasse Admittance
    def __add__(self, admittance_obj):
        a = self.__g
        b = self.__b
        c = admittance_obj.get_real_part()
        d = admittance_obj.get_imaginary_part()

        self.__g = a + c
        self.__b = b + d

        return self

    # Methode subtrahiert aus einem übergebenen Admittance-Objekte deren Werte von den eigenen Werten
    # Methode ueberschreibt den "-" Operator fuer die Klasse Admittance
    def __sub__(self, admittance_obj):
        a = self.__g
        b = self.__b
        c = admittance_obj.get_real_part()
        d = admittance_obj.get_imaginary_part()

        self.__g = a - c
        self.__b = b - d

        return self

    # Methode multipliziert aus einem übergebenen Admittance-Objekte deren Werte mit den eigenen Werten
    def __mul__(self, factor_obj):

        a = self.__g
        b = self.__b

        if type(factor_obj) == Admittance:
            c = factor_obj.get_real_part()
            d = factor_obj.get_imaginary_part()

            self.__g = a * c - b * d
            self.__b = a * d + b * c

        else:
            self.__g = a * factor_obj
            self.__b = b * factor_obj

        return self

    # Methode dividiert aus einem übergebenen Admittance-Objekte deren Werte mit den eigenen Werten
    def __truediv__(self, admittance_obj):
        a = self.__g
        b = self.__b
        c = admittance_obj.get_real_part()
        d = admittance_obj.get_imaginary_part()

        self.__g = (a * c + b * d) / (c ** 2 + d ** 2)
        self.__b = (c * b - a * d) / (c ** 2 + d ** 2)

        return self
