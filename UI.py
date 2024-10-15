import datetime

class UI:
    def __init__(self, hub):
        self.hub = hub
        self.packages = hub.delivered_packages
        self.running = True  # Flag to control the UI loop

    def initialize_ui(self):
        print(f"Welcome to WGUPS command line UI")
        
        while self.running:
            print("Enter 1 to check package status by time.")
            print("Enter 2 to check a specific package by package id.")
            print("Enter 3 to view all delivered packages.")
            print("Enter 4 to exit.")

            user_input = input("Enter choice: ")

            match user_input:
                case "1":
                    self.check_package_status_by_time()
                case "2":
                    self.get_package_by_id()
                case "3":
                    self.view_all_delivered_packages()
                case "4":
                    self.exit_ui()
                case _:
                    print("Invalid choice. Please try again.")

    def get_package_by_id(self):
        package_id = input("Enter package id: ")
        try:
            package_id = int(package_id)
            package = self.search_package_by_id(package_id)
            if package:
                print(f"Package ID: {package.package_id}, Address: {package.address_obj.address_line_1}, Status: {package.status}")
            else:
                print(f"No package found with ID {package_id}.")
        except ValueError:
            print("Invalid package ID. Please enter a number.")

    def check_package_status_by_time(self):
        time_input = input("Enter time (HH:MM) to check package status: ")
        try:
            hours, minutes = map(int, time_input.split(":"))
            today = datetime.date.today()
            target_time = datetime.datetime.combine(today, datetime.time(hours, minutes))
            print(f"Checking packages delivered by {target_time}...")
            # Example filter by time - assuming packages have a 'delivered_time' attribute
            #late_packages = [pkg for pkg in self.packages if not pkg.on_truck_time]
            late_packages = []
            on_truck_packages = []
            en_route_packages = []
            delivered_packages = []
            for package in self.packages:
                # Check if the package was late to get on the truck
                if package.on_truck_time and package.on_truck_time >= target_time:
                    late_packages.append(package)
                # Check if the package is on the truck but not yet delivered
                elif package.on_truck_time and package.on_truck_time <= target_time and (package.en_route_time is None or package.en_route_time >= target_time):
                    on_truck_packages.append(package)
                # Check if the package is en route
                elif package.en_route_time and package.en_route_time <= target_time and (package.delivered_time is None or package.delivered_time > target_time):
                    en_route_packages.append(package)
                # Check if the package has already been delivered by the target time
                elif package.delivered_time and package.delivered_time <= target_time:
                    delivered_packages.append(package)
                else:
                    print(f"Package {package.package_id} was not found!")
                    if package.delivered_time:
                        print(f"Package had delivered time of {package.delivered_time}")


            # late_packages = [pkg for pkg in self.packages if pkg.on_truck_time and pkg.on_truck_time.time() >= target_time]
            # on_truck_packages = [pkg for pkg in self.packages if pkg.on_truck_time and pkg.on_truck_time.time() <= target_time and pkg.en_route_time.time() > target_time]
            # en_route_packages = [pkg for pkg in self.packages if pkg.en_route_time and pkg.en_route_time.time() >= target_time and pkg.delivered_time.time() > target_time]
            # delivered_packages = [pkg for pkg in self.packages if pkg.delivered_time and pkg.delivered_time.time() >= target_time]
            if late_packages:
                for package in late_packages:
                    #print(f"Package ID: {package.package_id}, Hasn't made it to the hub yet.")
                    print(package.print_status_time("late"))
            if on_truck_packages:
                for package in on_truck_packages:
                    #print(f"Package Id: {package.package_id}, Loaded onto truck at: {package.on_truck_time.time()}")
                    print(package.print_status_time("truck"))
            if en_route_packages:
                for package in en_route_packages:
                    #print(f"Package ID: {package.package_id}, On the way at {package.en_route_time.time()}")
                    print(package.print_status_time("route"))
            if delivered_packages:
                for package in delivered_packages:
                    #print(f"Package ID: {package.package_id}, Delivered at {package.delivered_time.time()}")
                    print(package.print_status_time("delivered"))
            else:
                print(f"No packages delivered by {target_time}.")
        except ValueError:
            print("Invalid time format. Please enter time in HH:MM format.")

    def search_package_by_id(self, package_id):
        for package in self.packages:
            if package.package_id == package_id:
                return package
        return None

    def view_all_delivered_packages(self):
        if not self.packages:
            print("No packages have been delivered yet.")
        else:
            print("All delivered packages:")
            for package in self.packages:
                print(f"Package ID: {package.package_id}, Delivered at {package.delivered_time}")

    def exit_ui(self):
        print("Exiting WGUPS command line UI. Goodbye!")
        self.running = False
