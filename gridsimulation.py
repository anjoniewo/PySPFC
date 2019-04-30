from grid import Grid


network = Grid()
network.create_grid_node("K1", 1, [5, 2])
network.create_grid_node("K2", 0, [25, 12, 400, 0])
network.create_grid_node("K3", 2, [25, 12, 400, 1])

#network.print_grid_node_list()

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
network.create_grid_line("K1","K2",[0.1, 0.206, 0.256, 0, 250])
network.create_grid_line("K2","K3",[0.2, 0.206, 0.256, 0, 250])
network.create_grid_line("K1","K3",[0.3, 0.206, 0.256, 0, 250])
#network.grid_line_list[0].info();

network.calc_bus_admittance_matrix()

print(network.show_admittanz_matrix())