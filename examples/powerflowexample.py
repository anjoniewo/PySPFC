import pyspfc

# Grid - object instantiation
grid = pyspfc.Grid()

# import of grid/network data
# if import_path = '' the default directory 'csv_import' in the project folder will be set
# else the chosen directory will be set
import_path = ''
grid.import_csv_data(import_path)

# run of powerflow calculations
grid.do_powerflow()

# export of powerflow calculation results
# results will automatically be exported to an 'export' folder int the import directory
grid.export_powerflow_results()

# creation of a PDF - report with significant data
# a pdf file with significant results will automatically be exported to an 'export' folder int the import directory
grid.create_pdf_report()
