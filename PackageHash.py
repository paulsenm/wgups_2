class PackageHash:
    def __init__(self, size = 3):
        self.hash_table = [[] for _ in range(size)]

    def _hash(self, package_id):
        key = hash(package_id)
        return key % len(self.hash_table)
    
    def insert(self, package):
        package_id = package.package_id
        package_data = {
            'id': package.package_id,
            'address_line_1': package.address_line_1,
            'city': package.city,
            'state': package.state,
            'zip': package.zip,
            'deadline': package.deadline,
            'weight': package.weight,
            'notes': package.notes,
            'priority': package.priority,
            'status': package.status,
            'delivery_time': package.delivered_time
        } 
        index = self._hash(package_id)
        self.hash_table[index].append((package_id, package_data))

    def search(self, package_id):
        index = self._hash(package_id)
        for package in self.hash_table[index]:
            if package[0] == package_id:
                return package[1]
        return None
    
    
    def __str__(self):
        hash_string = ""
        for i in range(len(self.hash_table)):
            bucket = self.hash_table[i]
            row_string = ""
            for package in bucket:
                row_string += str(package)
                row_string += '\n'
            hash_string += row_string
            hash_string += "\n \n \n"
        return hash_string