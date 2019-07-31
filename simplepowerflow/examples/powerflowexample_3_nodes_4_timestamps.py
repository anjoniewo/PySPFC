import os.path

from simplepowerflow.powerflow.grid import Grid

csv_export_path = os.path.join(os.path.dirname(__file__), '../../test/test_export/6_knoten_export')

network = Grid()
network.import_csv_data()
network.do_powerflow()
network.export_powerflow_results()
# create_pdf_report(network.powerflow.grid_node_results, network.powerflow.grid_line_results, v_nom, s_nom)
