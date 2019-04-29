from gridelementparser import GridElementParser


# Parser-Klasse zum Einleser der Leitungsdaten
class GridLineParser(GridElementParser):
	
	def __init__(self, file_path):
		
		super(GridLineParser, self).__init__()
		
		self.line_parameters = []
		
		# Verzeichnis
		root = "C:\\Users\\EUProjekt\\Desktop\\AnjoNie\\02_Projekte\\LoadFlowSimulationTool\\"
		
		# Dateiname
		file_path =  root + str(file_path) + str(".csv")
		
		self.read_line_parameters(file_path)
		
	def read_line_parameters(self, file_path):
		self.read_csv_to_dictionary(file_path)
		

lineparser = GridLineParser("lines")