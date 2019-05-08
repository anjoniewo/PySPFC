from main.parser.gridlineparser import GridLineParser
from main.parser.gridnodeparser import GridNodeParser


class GridParser:

    def __init__(self, frequency, gridline_file_path="", gridnode_file_path=""):
        self.grid_line_parser = GridLineParser(gridline_file_path, frequency)
        self.grid_node_parser = GridNodeParser(gridnode_file_path)

    # # getter-Methoden
    # def get_grid_line_parser(self):
    #     return self.get_grid_line_parser()
    #
    # def get_grid_node_parser(self):
    #     return self.get_grid_node_parser()
