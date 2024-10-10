class Address:
    def __init__(self, address_id, address_line_1):
        self.address_id = address_id
        self.address_line_1 = address_line_1
        self.distances = []
        
    def set_distances(self, distance_row):
        self.distances = distance_row

    def get_distance_to_neighbor(self, other_address):
        distance = self.distances[other_address.address_id]
        return distance


    def __str__(self):
        address_string = f"Address: {self.address_line_1}, distances: {str(self.distances)}"
        return address_string