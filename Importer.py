#utils for importing csv files and returning lists of package/address/truck objects

import csv

def import_packages(file):
    with open(file) as package_csv:
        package_data = csv.reader(package_csv, delimiter=',')
        for package in package_data:
            package_id = int(package[0])
            address_line_1 = package[1]
            city = package[2]
            state = package[3]
            