from LoadFlowTool.loadflowtool.utils.complexutils import *


class Impedance:

    def __init__(self, r=0, x=0):
        # Realteil der Impedanz
        self.__r = r

        # Imaginaerteil der Impedanz
        self.__x = x

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
