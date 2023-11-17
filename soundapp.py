import datetime
import os.path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from pathlib import Path
from pydub import AudioSegment
import wave
import matplotlib.pyplot as plt
import matplotlib.figure as Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np

# returns raw audio data from wav file
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
'''def converttowav(input_file):
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
'''


# This works! It extracts raw audio data from any audio file type, then returns it as wav
def converttowav(audio_file_path):
    audio_file = AudioSegment.from_file(
        audio_file_path,
        format=os.path.splitext(audio_file_path)[-1].strip('.')
    )

    wav_data = audio_file.raw_data
    wav_audio = AudioSegment(
        wav_data,
        frame_rate=audio_file.frame_rate,
        sample_width=audio_file.sample_width,
        channels=audio_file.channels
    )
    # sets channels to 1 in case of multiple channels
    wav_audio.set_channels(1)

    return wav_audio


def extractdata():
    wav_audio = converttowav(_filepath.get())

    raw_data = np.frombuffer(wav_audio.raw_data, dtype=np.int16)

    time_duration = len(raw_data) / wav_audio.frame_rate
    wav_audio_time_length = np.linspace(0, time_duration, len(raw_data))

    time_min = time_duration // 60
    time_sec = round(time_duration % (24 * 3600), 2)

    time_string = f'{time_min} minutes {time_sec} seconds'
    print(time_string)
    print(getmetadata(_filepath.get()))


def createplot():

    # data = getwavdata(_filepath.get())

    data = np.frombuffer(converttowav(_filepath.get()).raw_data, dtype=np.int16)

    fig, ax = plt.subplots(figsize=(5, 2))
    ax.plot(data)
    ax.set_title('Waveform of ' + _filepath.get().split('/')[-1])

    canvas = FigureCanvasTkAgg(fig, master=_data_file_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=3)


def getmetadata(file_path):

    metadata = {
        'Title': file_path.split('/')[-1],
        'Latest Modification Time': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)),
        'File Creation Date': datetime.datetime.fromtimestamp(os.path.getctime(file_path)).date(),
        'File Size': os.path.getsize(file_path)
    }

    return metadata

if __name__ == "__main__":  # execute logic if run directly
    _root = Tk()  # instantiate instance of Tk class
    _root.title('Sound App')
    _root.geometry('800x500')
    _root.rowconfigure(0, weight=1)
    _root.columnconfigure(0, weight=1)
    # _root.resizable(False, False)
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
        text='Please input the path of the file you wish to analyze:',
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
        row=1,
        sticky='wn'
    )
    _data_show = ttk.Button(
        _data_file_frame,
        text='Data',
        command=extractdata
    )
    _data_show.grid(
        column=0,
        row=2,
        sticky='nw'
    )

    _status_frame = ttk.Frame(
        _root, relief='sunken', padding='2 2 2 2')
    _status_frame.grid(row=1, column=0, sticky=("E", "W", "S"))
    _status_msg = StringVar()  # need modified when update status text
    _status_msg.set('')
    _status = ttk.Label(
        _status_frame, textvariable=_status_msg, anchor=W)
    _status.grid(row=0, column=0, sticky=(E, W))

    # _root.bind("<Configure>", on_resize)
    _root.mainloop()  # listens for events, blocks any code that comes after it
