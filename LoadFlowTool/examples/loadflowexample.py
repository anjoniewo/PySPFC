import os.path
from LoadFlowTool.loadflowtool.grid.grid import Grid
from LoadFlowTool.loadflowtool.parser.gridparser import GridParser
from LoadFlowTool.loadflowtool.loadflow.jacobianmatrix import JacobianMatrix
from LoadFlowTool.loadflowtool.utils.loadflowutils import print_matrix
from LoadFlowTool.loadflowtool.loadflow.loadflow import do_loadflow

import numpy as np

# Erstelle Dateipfad zu grideline- und gridnode-Dateien

# WINDOWS
current_file_path = os.path.abspath(os.path.dirname(__file__))
csv_files_path = os.path.join(current_file_path, "..\\..\\test\\test_files\\")

# MAC
# csv_files_path = os.path.join(os.path.dirname(__file__), "../../test/test_files/")

# Dateipfad fuer gridline-Datei
gridline_path = os.path.join(csv_files_path, "lines.csv")

# Dateipfad fuer gridnode-Datei
gridnode_path = os.path.join(csv_files_path, "gridnodes.csv")

# einlesen der Netzdaten
gridparser = GridParser(gridline_file_path=gridline_path, gridnode_file_path=gridnode_path, frequency=50)

# Erstellung des Netzwerks
network = Grid(grid_line_list=gridparser.grid_line_parser.get_gridlines(),
               grid_node_list=gridparser.grid_node_parser.get_gridnodes())

# network.print_bus_admittance_matrix()
# network.print_grid_node_list()

# Lastflussberechnung für das eingelesene durchführen
do_loadflow(network)
