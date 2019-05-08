from LoadFlowTool.loadflowtool.grid.grid import Grid
from LoadFlowTool.loadflowtool.parser.gridparser import GridParser

# Dateipfad fuer gridline-Datei
gridline_path = "C:\\Users\\EUProjekt\\PycharmProjects\\LoadFlowToolProjekt\\test\\test_files\\lines.csv"
# Dateipfad fuer gridnode-Datei
gridnode_path = "C:\\Users\\EUProjekt\\PycharmProjects\\LoadFlowToolProjekt\\test\\test_files\\gridnodes.csv"

gridparser = GridParser(frequency=50, gridline_file_path=gridline_path, gridnode_file_path=gridnode_path)

network = Grid(grid_line_list=gridparser.grid_line_parser.get_gridlines(),
               grid_node_list=gridparser.grid_node_parser.get_gridnodes())

network.calc_bus_admittance_matrix()
network.print_bus_admittance_matrix()

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
