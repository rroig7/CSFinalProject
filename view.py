import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from controller import Controller
from model import Model

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None
        self.status_msg = StringVar()

        # create widgets
        self.master.geometry('1000x700')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self.master, padding='5 5 5 5')
        self.mainframe.grid(row=0, column=0, sticky="NEWS")
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=1)

        # filepath entry
        self.filepath_var = tk.StringVar()
        self.load_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Choose File')
        self.load_file_frame.grid(column=0, row=0, sticky='NEW')
        self.load_file_frame.columnconfigure(0, weight=1)
        self.load_file_frame.rowconfigure(0, weight=1)

        choose_file_label = ttk.Label(self.load_file_frame, text='Please input file you would like to analyze:')
        choose_file_label.grid(column=0, row=0, columnspan=1, sticky='NEWS')

        self.choose_file_text = ttk.Entry(self.load_file_frame, width=70, textvariable=self.filepath_var)
        self.choose_file_text.grid(column=0, row=1, sticky='NEWS')

        choose_file_button = ttk.Button(self.load_file_frame, text="Browse", command=self.getfilepath)
        choose_file_button.grid(row=2, column=0, sticky='W')

        load_file_button = ttk.Button(self.load_file_frame, text="Load", command=self.load_button_clicked)
        load_file_button.grid(row=1, column=1, sticky='E')

        self.data_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Data')
        self.data_file_frame.grid(column=0, row=2, sticky='NEW')
        self.data_file_frame.rowconfigure(1, weight=1)
        self.data_file_frame.columnconfigure(0, weight=1)

        show_plot = ttk.Button(self.data_file_frame, text='Plot', command=self.create_plot_call_to_controller)
        show_plot.grid(column=0, row=1, sticky='WN')

        # show_time = ttk.Button(self.data_file_frame, text='Time', command=self.extracttime)
        # show_time.grid(column=0, row=2, sticky='WN')
        #
        self.status_frame = ttk.Frame(self.master, relief='sunken', padding='2 2 2 2')
        self.status_frame.grid(row=1, column=0, sticky='EWS')
        self.status_msg.set('')
        status = ttk.Label(self.status_frame, textvariable=self.status_msg, anchor=W)
        status.grid(row=0, column=0, sticky='EW')

        # self.extra_data_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Audio Data')
        # self.extra_data_file_frame.grid(column=0, row=1, sticky='NEW')
        # self.extra_data_file_frame.rowconfigure(1, weight=1)
        # self.extra_data_file_frame.columnconfigure(0, weight=1)
        #
        # self.highest_resonance.set(f'Frequency of Highest Amplitude: ')
        #
        # self.extra_data_highest_resonance_data = ttk.Label(self.extra_data_file_frame,
        #                                                    textvariable=self.highest_resonance)
        # self.extra_data_highest_resonance_data.grid(row=0, column=0, sticky='NW')
        #

    def set_controller(self, controller):
        self.controller = controller
    def getfilepath(self):
        self.filepath_var.set(tk.filedialog.askopenfilename())

    def load_button_clicked(self):
        if self.controller:
            self.controller.save(self.filepath_var.get())

    def create_plot_call_to_controller(self):
        self.controller.model.create_plot()

    def sb(self, msg):
        self.status_msg.set(msg)