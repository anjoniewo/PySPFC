import os.path
from LoadFlowTool.loadflowtool.grid.grid import Grid
from LoadFlowTool.loadflowtool.parser.gridparser import GridParser

# Erstelle Dateipfad zu grideline- und gridnode-Dateien
current_file_path = os.path.abspath(os.path.dirname(__file__))
csv_files_path = os.path.join(current_file_path, "..\\..\\test\\test_files\\")

# Dateipfad fuer gridline-Datei
gridline_path = os.path.join(csv_files_path, "lines.csv")

# Dateipfad fuer gridnode-Datei
gridnode_path = os.path.join(csv_files_path, "gridnodes.csv")

gridparser = GridParser(frequency=50, gridline_file_path=gridline_path, gridnode_file_path=gridnode_path)

network = Grid(grid_line_list=gridparser.grid_line_parser.get_gridlines(),
               grid_node_list=gridparser.grid_node_parser.get_gridnodes())

network.calc_bus_admittance_matrix()
network.print_bus_admittance_matrix()
network.print_grid_node_list()

""" create_grid_line-Parameter (
        STRING Knotenname_1,
        STRING Knotenname_2,
        LIST Kabel_Leitungsparameter[ 
            FLOAT Leitungslaenge,                #(km)
            FLOAT resistiver Längsleitungsbelag, #(Ω/km)
            FLOAT induktiver Längsleitungsbelag, #(mH/km)
            FLOAT resistiver Querleitungsbelag,  #(Ω/km)
            FLOAT kapazitiver Querleitungsbelag  #(nF/km)
        ]
    )
"""
