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
        self.late_packages = []
        self.late_package_count = 0
        self.third_truck_sent = False

    def assign_distances(self):
        for address in self.addresses:
            address.set_distances(self.distance_matrix[address.address_id - 1])

    def make_trucks(self):
        for i in range(self.truck_qty):
            new_truck_id = i + 1
            new_truck = Truck(new_truck_id, self.addresses)
            self.truck_fleet.append(new_truck)

    def load_trucks_initial(self):
        truck_2_mandatory_strings = ["Can only be on truck 2", "Must be delivered with"]
        delayed_package_strings = ["Delayed on flight", "Wrong address"]

        for package in self.packages:
            package_notes = package.notes
            if "Delayed" in package_notes or "Wrong" in package_notes:
                self.late_packages.append(package)
                self.late_package_count += 1
            else:
                if package_notes != "No notes":
                    for string in truck_2_mandatory_strings:
                        if string in package_notes:
                            self.truck_fleet[1].load_package(package)
                elif package.priority == 1:
                    self.truck_fleet[0].load_package(package)
                else:
                    if not self.truck_fleet[2].is_full:
                        if package.priority != 2:
                            self.truck_fleet[2].load_package(package)
                        else:
                            self.truck_fleet[1].load_package(package)
                    else:
                        self.truck_fleet[0].load_package(package)

    def start_deliveries(self):
        self.truck_fleet[0].deliver_all_queues(self)
        self.truck_fleet[1].deliver_all_queues(self)
        
    def send_third_truck(self, driver_return_time):
        self.third_truck_sent = True
        self.truck_fleet[2].deliver_all_queues(self, driver_return_time)
        

    def get_next_late_package(self):
        if self.late_packages:
            package_to_load = self.late_packages[0]
            self.late_packages.remove(package_to_load)
            return package_to_load
