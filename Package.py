class Package:
    def __init__(self, package_id, address_id, address_line_1, city, state, zip, deadline, weight, notes, priority):
        self.package_id = package_id
        self.address_id = address_id
        self.address_line_1 = address_line_1
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.priority = priority
        self.status = "At Hub"
        self.delivered_time = None



    def __str__(self):
        package_string = f"Package ID: {str(self.package_id)}, address line 1: {self.address_line_1}, and address id was: {str(self.address_id)}"
        return package_string