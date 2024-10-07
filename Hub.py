from Package import Package
from ImporterUtils import import_packages, import_distances, import_addresses
from PackageHash import PackageHash

class Hub:
    def __init__(self):
        self.truck_fleet = None
        self.addresses, self.address_dict = import_addresses("CSV/addresses.csv")
        self.distance_matrix = import_distances("CSV/distances.csv")
        self.packages = import_packages("CSV/package_list.csv", self.address_dict)

    

    def assign_distances(self):
        for address in self.addresses:
            address.set_distances(self.distance_matrix[address.address_id - 1])


    def get_address_obj_from_address_str(self):
        pass

    def assign_address_objs_to_packages(self):
        pass

    

    def __str__(self):
        hub_string = "Hub string \n"
        hub_string += "Printing distances: \n"
        for row in self.distance_matrix:
            hub_string += str(row)
            hub_string += "\n"
        hub_string += "Printing Addresses:"
        for address in self.addresses:
            hub_string += str(address)
            hub_string += "\n"
        if len(self.packages) > 0:
            for package in self.packages:
                hub_string += str(package)
                hub_string += "\n"
        return hub_string