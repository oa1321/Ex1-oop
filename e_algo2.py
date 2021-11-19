import csv
import json
import sys

"""
savas the call data in an object 
"""
class Call:
    call_raw_data = []
    time = 0
    origin = 0
    destination = 0
    state = 0
    elevator_call = 0

    def __init__(self, call_data):
        if call_data[0] == 'Elevator call':
            self.call_raw_data = call_data
            self.time = float(call_data[1])
            self.origin = int(call_data[2])
            self.destination = int(call_data[3])
            self.state = int(call_data[4])
            self.elevator_call = int(call_data[5])

    def get_csv_format(self):
        return ['Elevator call',self.time,self.origin,self.destination,0,self.elevator_call]

    def __str__(self):
        return "Call handle by elevator: " + str(self.elevator_call) + " got called in: " + \
               str(self.time) + " route: " + str(self.origin) + "-->" + str(self.destination)

"""
the elevator class gets the data of the elevator and saves it for easier use of the data
also saves a list that contain all the calls objects that the elevator will do
"""
class Elevator:
    elevator_raw_data = {}
    number = 0
    floor_per_sec = 1
    min_floor = 0
    max_floor = 0
    close_time = 0
    open_time = 0
    start_time = 0
    stop_time = 0
    call_list = []
    section = 0

    def __init__(self, e_data):
        self.elevator_raw_data = e_data
        self.number = e_data['_id']
        self.floor_per_sec = e_data['_speed']
        self.min_floor = e_data['_minFloor']
        self.max_floor = e_data['_maxFloor']
        self.close_time = e_data['_closeTime']
        self.open_time = e_data['_openTime']
        self.start_time = e_data['_startTime']
        self.stop_time = e_data['_stopTime']
        self.section = self.number

    def set_call_list(self, empty_list):
        self.call_list = empty_list

    def __str__(self):
        return "[-|-] NO." + str(self.number) + " speed(in Floor-Per-Second): " + str(self.floor_per_sec) + \
               " section - " + str(self.section)

"""
the building class gets the data of the building and saves it for easier use of the data
also saves a list that contain all the elevators object that are in the building
"""
class Building:
    min_floor = 0
    max_floor = 0
    elevator_num = 0
    list_of_elevators = []
    building_raw_data = {}
    floors = 0

    def __init__(self, building_data):
        self.max_floor = building_data['_maxFloor']
        self.min_floor = building_data['_minFloor']
        self.elevator_num = building_data['_elevators']
        self.floors = abs(self.max_floor - self.min_floor) + 1

    def __str__(self):
        elevator_str = ""
        call_str = ""
        j = 0
        for i in self.list_of_elevators:
            elevator_str = elevator_str + str(j) + ")" + str(i) + "\n"
            j += 1
            for k in i.call_list:
                call_str = call_str + "  " + str(k) + "\n"
                """
            elevator_str += call_str
            call_str = ""
            """
        return "Building range: " + str(self.min_floor) + " <--> " + \
               str(self.max_floor) + "\nELEVATORS:\n" + elevator_str

"""
open the files and returning 3 lists that contains the files data
"""
def open_files(json_file_name, csv_file_name):
    with open(json_file_name) as f:
        data = json.load(f)

    my_elevators = data['_elevators']
    data['_elevators'] = len(my_elevators)
    my_building = data

    all_calls = []
    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            all_calls.append(row)
    return all_calls, my_building, my_elevators

"""
gets a file name and call list and write the data on the list to the file
"""
def write_file(csv_file_name, my_calls):
    with open(csv_file_name, 'w',newline='') as f:
        writer = csv.writer(f)
        for call in my_calls:
            row = call.get_csv_format()
            writer.writerow(row)

"""
calc for each elevator the total time it will take for her to do all the calls she have + the new call
"""
def calc_total_wait_time(curr_e, new_call):
    total = 0
    speed = 1/curr_e.floor_per_sec
    start_t = curr_e.start_time
    stop_t = curr_e.stop_time
    close_t = curr_e.close_time
    open_t = curr_e.open_time
    last_call = None
    for call in curr_e.call_list:
        total += close_t
        total += start_t
        total += abs(call.origin - call.destination)*speed
        total += stop_t
        total += open_t
        if last_call is None:
            last_call=call
        else:
            total += abs(last_call.destination - call.origin)*speed
            last_call=call
    """
    change a lot somehow
    """
    total /= 10

    total += close_t
    total += start_t
    total += abs(new_call.origin - new_call.destination) * speed
    total += stop_t
    total += open_t

    if last_call is None:
        last_call = new_call
    else:
        total += abs(last_call.destination - new_call.origin) * speed
    return total

"""
choosing an elevator for each call by data got from other functions 
and writes the results to the output file
"""
def sort_calls_algo(my_building, my_calls):
    f_amount = my_building.floors
    e_amount = my_building.elevator_num

    """ sorting some how here """

    times = []
    for i in range(e_amount):
        times.append(0)
    for call in my_calls:
        for curr_e in my_building.list_of_elevators:
            times[curr_e.number] = calc_total_wait_time(curr_e, call)

        min = times[0]
        index = 0
        for i in range(len(times)):
            if times[i]<min:
                index = i
                min = times[i]
        call.elevator_call = index
        my_building.list_of_elevators[index].call_list.append(call)

    print(my_building)
    write_file(csv_out, my_calls)

"""
thr main function - 
gets the building , calls and output files names
calls the open files function to open the files 
"""
def main(json_name, csv_name, csv_out):
    calls, building, elevators = open_files(json_name, csv_name)

    my_building = Building(building)
    calls_list = []
    calls_list_printable = []
    for i in calls:
        c = Call(i)
        calls_list.append(c)
        calls_list_printable.append(c.get_csv_format())
    elevators_list = []
    k = 0
    for i in elevators:
        c = Elevator(i)
        c.set_call_list([])
        c.section = k
        elevators_list.append(c)
        k += 1
    my_building.list_of_elevators = elevators_list
    sort_calls_algo(my_building, calls_list)

"""
definening the files we will work with
"""
if __name__ == '__main__':
    b_num = 5
    c_num = 'a'
    """
    sys,argv[0] returns file name 
    """
    json_name = sys.argv[1]
    csv_name = sys.argv[2]
    csv_out = sys.argv[3]
    main(json_name,csv_name,csv_out)
