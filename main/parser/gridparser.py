from main.parser.gridlineparser import GridLineParser
from main.parser.gridnodeparser import GridNodeParser


class GridParser:

    def __init__(self, frequency, line_file_path, node_file_path):
        self.__grid_line_parser = GridLineParser(line_file_path, frequency)
        self.__grid_node_parser = GridNodeParser(node_file_path)

    # getter-Methoden
    def get_grid_line_parser(self):
        return self.get_grid_line_parser()

    def get_grid_node_parser(self):
        return self.get_grid_node_parser()
