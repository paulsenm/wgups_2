import datetime

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
        self.delivered_time = None
        self.at_hub_time = None 
        self.on_truck_time = None
        self.en_route_time = None


    def print_status_time(self):
        pass
    
    def __str__(self):
        package_string = f"Package ID: {str(self.package_id)}, address line 1: {self.address_line_1}, and address id was: {str(self.address_id)} and priority is: {str(self.priority)}"
        return package_string