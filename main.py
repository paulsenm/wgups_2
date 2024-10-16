#Id: 012350434
#Michael Paulsen
#WGUPS App
#C950 - Data Structures II

from Hub import Hub
from PackageHash import PackageHash
from UI import UI

def main():
    test_hub = Hub()
    test_hub.assign_distances()
    package_hash_table = PackageHash()

    for package in test_hub.packages:
        package_hash_table.insert(package)

    test_hub.make_trucks()
    test_hub.load_trucks_initial()
    test_hub.start_deliveries()

    wgups_ui = UI(test_hub)
    wgups_ui.initialize_ui()

if __name__ == '__main__':
    main()
