import numpy as np

# Klasse fuer die Erstellung der Knotenadmittanzmatrix
class BusAdmittanceMatrix:

    # Initialisierungskonstruktor
    def __init__(self):
        self.matrix = None

    """
    # Methode zur Erzeugung der Knotenadimttanzmatrix auf Grundlage der Knoten und Zweige eines Netzes
    def get_bus_admittance_matrix(self, gridnodes, gridlines):
        Y = np.array()

        for i in range(0, len(gridnodes)):
            for j in range(0, len(gridnodes)):
                Y[i][j] = 1

    # Methode zur Konsolenausgabe der Matrix
    def print_bus_admittance_matrix(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                print("")
    """


    # Methode zur Erstellung der Knotenpunkt-Admittanz Matrix
    def calc_bus_admittance_matrix(self, grid_node_list, grid_line_list):

        # quadratische Matrixdimension: nxn
        n = len(grid_node_list)

        # Erstellung eines nxn Numpy-Arrays
        self.matrix = np.array(n, n)

        for i in range(0, n)
            for j in range(i, n)

                # Diagonalelemente der Matrix i=j
                if(i == j)
                    self.matrix[i][j] = get_sum_of_grid_lines_on_node(i)

                # Nicht-Diagonalelemente der Matrix i≠j
                else
                    self.matrix[i][j],self.matrix[j][i] = get_sum_of_connected_grid_lines_between_node_(i)
