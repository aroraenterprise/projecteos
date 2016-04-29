"""
Project: tools
Author: Saj Arora
Description: 
"""
import argparse
import csv
import os


def csv_file_parser(file):
    if not os.path.isfile(file):
        raise Exception('%s file does not exist!' % file)

    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        fieldnames = []
        for row in reader:
            fieldnames = [x.lower() for x in row]
            break

        reader = csv.DictReader(csv_file, fieldnames, delimiter=',', quotechar='"')
        for index, row in enumerate(reader):
            if index == 0:
                continue



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()

    csv_file_parser(args.input)


if __name__ == "__main__":
    main()
