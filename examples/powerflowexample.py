from simplepowerflow.grid import Grid

# Grid - object instantiation
network = Grid()

# import of grid/network data from 'csv_import' directory in the project folder
network.import_csv_data()

# run of simplepowerflow2 calculations
network.do_powerflow()

# export of simplepowerflow2 calculation results
network.export_powerflow_results()

# creation of a PDF - report with significant data
network.create_pdf_report()
