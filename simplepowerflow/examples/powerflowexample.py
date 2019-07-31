from simplepowerflow.powerflow.grid import Grid

# Grid - object instantiation
network = Grid()

# import of grid/network data from 'csv_import' directory in the project folder
network.import_csv_data()

# run of powerflow calculations
network.do_powerflow()

# export of powerflow calculation results
network.export_powerflow_results()

# creation of a PDF - report with significant data
"""
@TODO: not yet customized to time series data
"""
network.create_pdf_report()
