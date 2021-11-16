from tkinter import *
import threading
import time
import json
import csv

colors4 = ["gray40", "gray26", "gray30", "gray10"]
colors = colors4


class StartPage:

    def __init__(self, master):
        global colors
        base = Frame(master)
        base.grid(row=0, column=0)
        self.b = base
        self.m = master
        self.up_frame = Frame(base, borderwidth=2, relief=FLAT, background=colors[3], width=301, height=30)
        self.up_frame.grid(row=0, column=0)
        Label(self.up_frame, text="Elevator Simulator", background=colors[3], font=("Helvetica", 12),
              foreground="white").place(x=85)
        self.down_frame = Frame(base, borderwidth=2, relief=RAISED, background=colors[0], width=301, height=471)
        self.down_frame.grid(row=2, column=0)

        Label(self.down_frame, text="csv Num", background=colors[0], font=("Helvetica", 10)).place(x=0, y=10)
        self.csv_name = Entry(self.down_frame, width=30, borderwidth=2, relief=GROOVE, font=("Helvetica", 8, "bold"))
        self.csv_name.place(x=72, y=10)
        Label(self.down_frame, text="json Num", background=colors[0], font=("Helvetica", 10)).place(x=0, y=40)
        self.json_name = Entry(self.down_frame, width=30, borderwidth=2, relief=GROOVE
                               , font=("Helvetica", 8, "bold"))
        self.json_name.place(x=72, y=40)

        send_data = Button(self.down_frame, text="START", command=lambda: self.move_page(base, master), borderwidth=1,
                        relief=GROOVE, width=10, background=colors[2])
        send_data.place(x=72, y=65)

        self.csv_name.bind("<Key>", self.focus1)
        self.json_name.bind("<Key>", self.focus2)

    def focus1(self, e):
        if e.char == "\r":
            self.json_name.focus()

    def focus2(self, e):
        if e.char == "\r":
            self.move_page(self.b, self.m)

    def move_page(self, base, master):
        global csv_name
        global json_name

        csv_num = self.csv_name.get()
        json_num = self.json_name.get()

        json_name = "./Ex1_input/Ex1_Buildings/B"+json_num+".json"
        csv_name = "./Ex1_out/Calls_"+csv_num+json_num+".csv"
        c, b, e = open_files(json_name, csv_name)
        base.destroy()
        MainPage(master, c, b, e)


class MainPage:

    def __init__(self, master, c, b, e):
        self.calls = c
        self.b_info = b
        self.e_list = e
        self.floors_max = self.b_info["_maxFloor"]
        self.floors_min = self.b_info["_minFloor"]
        self.e_num = len(self.e_list)
        global colors
        base = Frame(master)
        base.grid(row=0, column=0)
        self.kill = False
        self.b = base
        self.m = master
        self.up_frame = Frame(base, borderwidth=2, relief=FLAT, background=colors[3], width=801, height=30)
        self.up_frame.grid(row=0, column=0)
        Label(self.up_frame, text="Simulator main page", background=colors[3], font=("Helvetica", 12),
              foreground="white").place(x=85)
        self.down_frame = Frame(base, borderwidth=2, relief=RAISED, background=colors[0], width=801, height=600)
        self.down_frame.grid(row=2, column=0)

        start_b = Button(self.down_frame, text="START", command=lambda: self.start_sim(), borderwidth=1,
                        relief=GROOVE, width=10, background=colors[2])
        start_b.place(x=80, y=0)
        start_b = Button(self.down_frame, text="STOP", command=lambda: self.stop_sim(), borderwidth=1,
                         relief=GROOVE, width=10, background=colors[2])
        start_b.place(x=180, y=0)
        self.text = Text(self.down_frame)
        self.text.place(x=80, y=50)


        self.text.config(height=self.floors_max + abs(self.floors_min) + 1, width=self.e_num * 5 + 10)

    def build_arr(self, arr, w):
        tall = abs(self.floors_min - self.floors_max) + 1
        for i in range(tall):
            arr.append(["F "+str(self.floors_min + i)])

        counter = 0
        for i in arr:
            for j in range(len(self.e_list)):
                if counter == abs(self.floors_min) + w[j]:
                    i.append(" [|] ")
                else:
                    i.append(" ___ ")
            counter += 1

    def draw_arr(self, arr):
        stringy = ""
        for i in arr:
            for j in i:
                stringy += j
            stringy += "\n"
        return stringy

    def set_dests(self, d):
        for j in range(len(self.e_list)):
            d.append([])
        for call in self.calls:
            d[int(call[-1])].append(int(call[2]))
            d[int(call[-1])].append(int(call[3]))

    def show_screen(self):
        show_b = []
        where = []
        dests = []
        speeds = []
        self.set_dests(dests)

        for j in range(len(self.e_list)):
            speeds.append(self.e_list[j]["_speed"])
        for j in range(len(self.e_list)):
            where.append(0)
        self.build_arr(show_b, where)
        print(speeds)
        while not self.kill:
            self.text.delete('1.0', END)
            self.text.insert(END, self.draw_arr(show_b))
            for k in range(len(self.e_list)):
                show_b[int(where[k]) + abs(self.floors_min)][k+1] = " ___ "
            print(dests)
            for k in range(len(self.e_list)):
                if len(dests[k]) > 0:
                    if where[k] == dests[k][0]:
                        dests[k].pop(0)
                    else:
                        if where[k] < dests[k][0]:
                            where[k] = where[k]+speeds[k]
                            if where[k] > dests[k][0]:
                                where[k] = dests[k][0]
                        elif where[k] > dests[k][0]:
                            where[k] = where[k]-speeds[k]
                            if where[k] < dests[k][0]:
                                where[k] = dests[k][0]

            for k in range(len(self.e_list)):
                show_b[int(where[k]) + abs(self.floors_min)][k+1] = " [|] "
            print(where)
            time.sleep(0.05)

    def start_sim(self):
        if not self.kill:
            threading.Thread(target=lambda: self.show_screen()).start()
        else:
            self.kill = False

    def stop_sim(self):
        self.kill = True


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


json_name = "./Ex1_input/Ex1_Buildings/B1.json"
csv_name = "./Ex1_input/Ex1_Calls/Calls_a.csv"

if True:
    root = Tk()
    StartPage(root)
    root.mainloop()
