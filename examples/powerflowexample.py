import pyspfc

# Grid - object instantiation
grid = pyspfc.Grid()

# import of grid/network data from 'csv_import' directory in the project folder
import_path = 'C:\\Users\\Admin\\Desktop\\Neuer Ordner'
grid.import_csv_data(import_path)

# run of powerflow calculations
grid.do_powerflow()

# export of powerflow calculation results
grid.export_powerflow_results()

# creation of a PDF - report with significant data
grid.create_pdf_report()
