import csv
import os


def export_grid_line_data(file_name, data_dict):
    csv_files_path = os.path.join(os.path.dirname(__file__), "test\\test_export")
    file_path_name = os.path.join(csv_files_path, file_name + ".csv")

    data = [data_dict]

    with open(file_path_name, 'w', newline='') as csvFile:
        fields = [*data_dict]
        writer = csv.DictWriter(csvFile, delimiter=';', fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

        csvFile.close()
