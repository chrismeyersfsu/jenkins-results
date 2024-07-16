#!/usr/bin/env python3

import sys
import csv

def write(csv_file_in, csv_file_out):
    # encoding='utf-8-sig' because this came from Grafana csv
    # The Unicode character U+FEFF is the byte order mark, or BOM, and is used to tell the difference between big- and little-endian UTF-16 encoding
    with open(csv_file_in, encoding='utf-8-sig', newline='') as csvfile:
        #reader = csv.reader(csvfile, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_NONE, doublequote=False)
        reader = csv.reader(csvfile)
        fieldnames = next(reader)
        print(f"Headers: {fieldnames}")

        with open(csv_file_out, "w", newline='') as file:
            writer = csv.writer(file, delimiter=',', escapechar='\\', quoting=csv.QUOTE_ALL, lineterminator='\n', quotechar='"', doublequote=False)
            writer.writerow(fieldnames)

            for line in reader:
                writer.writerow(line)


def run(csv_file_in, csv_file_out):
    write(csv_file_in, csv_file_out)


run(sys.argv[1], sys.argv[2])
