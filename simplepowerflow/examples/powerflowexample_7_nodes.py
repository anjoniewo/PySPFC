import os.path
from simplepowerflow.powerflow.grid.grid import Grid
from simplepowerflow.powerflow.griddataexport.export_results_to_pdf import create_pdf_report
from simplepowerflow.powerflow.griddataimport.gridimport import GridImport

# Erstelle Dateipfad zu grideline- und gridnode-Dateien
csv_files_path = os.path.join(os.path.dirname(__file__), '../../test/test_files/7_knoten_mit_trafo')

# Erstelle Dateipfad fuer export
csv_export_path = os.path.join(os.path.dirname(__file__), '../../test/test_export')

# Dateipfade fuer einzulesenden Dateien
gridline_path = os.path.join(csv_files_path, 'lines.csv')
gridnode_path = os.path.join(csv_files_path, 'gridnodes.csv')
transformer_path = os.path.join(csv_files_path, 'transformers.csv')

# einlesen der Netzdaten
gridparser = GridImport(gridline_file_path=gridline_path, gridnode_file_path=gridnode_path,
                        transformer_path=transformer_path)

# Bezugsgroeßen des Netzwerks
v_nom = 220e3
s_nom = 100e6

# Erstellung des Netzwerks
network = Grid(grid_node_list=gridparser.gridnodes, grid_line_list=gridparser.gridlines,
               transformer_list=gridparser.transformers, v_nom=v_nom, s_nom=s_nom)

# Lastflussberechnung für das eingelesene durchführen
network.do_powerflow()
network.export_powerflow_results(csv_export_path=csv_export_path)
create_pdf_report(network.powerflow.grid_node_results, network.powerflow.grid_line_results, v_nom, s_nom)