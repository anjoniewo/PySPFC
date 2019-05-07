from main.grid.grid import *
from main.parser.gridparser import GridParser

# network.create_grid_node("K1", 0, [0, 0, 400, 0])
# network.create_grid_node("K2", 1, [5, 1])
# network.create_grid_node("K3", 1, [5, 1])
# # network.create_grid_node("K4", 1, [5, 1])
# # network.create_grid_node("K5", 1, [5, 1])
# # network.create_grid_node("K6", 1, [5, 1])
# # network.create_grid_node("K7", 1, [5, 1])
# # network.create_grid_node("K8", 1, [5, 1])
# # network.create_grid_node("K9", 1, [5, 1])
# # network.create_grid_node("K3", 2, [25, 12, 400, 1])
#
# # network.create_grid_line("K1", "K2", [0.1, 0.206, 0.256, 0, 250])
# # network.create_grid_line("K2", "K3", [0.2, 0.206, 0.256, 0, 250])
# # network.create_grid_line("K1", "K3", [0.3, 0.206, 0.256, 0, 250])
#
# network.create_grid_line("K1", "K2", [1, 1, 1, 1, 1])
# network.create_grid_line("K2", "K3", [1, 1, 1, 1, 1])
# # network.create_grid_line("K3", "K4", [1, 1, 1, 1, 1])
# # network.create_grid_line("K4", "K5", [1, 1, 1, 1, 1])
# # network.create_grid_line("K5", "K6", [1, 1, 1, 1, 1])
# # network.create_grid_line("K6", "K7", [1, 1, 1, 1, 1])
# # network.create_grid_line("K7", "K8", [1, 1, 1, 1, 1])
# # network.create_grid_line("K8", "K9", [1, 1, 1, 1, 1])

""" TEST TEST TEST """
grid_line_path = "lines"
grid_node_path = "gridnodes"

gridparser = GridParser(50, grid_line_path, grid_node_path)

network = Grid(grid_line_list=gridparser.grid_line_parser.get_gridlines(),
               grid_node_list=gridparser.grid_node_parser.get_gridnodes())

network.calc_bus_admittance_matrix()
network.print_bus_admittanz_matrix()

# network.print_grid_node_list()
# network.print_grid_line_list()


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
