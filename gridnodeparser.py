from gridelementparser import GridElementParser


# Parser-Klasse zum Einleser der Leitungsdaten
class GridNodeParser(GridElementParser):
	
	def __init__(self, file_path):
		
		super(GridNodeParser, self).__init__()
		
		self.node_parameters = []
		
		file_path = "C:\\Users\\EUProjekt\\Desktop\\AnjoNie\\02_Projekte\\LoadFlowSimulationTool\\" + str(
			file_path) + str(".csv")
		
		self.read_node_parameters(file_path)
	
	def read_node_parameters(self, file_path):
		self.read_csv_to_dictionary(file_path)
	
	
nodeparser = GridNodeParser("gridnodes")
s = ""