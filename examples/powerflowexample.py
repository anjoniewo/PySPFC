import pyspfc

# Grid - object instantiation
grid = pyspfc.Grid()

# import of grid/network data
# if import_path = '' the default directory 'csv_import' in the project folder will be set
# else the directory set to import_path will be chosen
# HINT: if the operating system is Windows you have to replace a single "\" by "\\"
# Example: "C:\Desktop\folder" --> "C:\\Desktop\\folder"
import_path = ''
grid.import_csv_data(import_path)

# run of power flow calculations
grid.do_powerflow()

# export of power flow calculation results
# results will automatically be exported to an 'export' folder int the import directory
grid.export_powerflow_results()

# creation of a PDF - report with significant data
# a pdf file with significant results will automatically be exported to an 'export' folder int the import directory
grid.create_pdf_report()



