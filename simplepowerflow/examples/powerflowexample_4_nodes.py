import os.path

from simplepowerflow.powerflow.gridelements.admittance import Admittance
from simplepowerflow.powerflow.gridelements.grid import Grid
from simplepowerflow.powerflow.griddataimport.ALT_gridimport import GridImport
from simplepowerflow.powerflow.powerflow.powerflow import PowerFlow

# Erstelle Dateipfad zu grideline- und gridnode-Dateien
csv_files_path = os.path.join(os.path.dirname(__file__), '../../test/test_files/4_knoten')

# Dateipfad fuer gridline-Datei
gridline_path = os.path.join(csv_files_path, 'lines.csv')

# Dateipfad fuer gridnode-Datei
gridnode_path = os.path.join(csv_files_path, 'gridnodes_350kW.csv')

# Dateipfad fuer transformator-Datei
transformer_path = os.path.join(csv_files_path, 'transformers.csv')

# einlesen der Netzdaten
gridparser = GridImport(gridline_file_path=gridline_path, gridnode_file_path=gridnode_path,
                        transformer_path=transformer_path)

# Erstellung des Netzwerks
network = Grid(grid_node_list=gridparser.grid_node_parser.get_gridnodes(),
               grid_line_list=gridparser.grid_line_parser.get_gridlines(),
               transformer_list=gridparser.transformer_parser.get_transformers())

# Hier Admittanzmatrix manuell fuellen
admittance1 = Admittance(g=1.7647, b=-7.0588)
admittance2 = Admittance(g=-0.5882, b=2.3529)
admittance3 = Admittance(g=0, b=0)
admittance4 = Admittance(g=-1.1765, b=4.7059)
admittance5 = Admittance(g=1.5611, b=-6.6290)
admittance6 = Admittance(g=-0.3846, b=1.9231)
admittance7 = Admittance(g=2.9412, b=-11.7647)

# Diagonaelemte
network.bus_admittance_matrix.set_element(0, 0, admittance1)
network.bus_admittance_matrix.set_element(1, 1, admittance5)
network.bus_admittance_matrix.set_element(2, 2, admittance5)
network.bus_admittance_matrix.set_element(3, 3, admittance7)

# Nicht-Diagonalelemente
network.bus_admittance_matrix.set_element(0, 1, admittance2)
network.bus_admittance_matrix.set_element(0, 2, admittance3)
network.bus_admittance_matrix.set_element(0, 3, admittance4)
network.bus_admittance_matrix.set_element(1, 2, admittance6)
network.bus_admittance_matrix.set_element(1, 3, admittance2)
network.bus_admittance_matrix.set_element(2, 3, admittance4)

# network.print_bus_admittance_matrix()

# Lastflussberechnung für das eingelesene Netz durchführen
network.do_powerflow()
network.print_loadflow_results()