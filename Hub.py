from Package import Package
from ImporterUtils import import_packages, import_distances

class Hub:
    def __init__(self):
        self.truck_fleet = None
        self.addresses = None
        self.distance_matrix = import_distances("distances.csv")
        self.packages = import_packages("package_list.csv")

    



    def __str__(self):
        hub_string = "Hub string \n"
        hub_string += "Printing distances: \n"
        for row in self.distance_matrix:
            hub_string += str(row)
            hub_string += "\n"
        if len(self.packages) > 0:
            for package in self.packages:
                hub_string += str(package)
                hub_string += "\n"
        return hub_string