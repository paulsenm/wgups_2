from Hub import Hub
from PackageHash import PackageHash

def main():
    test_hub = Hub()
    test_hub.assign_distances()
    package_hash_table = PackageHash()

    for package in test_hub.packages:
        package_hash_table.insert(package)

    test_hub.make_trucks()
    test_hub.load_trucks_initial()
    test_hub.start_deliveries()

if __name__ == '__main__':
    main()
