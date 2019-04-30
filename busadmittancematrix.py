import numpy as np
from admittance import Admittance

# Klasse fuer die Erstellung der Knotenadmittanzmatrix
class BusAdmittanceMatrix:

    # Initialisierungskonstruktor
    def __init__(self):
        self.matrix = None

    # Methode zur Aufsummierung aller Admittanzen an einem Knoten
    #
    # Parameter:
    # Modus: True|False (all_admittances), Wenn True: werden alle (längs- und Quer-) Admittanzen aufsummiert. Wenn False: werden nur die Längsadmittanzen aufsummiert (Queradmittanzen werden igoniert)
    # aktueller Knoten (i),
    # Leitungsliste (grid_line_list)
    #
    # Rückgabewert: kummulierter Admittanzenwert
    def get_sum_of_grid_lines_on_node(self, node_name, grid_line_list, all_admittances=True):

        # Summenadmittanz an Knoten i
        sum_admittance = Admittance()

        for grid_line in grid_line_list:

            if node_name == grid_line.node_name_i or node_name == grid_line.node_name_j:

                # Addiere Längsadmittanz von Gridline zur Summenadmittanz
                sum_admittance.addition(grid_line.admittance)

                # Prüfen ob Modus "alle Admittanzen" true ist und ob Queradmittanz in Gridline vorhanden
                if all_admittances and grid_line.transverse_admittance:

                    # Teile Gridline Queradmittanz durch 2, da pro Knoten nur halbe Queradmittanz berechnet werden darf
                    grid_line.transverse_admittance.g = grid_line.transverse_admittance.g / 2
                    grid_line.transverse_admittance.b = grid_line.transverse_admittance.b / 2

                    # Addiere Queradmittanz von Gridline zur Summenadmittanz
                    sum_admittance.addition(grid_line.transverse_admittance)

        return sum_admittance

    # Methode zur Erstellung der Knotenpunkt-Admittanz Matrix
    def calc_matrix(self, grid_node_list, grid_line_list):

        # quadratische Matrixdimension: nxn
        n = len(grid_node_list)

        # Erstellung eines nxn Numpy-Arrays
        self.matrix = np.array(n, n)

        for i in range(0, n):
            for j in range(i, n):

                # Diagonalelemente der Matrix i=j
                if(i == j):
                    self.matrix[i][j] = self.get_sum_of_grid_lines_on_node(grid_node_list[i].name, grid_line_list)

                # Nicht-Diagonalelemente der Matrix i≠j
                else:
                    self.matrix[i][j] = self.matrix[j][i] = self.get_sum_of_grid_lines_on_node(grid_node_list[i].name, grid_line_list, False)

 # """
 #    # Methode zur Erzeugung der Knotenadimttanzmatrix auf Grundlage der Knoten und Zweige eines Netzes
 #    def get_bus_admittance_matrix(self, gridnodes, gridlines):
 #        Y = np.array()
 #
 #        for i in range(0, len(gridnodes)):
 #            for j in range(0, len(gridnodes)):
 #                Y[i][j] = 1
 #
 #    # Methode zur Konsolenausgabe der Matrix
 #    def print_bus_admittance_matrix(self):
 #        for i in range(0, self.rows):
 #            for j in range(0, self.columns):
 #                print("")
 #    """