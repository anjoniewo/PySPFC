import os.path
from LoadFlowTool.loadflowtool.grid.grid import Grid
from LoadFlowTool.loadflowtool.parser.gridparser import GridParser
from LoadFlowTool.loadflowtool.loadflow.loadflow import LoadFlow

# Erstelle Dateipfad zu grideline- und gridnode-Dateien
csv_files_path = os.path.join(os.path.dirname(__file__), "../../test/test_files/")

# Dateipfad fuer gridline-Datei
gridline_path = os.path.join(csv_files_path, "lines.csv")

# Dateipfad fuer gridnode-Datei
gridnode_path = os.path.join(csv_files_path, "gridnodes.csv")

# einlesen der Netzdaten
gridparser = GridParser(gridline_file_path=gridline_path, gridnode_file_path=gridnode_path, frequency=50)

# Erstellung des Netzwerks
network = Grid(grid_node_list=gridparser.grid_node_parser.get_gridnodes(),
               grid_line_list=gridparser.grid_line_parser.get_gridlines())

# network.print_bus_admittance_matrix()

# Lastflussberechnung für das eingelesene durchführen
loadflow = LoadFlow(network)

# Zeige Ergebnisse der Lastflussberechnung
print(loadflow)
