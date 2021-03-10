import csv
import os


def gen_value(instance, attr):
    return {attr: getattr(instance, attr)}


def write_to_csv(csv_name, fields, row):
    if not os.path.exists(csv_name):
        with open(csv_name, 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    with open(csv_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)
