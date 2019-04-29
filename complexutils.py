import math
from loadflowreporter import LoadFlowReporter


# Funktion gibt den Betrag einer komplexen Zahl zurueck
def get_complex_magnitude(real, imag):
    return math.sqrt((real ** 2) + (imag ** 2))


# Funktion gibt eine komplexe Zahl in kartesischen Koordinaten zurueck
def get_cartesian(real, imag):
    return real + 1j * imag


# Funktion gibt eine komplexe Zahl in Polarkoordinaten zurueck
def get_polar(real, imag):
    # Bestimme Betrag der komplexen Zahl / Vektors
    r = get_complex_magnitude(real, imag)

    # Bestimme Winkel phi in Bogenmaß anhand des Quadraten
    if real < 0 and imag < 0:
        phi = math.atan(imag / real) - math.pi

    elif real == 0 and imag < 0:
        phi = -math.pi / 2

    elif real > 0:
        phi = math.atan(imag / real)

    elif real == 0 and imag > 0:
        phi = math.pi / 2

    elif real < 0 and imag >= 0:
        phi = math.atan(imag / real) + math.pi

    else:
        ERROR = ""

    return { "magnitude" : r, "angle" : phi, "angleGrad" : (phi*180 / math.pi)}


# Funktion gibt eine komplexe Zahl in euler'scher Darstellung zurueck
def get_euler(real, imag):
    return 1