import datetime

from PackageHash import PackageHash as PH
from ColorPrinter import print_color as PC

class Truck:
    def __init__(self, truck_id, addresses, hub):
        self.truck_id = truck_id
        self.current_driver = -1
        self.all_queues = {
            "package_queue_high": [],
            "package_queue_med": [],
            "package_queue_low": [],
            "delivered_packages": []
        }
        self.late_package_count = 0
        self.is_full = False
        self.current_milage = 0
        self.hub = hub
        self.hub_location = addresses[0]
        self.current_location = addresses[0]
        self.current_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))
        self.current_package = None
        self.average_speed = 18
        self.package_qty = 16
        self.package_count = 0
        self.got_late_packages = False

    #Append package to low/medium/high priority queue based on priority
    def load_package(self, package_to_insert):
        hub = self.hub
        self.set_on_truck_time(package_to_insert, self.current_time)
        package_to_insert.truck_id = self.truck_id
        if package_to_insert.priority == 1:
            self.all_queues["package_queue_high"].append(package_to_insert)
        elif package_to_insert.priority == 2:
            self.all_queues["package_queue_med"].append(package_to_insert)
        elif package_to_insert.priority == 3:
            self.all_queues["package_queue_low"].append(package_to_insert)
        self.package_count += 1
        if self.package_count >= 16:
            self.is_full = True
        hub.hashed_packages.update(package_to_insert)
    
    #Set status and the time the status changed
    def set_en_route_time(self, package, time):
        package.en_route_time = time
        package.status = "En route"

    #Set status and the time the status changed
    def set_on_truck_time(self, package, time):
        package.on_truck_time = time
        package.status = "On truck"

    #Deliver all queues based on priority
    def deliver_all_queues(self, start_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))):
        hub = self.hub
        self.current_time = start_time

        for queue_name, queue in self.all_queues.items():
            for package in queue:
                package.en_route_time = start_time
        
        for queue_name, queue in self.all_queues.items():
            if len(queue) > 0 and queue_name != "delivered_packages":
                self.deliver_package_queue(queue)
                print(f"Done delivering {queue_name} packages for truck {self.truck_id}")

        print(f"total milage for truck {self.truck_id} was {self.current_milage}")
        self.go_to_hub()
        if hub.third_truck_sent == False:
            hub.send_third_truck(self.current_time)

    #Deliver every package in individual queue
    def deliver_package_queue(self, package_queue):
        hub = self.hub
        print(f"Delivering packages, {len(package_queue)} remaining")
        while len(package_queue) > 0:

            package_to_deliver = self.get_nearest_package(package_queue)
            self.deliver_package(package_to_deliver, package_queue)

    #Get the nearest package from the current queue
    def get_nearest_package(self, package_queue):
        #Get packages from the other queues if they have the same address
        out_of_queue_packages = self.get_same_address_other_queues(self.current_location)
        if len(out_of_queue_packages) > 0:
            print(f"There were {len(out_of_queue_packages)} out of queue packages with matching addresses.")
            for package_and_queue in out_of_queue_packages:
                package = package_and_queue[0]
                queue_name = package_and_queue[1]
                queue = self.all_queues[queue_name]
                self.deliver_package_out_of_queue(package, queue)
        #Get the closest package in this queue
        closest_distance = 1000
        closest_package = package_queue[0]
        for package in package_queue:
            delivery_address = package.address_obj
            distance_to_address = self.current_location.get_distance_to_neighbor(delivery_address)
            if distance_to_address <= closest_distance:
                closest_distance = distance_to_address
                closest_package = package
        return closest_package

    #Check the other queues for packages with the same address
    def get_same_address_other_queues(self, address):
        packages_with_same_address = []
        for queue_name, queue in self.all_queues.items():
            if queue_name != "delivered_packages":
                for package in queue:
                    if package.address_obj == address:
                        packages_with_same_address.append([package, queue_name])
        return packages_with_same_address

    #Deliver a package that wasn't in the original queue
    def deliver_package_out_of_queue(self, package, package_queue):
        hub = self.hub
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

    #Deliver package in order from current queue
    def deliver_package(self, package, package_queue):#hub-refactor
        hub = self.hub
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
            self.return_to_hub_for_late_packages()

    #Go back to hub after late packages arrive
    def return_to_hub_for_late_packages(self):#hub-refactor
        hub = self.hub
        late_packages = hub.late_packages
        if late_packages:
            self.go_to_hub()
            while len(hub.late_packages) > 0:
                self.load_package(hub.get_next_late_package(self.current_time))
                self.late_package_count += 1
            print(f"Truck {self.truck_id} loaded {self.late_package_count} late packages.")
        else:
            print(f"No late packages available for truck {self.truck_id} at 9:05 AM.")

    #Go back to hub, record distance if part of deliveries
    def go_to_hub(self):
        print(f"going back to hub from {self.current_location.address_line_1}")
        if self.hub.third_truck_sent == True:
            distance_to_add = self.current_location.get_distance_to_neighbor(self.hub_location)
            self.add_time_from_distance(distance_to_add)
        self.current_location = self.hub_location

    #Add time based on distance traveled and average truck speed
    def add_time_from_distance(self, distance):
        minutes_per_mile = 60 / self.average_speed
        time_delta = datetime.timedelta(minutes=distance * minutes_per_mile)
        self.current_time += time_delta

    #Overwrite to-string for truck
    def __str__(self):
        truck_string = f"Truck {self.truck_id} \nCount: {self.package_count} \n"
        for queue_name, queue in self.all_queues.items():
            for package in queue:
                truck_string += f"{queue_name} package: {str(package)}"
        return truck_string
