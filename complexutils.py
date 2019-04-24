import math


# Funktion git den Betrag einer komplexen Zahl zurueck
def get_complex_magnitude(real, imag):
    return math.sqrt((real * real) + (imag + imag))


# Funktion git eine komplexe Zahl in kartesischen Koordinaten zurueck
def get_cartesian(real, imag):
    return real + 1j * imag
    

# Funktion git eine komplexe Zahl in Polarkoordinaten zurueck
def get_polar(real, imag):
    return 1
    

# Funktion git eine komplexe Zahl in euler'scher Darstellung zurueck
def get_euler(real, imag):
    return 1