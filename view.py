import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from controller import AudioFileController

class View:
    def __init__(self):
        self.master = tk.Tk()
        self.create_widgets()
        self.tk_filepath = StringVar()
        self.status_msg = StringVar()
        self.audiofilecontroller = AudioFileController(self.tk_filepath.get())

    def create_widgets(self):
        # master is essentially the same as root in tkinter
        self.master.geometry('1000x700')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self.master, padding='5 5 5 5')
        self.mainframe.grid(row=0, column=0, sticky="NEWS")
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=1)

        self.load_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Choose File')
        self.load_file_frame.grid(column=0, row=0, sticky='NEW')
        self.load_file_frame.columnconfigure(0, weight=1)
        self.load_file_frame.rowconfigure(0, weight=1)

        choose_file_label = ttk.Label(self.load_file_frame, text='Please input file you would like to analyze:')
        choose_file_label.grid(column=0, row=0, columnspan=1, sticky='NEWS')

        self.choose_file_text = ttk.Entry(self.load_file_frame, width=70, textvariable=self.tk_filepath)
        self.choose_file_text.grid(column=0, row=1, sticky='NEWS')

        choose_file_button = ttk.Button(self.load_file_frame, text="Load/Browse",
                                        command=self.audiofilecontroller.get_file_path_with_window)
        choose_file_button.grid(row=2, column=0, sticky='W')

        self.data_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Data')
        self.data_file_frame.grid(column=0, row=2, sticky='NEW')
        self.data_file_frame.rowconfigure(1, weight=1)
        self.data_file_frame.columnconfigure(0, weight=1)
        #
        # show_plot = ttk.Button(self.data_file_frame, text='Plot', command=)
        # show_plot.grid(column=0, row=1, sticky='WN')
        #
        # show_time = ttk.Button(self.data_file_frame, text='Time', command=self.extracttime)
        # show_time.grid(column=0, row=2, sticky='WN')
        #
        # self.status_frame = ttk.Frame(self.master, relief='sunken', padding='2 2 2 2')
        # self.status_frame.grid(row=1, column=0, sticky='EWS')
        # self._status_msg.set('')
        # status = ttk.Label(self.status_frame, textvariable=self._status_msg, anchor=W)
        # status.grid(row=0, column=0, sticky='EW')
        #
        # self.extra_data_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Audio Data')
        # self.extra_data_file_frame.grid(column=0, row=1, sticky='NEW')
        # self.extra_data_file_frame.rowconfigure(1, weight=1)
        # self.extra_data_file_frame.columnconfigure(0, weight=1)
        #
        # model.highest_resonance.set(f'Frequency of Highest Amplitude: ')
        # model.lowest_resonance.set(f'Frequency of Lowest Amplitude: ')
        #
        # self.extra_data_highest_resonance_data = ttk.Label(self.extra_data_file_frame,
        #                                                    textvariable=model.highest_resonance)
        # self.extra_data_highest_resonance_data.grid(row=0, column=0, sticky='NW')
        # self.extra_data_lowest_resonance_data = ttk.Label(self.extra_data_file_frame,
        #                                                   textvariable=model.lowest_resonance)
        # self.extra_data_lowest_resonance_data.grid(row=1, column=0, sticky='NW')

    def sb(self, msg):
        self.status_msg.set(msg)


if __name__ == "__main__":
    root = tk.Tk()
    model = Model()
    view = View(root, None)  # The controller will be set later
    model.view = view  # Set the view reference in the model
    root.mainloop()
