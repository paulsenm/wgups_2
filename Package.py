import datetime

from ColorPrinter import print_color as PC

class Package:
    def __init__(self, package_id, address_id, address_obj, address_line_1, city, state, zip, deadline, weight, notes, status, priority):
        self.package_id = package_id
        self.address_id = address_id
        self.address_obj = address_obj
        self.address_line_1 = address_line_1
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.priority = priority
        self.status = status if status is not None else "Unknown"
        self.at_hub_time = None 
        self.on_truck_time = None
        self.en_route_time = None
        self.delivered_time = None


    def print_status_time(self, status):
        package_priority = self.priority
        color = ""
        package_id_color = "blue"
        status_string = ""
        match status:
            case "late": 
                color = "red"
                status_string = f"running late"
            case "truck": 
                color = "yellow"
                status_string = f"on truck, stationary as of {self.on_truck_time.time()}"
            case "route": 
                color = "blue"
                status_string = f"on truck, headed to destination {self.en_route_time.time()}"
            case "delivered":
                color = "green"
                status_string = f"delivered as of {self.delivered_time.time()}"

        # match package_priority:
        #     case 1:
        #         package_id_color = "red"
        #     case 2: 
        #         package_id_color = "yellow"
        #     case 3:
        #         package_id_color = "green"

        if package_priority == 1:
            package_id_color = "red"
        elif package_priority == 2:
            package_id_color = "yellow"
        elif package_priority == 3:
            package_id_color = "green"
        else: package_id_color = "blue"



        return f"Package {PC(self.package_id, package_id_color)} is currently {PC(status_string, color)}"
    
    def __str__(self):
        package_string = f"Package ID: {str(self.package_id)}, address line 1: {self.address_line_1}, and address id was: {str(self.address_id)} and priority is: {str(self.priority)}"
        return package_string