from grid import Grid

network = Grid()
network.create_grid_node("K1", 1, [5, 2])
network.create_grid_node("K2", 0, [25, 12, 400, 0])
network.create_grid_node("K3", 2, [25, 12, 400, 1])
network.print_grid_node_list()
