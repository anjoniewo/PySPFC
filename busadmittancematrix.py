import numpy as np
from np import *

# Klasse fuer die Erstellung der Knotenadmittanzmatrix
class BusAdmittanceMatrix:

    # Initialisierungskonstruktor
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = np.array(rows, columns)

    # Methode zur Erzeugung der Knotenadimttanzmatrix auf Grundlage der Knoten und Zweige eines Netzes
    def getBusAdmittanceMatrix(self, gridnodes, gridlines):
        Y = np.array()

        for i in range(0, len(gridnodes)):
            for j in range(0, len(gridnodes)):
                Y[i][j] = 1

    # Methode zur Konsolenausgabe der Matrix
    def printBusAdmittanceMatrix(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                print("")
