#!/usr/bin/env python
import csv
import sys
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import numpy as np

import Crossover_Operators as Operators
import GA_algorithm as GA

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


def execute_genetic(Frame, cross, mutate, start_point, ngen, chr_size, prob_mutation, cross_ratio):
    chosen_path_index = Frame.listbox.curselection()
    if cross is 0 or mutate is 0 or len(chosen_path_index) is 0 or start_point is None:
        print('Please, select one Crossover opertator and one Mutation operator.\n')
    else:
        print('The path must begin and finish at:', cities[start_point])
        print('The path must include the following cities:')
        chosen_cities = []
        for city in chosen_path_index:
            print(cities[city])
            if cities[city] is not cities[start_point]:  # we avoid having the starting point on the path
                chosen_cities.append(cities[city])

        # genes, decode, mutation, crossover, start_point
        p_genetic = GA.Problem_Genetic(chosen_cities, 'min', cross, mutate, cities[start_point])

        # problem_genetic, ngen, size, ratio_cross, prob_mutate, opt genetic_algorithm_t(sq_gen,3,min,20,10,0.7,0.1)
        thread1 = threading.Thread(
            target=GA.genetic_algorithm_main(p_genetic, ngen, chr_size, cross_ratio, prob_mutation, min))
        thread1.start()


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
                city = City(row[8], row[0], row[2], row[3])
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
        self.start_point_value = tk.StringVar()
        self.box = ttk.Combobox(self, width=30)
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
        go = tk.Button(self, text="Go!",
                       command=lambda: execute_genetic(self, cross.get(), mutate.get(), self.box.current(),
                                                       generations.current(), chr_size.current(), mutation.get(),
                                                       cross_ratio.get()))

        self.textbox = tk.Text(self, wrap='word', bg="black", fg="white", relief=tk.RIDGE)
        vertscroll = tk.Scrollbar(self)
        vertscroll.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=vertscroll.set)
        self.textbox.grid(column=1, row=0, rowspan=9)
        vertscroll.grid(column=2, row=0, rowspan=9, sticky=tk.N + tk.S)
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
        go.grid(row=8, column=8)

        file = tk.Button(self, text="file", command=lambda: OpenFile(self))
        file.grid(row=9, column=8)

        generations_label = tk.Label(self, text='Number of generations')
        generations_label.grid(row=0, column=8)

        generations = ttk.Combobox(self, width=30)
        generations['values'] = list(range(20))
        generations.current(3)
        generations.grid(column=8, row=1)

        chr_size_label = tk.Label(self, text='Chromosoma size')
        chr_size_label.grid(row=2, column=8)

        chr_size = ttk.Combobox(self, width=30)
        chr_size['values'] = list(range(20))
        chr_size.current(10)
        chr_size.grid(column=8, row=3)

        mutation_label = tk.Label(self, text='Mutation probability')
        mutation_label.grid(row=4, column=8)

        mutation = ttk.Combobox(self, width=30)
        mutation['values'] = (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
        mutation.current(2)
        mutation.grid(column=8, row=5)

        cross_ratio_label = tk.Label(self, text='Crossover probability')
        cross_ratio_label.grid(row=6, column=8)

        cross_ratio = ttk.Combobox(self, width=30)
        cross_ratio['values'] = (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
        cross_ratio.current(7)
        cross_ratio.grid(column=8, row=7)

    def pathWidget(self):
        start_point_label = tk.Label(self, text='Start point')
        start_point_label.grid(row=0, column=4)

        self.box['values'] = cities
        self.box.grid(column=4, row=1)

        path_label = tk.Label(self, text='Cities to pass by')
        path_label.grid(row=3, column=4)

        # Crear una barra de deslizamiento con orientación vertical.
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        # Vincularla con la lista.
        self.listbox = tk.Listbox(self, width=30, height=15, yscrollcommand=self.scrollbar.set, selectmode=tk.EXTENDED)

        # Insertar 20 elementos.
        for i in range(len(cities)):
            self.listbox.insert(tk.END, cities[i].__str__())

            self.scrollbar.config(command=self.listbox.yview)
        # Ubicarla a la derecha.
        self.scrollbar.grid(column=5, row=4, rowspan=5, sticky=tk.N + tk.S)
        self.listbox.grid(column=4, row=4, rowspan=5)


        # self.v = tk.StringVar()
        # self.checkbuttons = tk.Text(self, width=30, height=15)
        # vertscrollcheckbuttons = tk.Scrollbar(self)
        # vertscrollcheckbuttons.config(command=self.checkbuttons.yview)
        # self.checkbuttons.config(yscrollcommand=vertscrollcheckbuttons.set)
        # self.checkbuttons.grid(column=4, row=3, rowspan=3)
        # vertscrollcheckbuttons.grid(column=5, row=3, rowspan=3, sticky=tk.N + tk.S)
        # cb = []
        # for i in range(len(cities)):
        #     v = tk.StringVar()
        #     cb.append(tk.Checkbutton(self, text=cities[i].__str__(), variable=v))
        #     cb[-1].v = v
        #     self.checkbuttons.window_create("end", window=cb)
        #     # self.checkbuttons.insert("end", cb)  # to force one checkbox per line
        #     self.checkbuttons.insert("end", "\n")  # to force one checkbox per line
        # self.checkbuttons.config(state=tk.DISABLED)


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
        self.textbox.grid(column=1, row=0, rowspan=9)
        vertscroll.grid(column=2, row=0, rowspan=9, sticky=tk.N + tk.S)
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
