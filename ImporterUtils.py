#utils for importing csv files and returning lists of package/address/truck objects

import csv
import datetime

from Package import Package
from Address import Address

#Import the distances from distance csv, create adjacency matrix
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
    
#Make a list of address objects from address csv
def import_addresses(file):
    address_dict = {}
    address_obj_list = []
    with open(file) as address_csv:
        address_data = csv.reader(address_csv, delimiter=',')
        for address in address_data:
            address_id = len(address_obj_list) + 1
            raw_address = address[0]
            address_line_1 = raw_address.split("(")[0].strip()
            if "5383" in address_line_1:
                address_line_1 = "5383 South 900 East #104"            
            address_obj = Address(address_id, address_line_1)
            address_obj_list.append(address_obj)
            address_dict[address_line_1] = address_obj

    #for key in address_dict:
        #print(f"key was: {key}, value was: {str(address_dict[key])}")
    return address_obj_list, address_dict

#Make list of package objects from package csv
def import_packages(file, address_dict):
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
            weight = package[6]
            status = "Tracking info sent"
            notes = package[7] if package[7] else "No notes"
            priority = 3
            
            
            address_obj = address_dict.get(address_line_1)
            address_id = address_obj.address_id if address_obj else None
            #print(f"In import_packages, package_id was: {package_id} address_id was: {address_id}")
            if address_id is None:
                #print(f"couldn't find matching address for: {address_line_1}")
                address_line_1 = "5383 South 900 East #104"
                address_obj = address_dict.get("5383 South 900 East #104")

            if deadline != "EOD":
                deadline_time_high = datetime.time(9, 5)
                deadline_time_med = datetime.time(10, 30)
                deadline_time = datetime.datetime.strptime(deadline, "%I:%M %p").time()
                if deadline_time <= deadline_time_high:
                    priority = 1
                elif deadline_time <= deadline_time_med:
                    priority = 2
                


            the_package = Package(package_id, address_id, address_obj, address_line_1, city, state, zip, deadline, weight, notes, status, priority)
            package_obj_list.append(the_package)
            #get priority using get_priority(deadline) function
            #make package obj

    return package_obj_list


