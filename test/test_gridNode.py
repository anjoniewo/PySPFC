from unittest import TestCase
from LoadFlowTool.loadflowtool.grid.gridnode import GridNode


class TestGridNode(TestCase):
	
	# Methode fuer die Erstellung einer Liste mit GridNode-Parametern
	@staticmethod
	def create_gridnode_parameter_list():
		node_parameters = list()
		# active_load_power
		node_parameters.append(5)
		# reactive_load_power
		node_parameters.append(1.2)
		# active_injection_power
		node_parameters.append(0)
		# reactive_injection_power
		node_parameters.append(0)
		# theta in rad
		node_parameters.append(0.9)
		# node_voltage
		node_parameters.append(0.4)
		
		return node_parameters
	
	def test_set_node_parameters(self):
		gridnode = GridNode("K1", 0, self.create_gridnode_parameter_list())
	
	def test_print_gridnode_infos(self):
		gridnode = GridNode("K1", 0, self.create_gridnode_parameter_list())
		print(gridnode)
