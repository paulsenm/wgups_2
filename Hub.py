import datetime

from Package import Package
from ImporterUtils import import_packages, import_distances, import_addresses
from PackageHash import PackageHash
from Truck import Truck

class Hub:
    def __init__(self):
        self.truck_fleet = []
        self.addresses, self.address_dict = import_addresses("CSV/addresses.csv")
        self.distance_matrix = import_distances("CSV/distances.csv")
        self.packages = import_packages("CSV/package_list.csv", self.address_dict)
        self.truck_qty = 3

    

    def assign_distances(self):
        for address in self.addresses:
            address.set_distances(self.distance_matrix[address.address_id - 1])


    def make_trucks(self):
        for i in range(self.truck_qty):
            new_truck_id = i+1
            new_truck = Truck(new_truck_id, self.addresses)
            self.truck_fleet.append(new_truck)

    def load_trucks_initial(self):
        truck_2_mandatory_strings = ["Can only be on truck 2", "Must be delivered with"]
        delayed_package_strings = ["Delayed on flight", "Wrong address"]


        for package in self.packages:
            package_notes = package.notes            
            if "Delayed" not in package_notes and "Wrong" not in package_notes:
                if package_notes != "No notes":
                    print(f"package {package.package_id} had some notes! {package_notes}")
                    for string in truck_2_mandatory_strings:
                        if string in package_notes:
                            self.truck_fleet[1].load_package(package)
                elif package.priority == 1:
                    self.truck_fleet[0].load_package(package)
                else:
                    if self.truck_fleet[2].is_full == False:
                        self.truck_fleet[2].load_package(package)
                    else:
                        self.truck_fleet[0].load_package(package)
        for truck in self.truck_fleet:
            print(str(truck))
                    
    def start_deliveries(self):
        for truck in self.truck_fleet:
            truck.deliver_all_queues()
            
    def update_addresses(self, current_time, package):
        if current_time >= datetime.time(10, 30):
            print(f"Addresses updated at {str(current_time)}")
    
    
    

    def __str__(self):
        hub_string = "Hub string \n"
        # hub_string += "Printing distances: \n"
        # for row in self.distance_matrix:
        #     hub_string += str(row)
        #     hub_string += "\n"
        hub_string += "Addresses:"
        for address in self.addresses:
            hub_string += str(address)
            hub_string += "\n"
        if len(self.packages) > 0:
            for package in self.packages:
                hub_string += str(package)
                hub_string += "\n"
        return hub_string