from unittest import TestCase

from simplepowerflow.powerflow.grid.grid import Grid


class TestGrid(TestCase):
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
	pass
	
	def test_import_csv_data(self):
		grid = Grid(grid_node_list=list(), grid_line_list=list(), transformer_list=list(), v_nom=200, s_nom=100)
		grid.import_csv_data()
		grid.print_grid_line_list()
		grid.print_grid_node_list()
		
		assert 1 == 1
