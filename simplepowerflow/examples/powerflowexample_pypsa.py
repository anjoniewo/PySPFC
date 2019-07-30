import os.path
from simplepowerflow.powerflow.gridelements.grid import Grid
from simplepowerflow.powerflow.griddataimport.ALT_gridimport import GridImport
from simplepowerflow.powerflow.powerflow.powerflow import PowerFlow

# Erstelle Dateipfad zu grideline- und gridnode-Dateien
csv_files_path = os.path.join(os.path.dirname(__file__), "../../test/test_files/pypsa_example")

# Dateipfad fuer gridline-Datei
gridline_path = os.path.join(csv_files_path, "lines.csv")

# Dateipfad fuer gridnode-Datei
gridnode_path = os.path.join(csv_files_path, "gridnodes_350kW.csv")

# Dateipfad fuer transformator-Datei
transformer_path = os.path.join(csv_files_path, "transformers.csv")

# einlesen der Netzdaten
gridparser = GridImport(gridline_file_path=gridline_path, gridnode_file_path=gridnode_path,
                        transformer_path=transformer_path)

# Erstellung des Netzwerks
network = Grid(grid_node_list=gridparser.grid_node_parser.get_gridnodes(),
               grid_line_list=gridparser.grid_line_parser.get_gridlines(),
               transformer_list=gridparser.transformer_parser.get_transformers())

# network.print_bus_admittance_matrix()

# Lastflussberechnung für das eingelesene durchführen
network.do_powerflow()
network.print_loadflow_results()