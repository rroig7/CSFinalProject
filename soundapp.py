import os.path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from pathlib import Path
from pydub import AudioSegment
import wave
import matplotlib.pyplot as plt
import matplotlib.figure as Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk)
import numpy as np


#returns raw audio data from wav file
def getwavdata(audio_file):
    wav_file = wave.open(audio_file, 'rb')
    audio_data = wav_file.readframes(wav_file.getnframes())
    return np.frombuffer(audio_data, np.int16)


def getfilepath():
    _filepath.set(tk.filedialog.askopenfilename())


def loadfilepath():
    try:
        if str(_choose_file_textbox.get()) != '':
            _filepath.set(_choose_file_textbox.get())
            sb(f'File path set as \"{_filepath.get()}\"')
        else:
            sb('File path cannot be empty.')
    except:
        sb('Error setting specified path.')


# checks if file is in wav format

def sb(msg):
    _status_msg.set(msg)

# Not finished, not sure if this function works or not
def converttowav(input_file):
    # Check if the file exists
    if not os.path.isfile(input_file):
        print(f"Error: File {input_file} not found.")
        return

    # Check if the file has a supported audio extension
    supported_extensions = ['.mp3', '.wav', '.ogg']  # audio extensions
    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension not in supported_extensions:
        print(f"Error: Unsupported file format ({file_extension}). Supported formats are {supported_extensions}.")
        return

    try:
        # Attempt to load and convert the audio file
        audiofile = AudioSegment.from_file(input_file, format='wav')
        print(f"Conversion successful. WAV file saved as {audiofile}")
        return audiofile
    except Exception as e:
        print(f"Error during conversion: {e}")

def createplot():
    data = getwavdata(_filepath.get())

    fig, ax = plt.subplots(figsize=(5,2))
    ax.plot(data)
    ax.set_title('Signal Graph')

    canvas = FigureCanvasTkAgg(fig, master=_data_file_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=0)

if __name__ == "__main__":  # execute logic if run directly
    _root = Tk()  # instantiate instance of Tk class
    _root.title('Sound App')
    _root.geometry('600x500')
    _root.rowconfigure(0, weight=1)
    _root.columnconfigure(0, weight=1)
    #_root.resizable(False, False)
    _mainframe = ttk.Frame(_root, padding='5 5 5 5 ')  # root is parent of frame
    _mainframe.grid(row=0, column=0, sticky=("E", "W", "N", "S"))
    _mainframe.rowconfigure(0, weight=1)
    _mainframe.columnconfigure(0, weight=1)
    # placed on first row,col of parent
    # frame can extend itself in all cardinal directions



    _load_file_frame = ttk.LabelFrame(
        _mainframe,
        padding='5 5 5 5',
        text='Choose File'
    )
    _load_file_frame.grid(
        column=0,
        row=0,
        sticky='new'
    )
    _load_file_frame.rowconfigure(0, weight=1)
    _load_file_frame.columnconfigure(0, weight=1)

    _filepath = StringVar()

    _choose_file_label = ttk.Label(
        _load_file_frame,
        text='Please input the path file you would like to analyze: ',
    )
    _choose_file_label.grid(
        column=0,
        row=0,
        columnspan=1,
        sticky='W'
    )

    _choose_file_textbox = ttk.Entry(
        _load_file_frame,
        width=70,
        textvariable=_filepath
    )
    _choose_file_textbox.grid(
        column=0,
        row=1,
        sticky='ew'
    )

    _choose_file_button = ttk.Button(
        _load_file_frame,
        text='Browse',
        command=getfilepath
    )
    _choose_file_button.grid(
        column=0,
        row=2,
        sticky='W'
    )
    _load_file_button = ttk.Button(
        _load_file_frame,
        text='Load',
        command=loadfilepath
    )
    _load_file_button.grid(
        column=2,
        row=1,
        sticky='E',
    )

    _data_file_frame = ttk.LabelFrame(
        _mainframe,
        padding='5 5 5 5',
        text='Data'
    )
    _data_file_frame.grid(
        column=0,
        row=1,
        sticky='new'
    )
    _data_file_frame.rowconfigure(1, weight=1)
    _data_file_frame.columnconfigure(0, weight=1)

    _plot_show = ttk.Button(
        _data_file_frame,
        text='Plot',
        command=createplot
    )
    _plot_show.grid(
        column=0,
        row=1
    )

    _status_frame = ttk.Frame(
        _root, relief='sunken', padding='2 2 2 2')
    _status_frame.grid(row=1, column=0, sticky=("E", "W", "S"))
    _status_msg = StringVar() # need modified when update status text
    _status_msg.set('')
    _status= ttk.Label(
        _status_frame, textvariable=_status_msg, anchor=W)
    _status.grid(row=0, column=0, sticky=(E, W))

    #_root.bind("<Configure>", on_resize)
    _root.mainloop()  # listens for events, blocks any code that comes after it




