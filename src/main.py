#!/usr/bin/env python
import csv
import tkinter as tk
from tkinter import ttk

import threading
import sys
import Crossover_Operators as Operators
from tkinter import filedialog

cities = []
exit_thread = False
exit_success = False


class StdRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        if not exit_thread:
            self.widget.config(state=tk.NORMAL)
            self.widget.insert(tk.END, string)
            self.widget.see(tk.END)
            self.widget.config(state=tk.DISABLED)


class City(object):  # Object to store the cities
    province = ''
    city = ''
    latitude = 0.0
    longitude = 0.0

    def __init__(self, province, city, latitude, longitude):
        self.province = province
        self.city = city
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return self.province + ': ' + self.city


def execute_genetic(cross, mutate):
    if cross is 0 or mutate is 0:
        print('Please, select one Crossover opertator and one Mutation operator.\n')
    else:
        thread1 = threading.Thread(target=Operators.edge_crossover())
        thread1.start()

        thread2 = threading.Thread(target=Operators.order_crossover,
                                   args=([1, 2, 3, 4, 5, 6, 7, 8, 9], [9, 3, 7, 8, 2, 6, 5, 1, 4]))
        thread2.start()


def OpenFile(Frame):  # https://gist.github.com/Yagisanatode/0d1baad4e3a871587ab1
    name = filedialog.askopenfilename(initialdir="../src/",
                                      filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")),
                                      title="Choose a file.")
    print(name)

    # Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name, 'r') as UseFile:
            city_reader = csv.reader(UseFile, delimiter=';')
            next(city_reader)  # skip header
            cities[:] = []  # clear cities list
            for row in city_reader:
                city = City(row[0], row[1], row[2], row[3])
                cities.append(city)
                print(city)
        Frame.destroy()
        app = myFrame(Frame.master)
    except:
        print("No file")


class myFrame(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.initUI()
        self.pathWidget()
        sys.stdout = StdRedirector(self.textbox)

    def initUI(self):
        self.grid(padx=20, pady=20)
        cross = tk.IntVar()
        mutate = tk.IntVar()

        crosslabel = tk.Label(self, text='Crossover operators')
        r1 = tk.Radiobutton(self, text="Crossover", variable=cross, value=1, relief=tk.RIDGE, width=15)
        r2 = tk.Radiobutton(self, text="Order crossover", variable=cross, value=2, relief=tk.RIDGE, width=15)
        r3 = tk.Radiobutton(self, text="Edge crossover", variable=cross, value=3, relief=tk.RIDGE, width=15)
        mutatelabel = tk.Label(self, text='Mutation operators')
        r4 = tk.Radiobutton(self, text="Mutation", variable=mutate, value=1, relief=tk.RIDGE, width=15)
        r5 = tk.Radiobutton(self, text="Insert mutation", variable=mutate, value=2, relief=tk.RIDGE, width=15)
        r6 = tk.Radiobutton(self, text="Swap mutation", variable=mutate, value=3, relief=tk.RIDGE, width=15)
        r7 = tk.Radiobutton(self, text="Inverse mutation", variable=mutate, value=4, relief=tk.RIDGE, width=15)
        go = tk.Button(self, text="Go!", command=lambda: execute_genetic(cross.get(), mutate.get()))

        self.textbox = tk.Text(self, wrap='word', bg="black", fg="white", relief=tk.RIDGE)
        vertscroll = tk.Scrollbar(self)
        vertscroll.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=vertscroll.set)
        self.textbox.grid(column=1, row=0, rowspan=5)
        vertscroll.grid(column=2, row=0, rowspan=5, sticky=tk.N + tk.S)
        self.textbox.insert(tk.INSERT,
                            "Welcome to the GUI for TSP Genetic Algorithm. \nAuthor: Andrés López Albín. \nPlease, select one Crossover opertator and one Mutation operator.\n\n")
        self.textbox.config(state=tk.DISABLED)

        crosslabel.grid(row=0, column=6)
        r1.grid(row=1, column=6)
        r2.grid(row=2, column=6)
        r3.grid(row=3, column=6)
        mutatelabel.grid(row=0, column=7)
        r4.grid(row=1, column=7)
        r5.grid(row=2, column=7)
        r6.grid(row=3, column=7)
        r7.grid(row=4, column=7)
        go.grid(row=0, column=8)

        file = tk.Button(self, text="file", command=lambda: OpenFile(self))
        file.grid(row=1, column=8)

    def pathWidget(self):
        start_point_label = tk.Label(self, text='Start point')
        start_point_label.grid(row=0, column=4)

        box_value = tk.StringVar()
        box = ttk.Combobox(self, width=30, textvariable=box_value)
        box['values'] = cities
        box.grid(column=4, row=1)

        path_label = tk.Label(self, text='Cities to pass by')
        path_label.grid(row=2, column=4)

        # vsb = tk.Scrollbar(self, orient="vertical")
        # checkbuttons = tk.Text(self, width=30, height=15, yscrollcommand=vsb.set)
        #
        # vsb.config(command=checkbuttons.yview)
        # vsb.grid(column=5, row=3, rowspan=3, sticky=tk.N + tk.S)
        # checkbuttons.grid(column=4, row=3, rowspan=3)

        self.checkbuttons = tk.Text(self, width=30, height=15)
        vertscrollcheckbuttons = tk.Scrollbar(self)
        vertscrollcheckbuttons.config(command=self.checkbuttons.yview)
        self.checkbuttons.config(yscrollcommand=vertscrollcheckbuttons.set)
        self.checkbuttons.grid(column=4, row=3, rowspan=3)
        vertscrollcheckbuttons.grid(column=5, row=3, rowspan=3, sticky=tk.N + tk.S)
        for i in range(len(cities)):
            cb = tk.Checkbutton(self, text=cities[i].__str__())
            self.checkbuttons.window_create("end", window=cb)
            # self.checkbuttons.insert("end", cb)  # to force one checkbox per line
            self.checkbuttons.insert("end", "\n")  # to force one checkbox per line
        self.checkbuttons.config(state=tk.DISABLED)


class SelectFileView(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.grid(padx=20, pady=20)

        self.textbox = tk.Text(self, wrap='word', bg="black", fg="white", relief=tk.RIDGE)
        vertscroll = tk.Scrollbar(self)
        vertscroll.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=vertscroll.set)
        self.textbox.grid(column=1, row=0, rowspan=5)
        vertscroll.grid(column=2, row=0, rowspan=5, sticky=tk.N + tk.S)
        self.textbox.insert(tk.INSERT,
                            "Welcome to the GUI for TSP Genetic Algorithm. \nAuthor: Andrés López Albín. \nPlease, select one Crossover opertator and one Mutation operator.\n")
        self.textbox.config(state=tk.DISABLED)

        file = tk.Button(self, text="file", command=lambda: OpenFile(self))
        file.grid(row=1, column=6)

        sys.stdout = StdRedirector(self.textbox)


def main():
    root = tk.Tk()
    root.title("TSP Generic Algorithm")
    app = SelectFileView(root)
    root.mainloop()


if __name__ == '__main__':
    main()
