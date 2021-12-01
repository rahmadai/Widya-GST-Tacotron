import sys
import csv
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--input_path", type=str)
parser.add_argument("--output_path", type=str)

global args
args = parser.parse_args()

if __name__ == "__main__":
    input_path = args.input_path
    output_path = args.output_path
    list_source = []
    list_original = []
    with open(input_path, mode="r") as csv_file:
        csv_read = csv.reader(csv_file)
        for row in csv_read:
            data = row[0]
            list_original.append(row)
            list_source.append(data.split(" ")[0])

    print(list_source)
    np_list_source = np.array(list_source)
    sorted_list_source = np.argsort(np_list_source)
    for index in range(0, len(sorted_list_source)):
        print(list_original[sorted_list_source[index]])

    with open(output_path, mode="w") as csv_file:
        csv_writer = csv.writer(csv_file)
        for index in range(0, len(sorted_list_source)):
            csv_writer.writerow(list_original[sorted_list_source[index]])
