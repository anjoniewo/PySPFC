from loadflowreporter import LoadFlowReporter
from gridnode import GridNode
from gridline import GridLine
from busadmittancematrix import BusAdmittanceMatrix


# Klasse fuer ein elektrisches Netz
class Grid:

    # Initialisierungskonstruktor
    def __init__(self, frequency=50):
        
        # Netzfrequenz (default 50 Hz)
        self.frequency = frequency
        
        # Liste von Knoten und Liste von Leitungen
        self.grid_node_list = list()
        self.grid_line_list = list()

        # Instanzierung der LoadFlowReporter-Klasse
        self.load_flow_reporter = LoadFlowReporter()

        # Instanzierung der BusAdmittanceMatrix-Klasse
        self.bus_admittanz_matrix = BusAdmittanceMatrix()

    # Methode erstellt einen neuen Netzknoten und fuegt diesen der Knotenliste hinzu
    def create_grid_node(self, name, type, node_parameters):
        # Instanzierung eines neuen GridNode Objektes
        node = GridNode(name, type, node_parameters)
        self.add_grid_node(node)

    # Methode fuegt der Netzknotenliste einen Knoten hinzu
    def add_grid_node(self, grid_node):
        self.grid_node_list.append(grid_node)

    # Methode erstellt einen neuen Netzzweig und fuegt diese der Leitungsliste hinzu
    def create_grid_line(self, node_i, node_j, line_parameters):
        # Instanzierung eines neuen GridNode Objektes
        line = GridLine(self.frequency, node_i, node_j, line_parameters)
        self.add_grid_line(line)

    # Methode fuegt der Leitungsliste einen Netzzweig hinzu
    def add_grid_line(self, grid_line):
        self.grid_line_list.append(grid_line)

    # Gibt alle Knoten des Netzes in der Konsole aus
    def print_grid_node_list(self):
        if not len(self.grid_node_list):
            print("\nKeine Knoten in Liste")
        else:
            for i in range(0, len(self.grid_node_list)):
                self.grid_node_list[i].info()

        # Gibt alle Knoten des Netzes in der Konsole aus

    def print_grid_line_list(self):
        if not len(self.grid_line_list):
            print("\nKeine Leitungen in Liste")
        else:
            for i in range(0, len(self.grid_line_list)):
                self.grid_line_list[i].info()

    # Methode zur Berechnung der aktuellen Knotenadmittanz-Matrix
    # Übergabeparameter: Knotenliste [grid_node_list], Admittanzenliste (Gridline-Liste) [grid_line_list]
    def calc_bus_admittance_matrix(self):
        self.bus_admittanz_matrix.calc_matrix(self.grid_node_list, self.grid_line_list)

    # Methode gibt die aktuelle Knotenadmittanzmatrix zurück
    def get_bus_admittanz_matrix(self):
        return self.bus_admittanz_matrix.matrix

    # Methode gibt die aktuelle Knotenadmittanzmatrix zurück
    def print_bus_admittanz_matrix(self):
        result = ""
        matrix = self.bus_admittanz_matrix.matrix
        n = len(matrix)
        for i in range(0, n):
            for j in range(0, n):
                # print("{0}".format(self.bus_admittanz_matrix.matrix[i][j])
                if matrix[i][j].g is not None
                    result += str(matrix[i][j].g)
                print(matrix[i][j].g, matrix[i][j].b, "j" )