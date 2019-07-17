import csv
import os

"""
    Konstanten
"""

TITLE_FONTSIZE = 16
LABEL_FONTSIZE = 14
TICK_FONTSIZE = 12

BAR_COLOR = 'red'


def get_file_names():
	"""
	reads a defined list of required file names for running the powerflow tool
	:param file_path: simplepowerflow/import_file_names.csv
	:return: a set of the file names
	"""
	file_path = os.path.join(os.path.dirname(__file__), '../../import_file_names.csv')
	with open(file_path, mode='r') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=";")
		
		file_names = dict()
		
		for row in csv_reader:
			file_names[row[0]] = row[1]
	
	return file_names
