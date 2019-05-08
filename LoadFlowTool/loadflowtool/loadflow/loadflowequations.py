import copy


class LoadFlowEquations:
	
	def __init__(self, grid_line_list=list(), grid_node_list=list()):
		
		self.__grid_line_list = copy.deepcopy(grid_line_list)
		
		self.__grid_node_list = copy.deepcopy(grid_node_list)
		
		self.__active_load_equations = list()
		
		self.__reactive_load_equations = list()
	
	def create_active_load_equations(self, ):
		
		E_i = 0
		E_j = 0
		F_i = 0
		F_j = 0
		# 
		G_ij = 0
		B_ij = 0
		P = 0
		
		P = E_i * (E_j * G_ij - F_j * B_ij) + F_i * (F_j * G_ij + E_j * B_ij)
