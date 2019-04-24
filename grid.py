from gridnode import GridNode
from gridline import GridLine

-
--
-
-
-

# Klasse fuer ein elektrisches Netz
class Grid:

    # Initialisierungskonstruktor
    def __init__(self, frequency=50):
        
        # Netzfrequenz (default 50 Hz)
        self.frequency = frequency
        
        # Liste von Knoten und Liste von Leitungen
        self.grid_node_list = []
        self.grid_line_list = []

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
        line = GridLine(node_i, node_j, line_parameters, frequency)
        self.add_grid_line(line)

    # Methode fuegt der Leitungsliste einen Netzzweig hinzu
    def add_grid_line(self, grid_line):
        self.grid_line_list.append(grid_line)

    

    # Gibt alle Knoten des Netzes in der Konsole aus
    def print_grid_node_list(self):
        if not len(self.grid_node_list):
            print("")
            print("Keine Knoten in Liste")
        else:
            for i in range(0, len(self.grid_node_list)):
                self.grid_node_list[i].info()
