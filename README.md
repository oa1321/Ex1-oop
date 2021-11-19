
# Ex1 - offline elevator algorithm 

in this project we will use an offline algorithm to allocate an elevators
to calls as fast as possibale


## Authors

- [@oa1321](https://www.github.com/oa1321) 213101637
- [@shayperetz6](https://github.com/shayperetz6) 203464870


## Reference
this are 3 articles that used to understand the problem and her possible 
solution 

- https://www.geeksforgeeks.org/scan-elevator-disk-scheduling-algorithms/
- https://www.popularmechanics.com/technology/infrastructure/a20986/the-hidden-science-of-elevators/
- http://www.diva-portal.org/smash/get/diva2:812034/FULLTEXT01.pdf

## The Problem Space
the problem in this case is this: we have a building with a certin amount of floors
and elevators, pepole in the building want to move from floor to floor by using the elevators
,our elevators are "smart elevators" ' which meens that every floor has pad that you enter there to where you want to go
and an elevator is allocated to your call inside the elevator you cant enter floor number to go to 
.

we need to build "offline algorithm" which meens that we get all the call in the building at once
and not one by one.
the algorithm will need to give each call an elevator that will handle the call while keeping
the wait time of each call as low as possible.
## The Algorithm

the Algorithm will work like this:

1) get the call and the building data
2) go trough each call and do next steps
3) calculate and save the time of each elevator to do all the call it have untill now
4) to each elevator add the time to do this call form the last call destntion
5) choose the one with the lowest time and add the call to his least of calls
6) move to next call


## Classes 
to make it easy to work with the data we got we will make 3 new Class.

Call - gets the call data(an array from the file)
the class fields:

    raw data = the array we got.
    time = the time we got the call in sec.
    origin = the floor wich we got the call.
    destination = the destination floor.
    state = not importent.
    elevator_call = the elevator that will handle the call.

Elevator - gets a dictionary with the elevator data
the class fields:

    elevator_raw_data = the dict we got
    number = the elevator index in the building
    floor_per_sec = the speed of the elevator in floor per sec format
    min_floor = the lowest floor in the building
    max_floor = the highest floor in the building
    close_time = time it takes to close the elevator
    open_time = time it takes to open the elevator
    start_time = time it takes to reach max speed for the elevator
    stop_time = time it takes to stop the elevator
    call_list = the list of calls the elevator handels

Building - gets a dictionary with the building data
the class fields:

    min_floor = the lowest floor in the building   
    max_floor = the highest floor in the building
    elevator_num = the amount of elevator in the building
    list_of_elevators = a list containing all the elevators in the building(as objects)
    building_raw_data = the dictionary we got 
    floors = the amount of floors in the building
## GUI - Showing Elevator Program
in the git we have the file new_emulator
by ruuing this Program you will be abble to see the 
Elevators moving according to the csv file

the video - https://www.youtube.com/watch?v=cA7X5P7OgZg

HOW TO USE?
- run the Program(required python and some liberies)
- enter the call file you used(a,b,c,d)
- enter the building number you used(1,2,3,4,5)
- the Program is looking for a file in this format
json_name = "./Ex1_input/Ex1_Buildings/B(number).json"

csv_name = "./Ex1_input/Ex1_Output/Calls_(call number+Building number).csv"

example for entering a , 1 the program will look for the files:

* json_name = "./Ex1_input/Ex1_Buildings/B1.json"

* csv_name = "./Ex1_input/Ex1_Output/Calls_a1.csv"
if the program finds the files you will move to a new screen with 2 buttons 
START and STOP simply press start and you will see the Elevators start to move