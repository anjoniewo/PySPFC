import os.path
from LoadFlowTool.loadflowtool.grid.grid import Grid
from LoadFlowTool.loadflowtool.griddataexport.export_results_to_pdf import create_pdf_report
from LoadFlowTool.loadflowtool.griddataimport.gridparser import GridParser

# Erstelle Dateipfad zu grideline- und gridnode-Dateien
csv_files_path = os.path.join(os.path.dirname(__file__), "../../test/test_files/3_knoten")

# Erstelle Dateipfad fuer export
csv_export_path = os.path.join(os.path.dirname(__file__), "../../test/test_export")

# Dateipfad fuer gridline-Datei
gridline_path = os.path.join(csv_files_path, "lines.csv")

# Dateipfad fuer gridnode-Datei
gridnode_path = os.path.join(csv_files_path, "gridnodes.csv")

# Dateipfad fuer transformator-Datei
transformer_path = os.path.join(csv_files_path, "transformers.csv")

# einlesen der Netzdaten
gridparser = GridParser(gridline_file_path=gridline_path, gridnode_file_path=gridnode_path,
                        transformer_path=transformer_path, frequency=50)

# Erstellung des Netzwerks

# Bezugsgroeßen des Netzwerks
v_nom = 220e3
s_nom = 100e6

network = Grid(grid_node_list=gridparser.grid_node_parser.get_gridnodes(),
               grid_line_list=gridparser.grid_line_parser.get_gridlines(),
               transformer_list=gridparser.transformer_parser.get_transformers(), v_nom=v_nom, s_nom=s_nom)

# network.print_bus_admittance_matrix()

# Lastflussberechnung für das eingelesene Netz durchführen
network.do_powerflow()
network.print_loadflow_results()
network.export_loadflow_results(csv_export_path=csv_export_path)
create_pdf_report()
