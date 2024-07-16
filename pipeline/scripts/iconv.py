#!/usr/bin/env python3

import sys
import csv

def write(csv_file_in):
    # encoding='utf-8-sig' because this came from Grafana csv
    # The Unicode character U+FEFF is the byte order mark, or BOM, and is used to tell the difference between big- and little-endian UTF-16 encoding
    with open(csv_file_in, encoding='utf-8-sig') as csvin:
        print(csvin.read())

def run(csv_file_in):
    write(csv_file_in)

run(sys.argv[1])
