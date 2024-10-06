#utils for importing csv files and returning lists of package/address/truck objects

import csv

from Package import Package
from Address import Address

def import_distances(file):
    distance_matrix = []
    with open(file) as distance_csv:
        distance_data = csv.reader(distance_csv, delimiter=',')
        for row in distance_data:
            distance_row = []
            for distance in row:
                if not distance:
                    distance = -1
                distance_row.append(float(distance))
            distance_matrix.append(distance_row)
        for col in range(len(distance_matrix[0])):
            for row in range(len(distance_matrix)):
                if distance_matrix[row][col] == -1:
                    distance_matrix[row][col] = float(distance_matrix[col][row])
    return distance_matrix
    

def import_addresses(file):
    address_obj_list = []
    with open(file) as address_csv:
        address_data = csv.reader(address_csv, delimiter=',')
        for address in address_data:
            address_id = len(address_obj_list) + 1
            raw_address = address[0]
            address_line_1 = raw_address.split("(")[0].strip()
            address_obj = Address(address_id, address_line_1)

def import_packages(file):
    package_obj_list = []
    with open(file) as package_csv:
        package_data = csv.reader(package_csv, delimiter=',')
        for package in package_data:
            package_id = int(package[0])
            address_line_1 = package[1]
            city = package[2]
            state = package[3]
            zip = package[4]
            deadline = package[5]
            weight = package[7]
            status = "Unknown"
            notes = ""
            
            if package[7] is not None:
                notes = package[7]
            else:
                notes = "No notes"

            the_package = Package(package_id, address_line_1, city, state, zip, deadline, weight, notes, status)
            package_obj_list.append(the_package)
            #get priority using get_priority(deadline) function
            #make package obj

    return package_obj_list


