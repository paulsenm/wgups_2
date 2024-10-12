import datetime

from ColorPrinter import print_color as PC
class Truck:
    def __init__(self, truck_id, addresses):
        self.truck_id = truck_id
        self.current_driver = -1
        self.package_queue_high = []
        self.package_queue_med = []
        self.package_queue_low = []
        self.delivered_packages = []
        self.is_full = False
        self.current_milage = 0
        self.current_location = addresses[0]
        self.current_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))
        self.current_package = None
        self.average_speed = 18
        self.package_qty = 16
        self.package_count = 0



    def load_package(self, package_to_insert):
        #print(f"loading package {package_to_insert.package_id} onto truck {self.truck_id}")
        #sort package into priority queue based on priority
        if package_to_insert.priority == 1:
            self.package_queue_high.append(package_to_insert)
        elif package_to_insert.priority == 2:
            self.package_queue_med.append(package_to_insert)
        elif package_to_insert.priority == 3:
            self.package_queue_low.append(package_to_insert)
        self.package_count += 1
        if self.package_count >= 16:
            self.is_full = True
    
    def deliver_all_queues(self):
        if len(self.package_queue_high) > 0:
            self.deliver_package_queue(self.package_queue_high)
            print(f"Delivered high priority packages for truck {self.truck_id}")
        if len(self.package_queue_med) > 0:
            self.deliver_package_queue(self.package_queue_med)
            print(f"Delivered medium priority packages for truck {self.truck_id}")
        if len(self.package_queue_low) > 0:
            self.deliver_package_queue(self.package_queue_low)
            print(f"Delivered low priority packages for truck {self.truck_id}")


    def deliver_package_queue(self, package_queue):
        print(f"made it to deliver_package_queue with {len(package_queue)} packages")
        while len(package_queue) > 0:
            package_to_deliver = self.get_nearest_package(package_queue)
            #if package_to_deliver is not None:
            self.deliver_package(package_to_deliver, package_queue)

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





    def deliver_package(self, package, package_queue):
        drive_distance = self.current_location.get_distance_to_neighbor(package.address_obj)
        self.current_milage += drive_distance
        self.add_time_from_distance(drive_distance)
        package.status = f"Delivered at {str(self.current_time)}"
        package.delivered_time = self.current_time
        package_queue.remove(package)
        self.delivered_packages.append(package)
        print(f"{PC("Delivered package:", "yellow")} {PC(package.package_id, "red")} to address: {package.address_obj.address_line_1} at time: {self.current_time.time()}")
        # if self.current_time > datetime.time(9, 5):
        #     print("time to get new packages")


    def add_time_from_distance(self, distance):
        minutes_per_mile = 60 / self.average_speed
        minutes_traveled = distance * minutes_per_mile
        time_delta = datetime.timedelta(minutes = minutes_traveled)
        self.current_time += time_delta


    def __str__(self):
        truck_string = f"Truck {self.truck_id} \nCount: {self.package_count} \n"
        for package in self.package_queue_high:
            truck_string += f"High priority package: {str(package)} \n"
        for package in self.package_queue_med:
            truck_string += f"Med priority package: {str(package)} \n"
        for package in self.package_queue_low:
            truck_string += f"Low piority package: {str(package)} \n"

        return truck_string