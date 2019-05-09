import math


# Funktion gibt den Kehrwert einer komplexen Zahl als Dictionary zurück
def calculate_complex_reciprocal(real, imaginary):
    if real and imaginary:
        real_result = (real / ((real ** 2) + (imaginary ** 2)))
        imaginary_result = (- (imaginary / ((real ** 2) + (imaginary ** 2))))

    elif real:
        real_result = 1 / real
        imaginary_result = imaginary

    elif imaginary:
        real_result = real
        imaginary_result = - 1 / imaginary

    complex_reciprocal = {
        "real": real_result,
        "imaginary": imaginary_result
    }

    return complex_reciprocal


# Funktion gibt den Betrag einer komplexen Zahl zurueck
def get_complex_magnitude(real, imaginary):
    return math.sqrt((real ** 2) + (imaginary ** 2))


# Funktion gibt eine komplexe Zahl in kartesischen Koordinaten zurueck
def get_cartesian(real, imaginary):
    return real + 1j * imaginary


# Funktion gibt eine komplexe Zahl in Polarkoordinaten zurueck
def get_polar(real, imaginary):
    # Bestimme Betrag der komplexen Zahl / Vektors
    r = get_complex_magnitude(real, imaginary)

    # Bestimme Winkel phi in Bogenmaß anhand des Quadraten
    if real < 0 and imaginary < 0:
        phi = math.atan(imaginary / real) - math.pi

    elif real == 0 and imaginary < 0:
        phi = -math.pi / 2

    elif real > 0:
        phi = math.atan(imaginary / real)

    elif real == 0 and imaginary > 0:
        phi = math.pi / 2

    elif real < 0 and imaginary >= 0:
        phi = math.atan(imaginary / real) + math.pi

    else:
        ERROR = ""

    return {"magnitude": r, "angle": phi, "angleGrad": (phi * 180 / math.pi)}


# Funktion gibt eine komplexe Zahl in euler'scher Darstellung zurueck
def get_euler(real, imaginary):
    return 1
