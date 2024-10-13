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
            target_time = datetime.time(hours, minutes)
            print(f"Checking packages delivered by {target_time}...")
            # Example filter by time - assuming packages have a 'delivered_time' attribute
            delivered_packages = [pkg for pkg in self.packages if pkg.delivered_time and pkg.delivered_time.time() <= target_time]
            if delivered_packages:
                for package in delivered_packages:
                    print(f"Package ID: {package.package_id}, Delivered at {package.delivered_time}")
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
