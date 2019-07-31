import csv
import os


def export_data_to_csv(csv_export_path, file_name, data_dict):
	file_path_name = os.path.join(csv_export_path, file_name + ".csv")
	
	with open(file_path_name, 'w', newline='') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(data_dict.keys())
		writer.writerows(zip(*data_dict.values()))
		
		csvFile.close()
