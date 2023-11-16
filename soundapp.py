import os.path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from pathlib import Path
from pydub import AudioSegment
import wave
import matplotlib.pyplot as plt
import matplotlib.figure as Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class AudioAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Analyzer")
        self.mainframe = None
        self.load_file_frame = None
        self.status_frame = None

        self._filepath = StringVar()
        self._status_msg = StringVar()

        self.create_widgets()

    def create_widgets(self):
        # master is essentially the same as root in tkinter
        self.master.geometry('800x500')
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

        choose_file_text = ttk.Entry(self.load_file_frame, width=70, textvariable=self._filepath)
        choose_file_text.grid(column=0, row=1, sticky='NEWS')

        choose_file_button = ttk.Button(self.load_file_frame, text="Browse", command=self.getfilepath)
        choose_file_button.grid(row=2, column=0, sticky='W')

        load_file_button = ttk.Button(self.load_file_frame, text="Load", command=self.loadfilepath)
        load_file_button.grid(row=1, column=1, sticky='E')

        data_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Data')
        data_file_frame.grid(column=0, row=1, sticky='NEW')
        data_file_frame.rowconfigure(1, weight=1)
        data_file_frame.columnconfigure(0, weight=1)

        show_plot = ttk.Button(data_file_frame, text='Plot', command=self.createplot)
        show_plot.grid(column=0, row=1, sticky='WN')

        show_data = ttk.Button(data_file_frame, text='Data', command=self.extractdata)
        show_data.grid(column=0, row=2, sticky='WN')

        self.status_frame = ttk.Frame(self.master, relief='sunken', padding='2 2 2 2')
        self.status_frame.grid(row=1, column=0, sticky='EWS')
        self._status_msg.set('')
        status = ttk.Label(self.status_frame, textvariable=self._status_msg, anchor=W)
        status.grid(row=0, column=0, sticky='EW')

    def getfilepath(self):
        self._filepath.set(tk.filedialog.askopenfilename())

    def loadfilepath(self):
        try:
            if str(self._choose_file_textbox.get()) != '':
                self._filepath.set(self._choose_file_textbox.get())
                self.sb(f'File path set as \"{self._filepath.get()}\"')
            else:
                self.sb('File path cannot be empty.')
        except:
            self.sb('Error setting specified path.')

    def sb(self, msg):
        self._status_msg.set(msg)

    def converttowav(self, audio_file_path):
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

        return wav_audio

    def extractdata(self):
        wav_audio = converttowav(_filepath.get())

        raw_data = np.frombuffer(wav_audio.raw_data, dtype=np.int16)

        time_duration = len(raw_data) / wav_audio.frame_rate
        wav_audio_time_length = np.linspace(0, time_duration, len(raw_data))

        print(wav_audio_time_length)

        time_min = time_duration // 60
        time_sec = round(time_duration % (24 * 3600), 2)

        time_string = f'{time_min} minutes {time_sec} seconds'
        print(time_string)

    def createplot(self):

        data = np.frombuffer(converttowav(_filepath.get()).raw_data, dtype=np.int16)

        fig, ax = plt.subplots(figsize=(5, 2))
        ax.plot(data)
        ax.set_title('Waveform of ' + _filepath.get().split('/')[-1])

        canvas = FigureCanvasTkAgg(fig, master=_data_file_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=3)


if __name__ == "__main__":
    root = Tk()
    app = AudioAnalyzerApp(root)
    root.mainloop()
