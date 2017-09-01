#!/usr/bin/env python
import tkinter as tk

import threading
import os
import sys
import Crossover_Operators as Operators


def execute_genetic(myframe, cross, mutate):
    if cross is 0 or mutate is 0:
        print('Please, select one Crossover opertator and one Mutation operator.\n')
    else:
        thread1 = threading.Thread(target=Operators.edge_crossover())
        thread1.start()

        thread2 = threading.Thread(target=Operators.order_crossover,
                                   args=([1, 2, 3, 4, 5, 6, 7, 8, 9], [9, 3, 7, 8, 2, 6, 5, 1, 4]))
        thread2.start()


exit_thread = False
exit_success = False


class StdRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        if not exit_thread:
            self.widget.config(state=tk.NORMAL)
            self.widget.insert(tk.END, string + '\n')
            self.widget.see(tk.END)
            self.widget.config(state=tk.DISABLED)


class myFrame(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.initUI()

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
        quit1 = tk.Button(self, text="Go!", command=lambda: execute_genetic(self, cross.get(), mutate.get()))

        self.textbox = tk.Text(self, wrap='word', bg="black", fg="white", relief=tk.RIDGE)
        vertscroll = tk.Scrollbar(self)
        vertscroll.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=vertscroll.set)
        self.textbox.grid(column=1, row=0, rowspan=5)
        vertscroll.grid(column=2, row=0, rowspan=5, sticky=tk.N + tk.S)
        self.textbox.insert(tk.INSERT,
                            "Welcome to the GUI for TSP Genetic Algorithm. \nAuthor: Andrés López Albín. \nPlease, select one Crossover opertator and one Mutation operator.\n")
        self.textbox.config(state=tk.DISABLED)

        crosslabel.grid(row=0, column=4)
        r1.grid(row=1, column=4)
        r2.grid(row=2, column=4)
        r3.grid(row=3, column=4)
        mutatelabel.grid(row=0, column=5)
        r4.grid(row=1, column=5)
        r5.grid(row=2, column=5)
        r6.grid(row=3, column=5)
        r7.grid(row=4, column=5)
        quit1.grid(row=0, column=6)

        sys.stdout = StdRedirector(self.textbox)


def main():
    root = tk.Tk()
    root.title("TSP Generic Algorithm")
    app = myFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
