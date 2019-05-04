from main.parser.gridlineparser import GridLineParser
from main.parser.gridnodeparser import GridNodeParser


class GridParser:
	
	def __init__(self, frequency, line_file_path, node_file_path):
		
		self.grid_line_parser = GridLineParser(line_file_path, frequency)
		self.grid_node_parser = GridNodeParser(node_file_path)
