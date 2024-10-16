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
    
    def search_kv(self, package_id):
        index = self._hash(package_id)
        for package_kv in self.hash_table[index]:
            if package_kv[0] == package_id:
                return package_kv
        return None

    def update(self, package):
        package_kv_to_update = self.search_kv(package.package_id)
        if package_kv_to_update:
            package_data = package_kv_to_update[1]
            package_data['address_line_1'] = package.address_obj.address_line_1
            package_data['city'] = package.city
            package_data['state'] = package.state
            package_data['zip'] = package.zip
            package_data['deadline'] = package.deadline
            package_data['status'] = package.status
            package_data['delivery_time'] = package.delivered_time
        else:
            print(f"Package with ID {package.package_id} not found for update.")
    
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