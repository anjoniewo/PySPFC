from unittest import TestCase
from simplepowerflow2.powerflowtool.grid.gridnode import GridNode


class TestGridNode(TestCase):
	
	# Methode fuer die Erstellung einer Liste mit GridNode-Parametern
	@staticmethod
	def create_gridnode_parameter_list(p_load, q_load, p_inject, q_inject, theta, volt):
		node_parameters = list()
		# active_load_power
		node_parameters.append(p_load)
		# reactive_load_power
		node_parameters.append(q_load)
		# active_injection_power
		node_parameters.append(p_inject)
		# reactive_injection_power
		node_parameters.append(q_inject)
		# theta in rad
		node_parameters.append(theta)
		# node_voltage
		node_parameters.append(volt)
		
		return node_parameters
	
	def test_set_node_parameters(self):
		gridnode = GridNode("K1", 0, self.create_gridnode_parameter_list(5, 1.2, 0, 0, 0.9, 0.4))
		print(gridnode.name)
	
	def test_print_gridnode_infos(self):
		gridnode = GridNode("K1", 0, self.create_gridnode_parameter_list(5, 1.2, 0, 0, 0.9, 0.4))
		print(gridnode)
