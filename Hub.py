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
        self.delivered_packages = []
        self.third_truck_sent = False
        self.hashed_packages = PackageHash()
        
        for package in self.packages:
            self.hashed_packages.insert(package)

    #Use adjacency matrix/distance matrix to assign relative distances to each address
    def assign_distances(self):
        for address in self.addresses:
            address.set_distances(self.distance_matrix[address.address_id - 1])

    #Make the fleet of trucks and provide each one with an id, list of addresses, and reference to hub
    def make_trucks(self):
        for i in range(self.truck_qty):
            new_truck_id = i + 1
            new_truck = Truck(new_truck_id, self.addresses, self)
            self.truck_fleet.append(new_truck)

    #Load the on-time packages into the trucks - use notes and deadlines to assign most time sensitive
    #packages on to the first 2 trucks to leave the hub
    def load_trucks_initial(self):
        truck_2_mandatory_strings = ["Can only be on truck 2", "Must be delivered with"]
        delayed_package_strings = ["Delayed on flight", "Wrong address"]

        for package in self.packages:
            package_notes = package.notes
            #These packages won't be available until later - their information is stored in the hub's late_packages queue
            if "Delayed" in package_notes or "Wrong" in package_notes:
                self.late_packages.append(package)
                self.late_package_count += 1
            else:
                #If package has notes, check for notes that require the package to be on truck 2
                if package_notes != "No notes":
                    for string in truck_2_mandatory_strings:
                        if string in package_notes:
                            self.truck_fleet[1].load_package(package)
                #Put highest priority package(s) on truck 1
                elif package.priority == 1:
                    self.truck_fleet[0].load_package(package)
                else:
                    #If truck 3 has room, and package priority is low, load package on truck 3
                    if not self.truck_fleet[2].is_full:
                        if package.priority != 2:
                            self.truck_fleet[2].load_package(package)
                        else:
                            #Load medium priority packages onto truck 2
                            self.truck_fleet[1].load_package(package)
                    else:
                        #Load overflow packages on truck 1
                        self.truck_fleet[0].load_package(package)

    #Start delivery with the first 2 trucks
    def start_deliveries(self):
        self.truck_fleet[0].deliver_all_queues()
        self.truck_fleet[1].deliver_all_queues()
    
    #Send the third truck out for deliveries after one truck gets back
    def send_third_truck(self, driver_return_time):
        self.third_truck_sent = True
        self.truck_fleet[2].deliver_all_queues(driver_return_time)
    
    #Use time to get the status of each package 
    def print_packages_by_time(self, time):
        packages_at_hub = []
        packages_on_truck = []
        packages_en_route = []
        for package in self.packages:
            if package.at_hub_time and package.at_hub_time <= time:
                packages_at_hub.append(package)
            elif package.on_truck_time and package.on_truck_time <= time:
                packages_on_truck.append(package)
            elif  package.en_route_time and package.en_route_time <= time:
                packages_en_route.append(package)
        print(f"there were {len(packages_at_hub)} packages at the hub, {len(packages_on_truck)} packages on a truck, and {len(packages_en_route)} en route.")

    #Remove late packages from late package queue and load them onto the truck when info is available 
    def get_next_late_package(self, current_time):
        if self.late_packages:
            package_to_load = self.late_packages[0]
            self.late_packages.remove(package_to_load)
            package_to_load.en_route_time = current_time
            return package_to_load
