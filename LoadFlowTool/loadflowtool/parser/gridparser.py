from LoadFlowTool.loadflowtool.parser.gridlineparser import GridLineParser
from LoadFlowTool.loadflowtool.parser.gridnodeparser import GridNodeParser


class GridParser:

    def __init__(self, frequency, gridline_file_path="", gridnode_file_path=""):
        self.grid_line_parser = GridLineParser(gridline_file_path, frequency)
        self.grid_node_parser = GridNodeParser(gridnode_file_path)
