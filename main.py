from Hub import Hub
from PackageHash import PackageHash

test_hub = Hub()
test_hub.assign_distances()
print(test_hub)
package_hash_table = PackageHash()

for package in test_hub.packages:
    package_hash_table.insert(package)

#print(f"package data from hashed package with id of 6 was: {package_hash_table.search(6)}")

#print(f"hash table: \n{package_hash_table}")

test_hub.make_trucks()
test_hub.load_trucks()