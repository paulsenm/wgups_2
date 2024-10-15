import datetime
from ColorPrinter import print_color as PC

class Truck:
    def __init__(self, truck_id, addresses):
        self.truck_id = truck_id
        self.current_driver = -1
        self.all_queues = {
            "package_queue_high": [],
            "package_queue_med": [],
            "package_queue_low": [],
            "delivered_packages": []
        }
        # self.package_queue_high = []
        # self.package_queue_med = []
        # self.package_queue_low = []
        # self.delivered_packages = []
        self.late_package_count = 0
        self.is_full = False
        self.current_milage = 0
        self.hub_location = addresses[0]
        self.current_location = addresses[0]
        self.current_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))
        self.current_package = None
        self.average_speed = 18
        self.package_qty = 16
        self.package_count = 0
        self.got_late_packages = False

    def load_package(self, package_to_insert):
        self.set_on_truck_time(package_to_insert, self.current_time)
        if package_to_insert.priority == 1:
            self.all_queues["package_queue_high"].append(package_to_insert)
        elif package_to_insert.priority == 2:
            self.all_queues["package_queue_med"].append(package_to_insert)
        elif package_to_insert.priority == 3:
            self.all_queues["package_queue_low"].append(package_to_insert)
        self.package_count += 1
        if self.package_count >= 16:
            self.is_full = True
    
    def set_en_route_time(self, package, time):
        package.en_route_time = time

    def set_on_truck_time(self, package, time):
        package.on_truck_time = time

    def deliver_all_queues(self, hub, start_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))):
        self.current_time = start_time
        
        for queue_name, queue in self.all_queues.items():
            if len(queue) > 0 and queue_name != "delivered_packages":
                self.deliver_package_queue(queue, hub)
                print(f"Done delivering {queue_name} packages for truck {self.truck_id}")

        # if len(self.package_queue_high) > 0:
        #     self.deliver_package_queue(self.package_queue_high, hub)
        #     print(f"Delivered high priority packages for truck {self.truck_id}")
        # if len(self.package_queue_med) > 0:
        #     self.deliver_package_queue(self.package_queue_med, hub)
        #     print(f"Delivered medium priority packages for truck {self.truck_id}")
        # if len(self.package_queue_low) > 0:
        #     self.deliver_package_queue(self.package_queue_low, hub)
        #     print(f"Delivered low priority packages for truck {self.truck_id}")
        print(f"total milage for truck {self.truck_id} was {self.current_milage}")
        self.go_to_hub()
        if hub.third_truck_sent == False:
            hub.send_third_truck(self.current_time)

    def deliver_package_queue(self, package_queue, hub):
        print(f"Delivering packages, {len(package_queue)} remaining")
        while len(package_queue) > 0:
            package_to_deliver = self.get_nearest_package(package_queue)
            self.deliver_package(package_to_deliver, package_queue, hub)

    def get_nearest_package(self, package_queue):
        closest_distance = 1000
        closest_package = package_queue[0]
        for package in package_queue:
            delivery_address = package.address_obj
            distance_to_address = self.current_location.get_distance_to_neighbor(delivery_address)
            if distance_to_address <= closest_distance:
                closest_distance = distance_to_address
                closest_package = package
        return closest_package

    def deliver_package(self, package, package_queue, hub):
        drive_distance = self.current_location.get_distance_to_neighbor(package.address_obj)
        self.current_milage += drive_distance
        self.add_time_from_distance(drive_distance)
        package.status = f"Delivered at {str(self.current_time)}"
        package.delivered_time = self.current_time
        package_queue.remove(package)
        self.all_queues["delivered_packages"].append(package)
        hub.delivered_packages.append(package)
        self.current_location = package.address_obj
        if package.priority == 1:
            id_color = "red"
        elif package.priority == 2:
            id_color = "yellow"
        elif package.priority == 3:
            id_color = "green"
        print(f"{PC('Delivered package:', id_color)} {PC(package.package_id, 'red')} to address: {package.address_obj.address_line_1} at time: {PC(self.current_time.time(), 'blue')}")

        # Check if it is past 9:05 AM, get late packages/update addresses
        if self.current_time.time() >= datetime.time(9, 5) and self.got_late_packages == False and hub.late_packages:
            print(PC(f"Time is {self.current_time.time()}. Returning to hub for late packages.", "green"))
            self.got_late_packages = True
            self.return_to_hub_for_late_packages(hub)


    def return_to_hub_for_late_packages(self, hub):
        late_packages = hub.late_packages
        if late_packages:
            self.go_to_hub()
            while len(hub.late_packages) > 0:
                self.load_package(hub.get_next_late_package())
                self.late_package_count += 1
            print(f"Truck {self.truck_id} loaded {self.late_package_count} late packages.")
        else:
            print(f"No late packages available for truck {self.truck_id} at 9:05 AM.")

    def go_to_hub(self):
        print(f"going back to hub from {self.current_location.address_line_1}")
        distance_to_add = self.current_location.get_distance_to_neighbor(self.hub_location)
        self.add_time_from_distance(distance_to_add)
        self.current_location = self.hub_location

    def add_time_from_distance(self, distance):
        minutes_per_mile = 60 / self.average_speed
        time_delta = datetime.timedelta(minutes=distance * minutes_per_mile)
        self.current_time += time_delta

    def __str__(self):
        truck_string = f"Truck {self.truck_id} \nCount: {self.package_count} \n"
        for queue_name, queue in self.all_queues.items():
            for package in queue:
                truck_string += f"{queue_name} package: {str(package)}"
        # for package in self.package_queue_high:
        #     truck_string += f"High priority package: {str(package)} \n"
        # for package in self.package_queue_med:
        #     truck_string += f"Medium priority package: {str(package)} \n"
        # for package in self.package_queue_low:
        #     truck_string += f"Low priority package: {str(package)} \n"
        return truck_string
