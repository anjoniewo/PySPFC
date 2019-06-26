import csv
import os


def export_grid_line_data(csv_export_path, file_name, data_dict):
    file_path_name = os.path.join(csv_export_path, file_name + ".csv")

    data = [data_dict]

    with open(file_path_name, 'w', newline='') as csvFile:
        fields = [*data_dict]
        writer = csv.DictWriter(csvFile, delimiter=';', fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

        csvFile.close()
