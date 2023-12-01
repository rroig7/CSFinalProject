import datetime
import os.path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from pathlib import Path
from pydub import AudioSegment
import wave
import matplotlib.pyplot as plt
from pydub.utils import mediainfo
from scipy.fft import fft
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np

class AudioAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Analyzer")
        self.mainframe = None
        self.load_file_frame = None
        self.status_frame = None
        self.choose_file_text = None
        self.wav_audio = None
        self.data_file_frame = None
        self.raw_data = None
        self.frame_amount = None
        self.highest_resonance = StringVar()
        self.lowest_resonance = StringVar()

        self._filepath = StringVar()
        self.str_filepath = None
        self._status_msg = StringVar()

        self.create_widgets()

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

        self.choose_file_text = ttk.Entry(self.load_file_frame, width=70, textvariable=self._filepath)
        self.choose_file_text.grid(column=0, row=1, sticky='NEWS')

        choose_file_button = ttk.Button(self.load_file_frame, text="Browse", command=self.getfilepath)
        choose_file_button.grid(row=2, column=0, sticky='W')

        load_file_button = ttk.Button(self.load_file_frame, text="Load", command=self.loadfilepath)
        load_file_button.grid(row=1, column=1, sticky='E')

        self.data_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Data')
        self.data_file_frame.grid(column=0, row=2, sticky='NEW')
        self.data_file_frame.rowconfigure(1, weight=1)
        self.data_file_frame.columnconfigure(0, weight=1)

        show_plot = ttk.Button(self.data_file_frame, text='Plot', command=self.createplot)
        show_plot.grid(column=0, row=1, sticky='WN')

        show_time = ttk.Button(self.data_file_frame, text='Time', command=self.extracttime)
        show_time.grid(column=0, row=2, sticky='WN')

        self.status_frame = ttk.Frame(self.master, relief='sunken', padding='2 2 2 2')
        self.status_frame.grid(row=1, column=0, sticky='EWS')
        self._status_msg.set('')
        status = ttk.Label(self.status_frame, textvariable=self._status_msg, anchor=W)
        status.grid(row=0, column=0, sticky='EW')

        self.extra_data_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Audio Data')
        self.extra_data_file_frame.grid(column=0, row=1, sticky='NEW')
        self.extra_data_file_frame.rowconfigure(1, weight=1)
        self.extra_data_file_frame.columnconfigure(0, weight=1)

        self.highest_resonance.set(f'Frequency of Highest Amplitude: ')
        self.lowest_resonance.set(f'Frequency of Lowest Amplitude: ')

        self.extra_data_highest_resonance_data = ttk.Label(self.extra_data_file_frame, textvariable=self.highest_resonance)
        self.extra_data_highest_resonance_data.grid(row=0, column=0, sticky='NW')
        self.extra_data_lowest_resonance_data = ttk.Label(self.extra_data_file_frame, textvariable=self.lowest_resonance)
        self.extra_data_lowest_resonance_data.grid(row=1, column=0, sticky='NW')

    def getwavdata(self,audio_file):
        wav_file = wave.open(audio_file, 'rb')
        audio_data = wav_file.readframes(wav_file.getnframes())
        return np.frombuffer(audio_data, np.int16)

    def getfilepath(self):
        self._filepath.set(tk.filedialog.askopenfilename())

    def loadfilepath(self):
        try:
            if str(self.choose_file_text.get()) != '':
                self._filepath.set(self.choose_file_text.get())
                self.sb(f'File path set as \"{self._filepath.get()}\"')
                self.converttowav(self._filepath.get())
            else:
                self.sb('File path cannot be empty.')
        except Exception as e:
            self.sb(f'The error is {e}')

    def sb(self, msg):
        self._status_msg.set(msg)

    def converttowav(self, audio_file_path):
        if not os.path.isfile(audio_file_path):
            self.sb(f"Error: File {audio_file_path} not found.")
            return

        supported_extensions = ['.mp3', '.wav', '.ogg']  # audio extensions
        file_extension = os.path.splitext(audio_file_path)[1].lower()

        if file_extension not in supported_extensions:
            self.sb(f"Error: Unsupported file format ({file_extension}). Supported formats are {supported_extensions}.")
            return
        else:
            try:
                audio_file = AudioSegment.from_file(
                    audio_file_path,
                    format=os.path.splitext(audio_file_path)[-1].strip('.')
                )

                wav_data = audio_file.raw_data
                self.wav_audio = AudioSegment(
                    wav_data,
                    frame_rate=audio_file.frame_rate,
                    sample_width=audio_file.sample_width,
                    channels=audio_file.channels
                )
                self.frame_amount = len(self.wav_audio.get_array_of_samples())
                self.wav_audio.set_channels(1)
                self.raw_data = np.frombuffer(self.wav_audio.raw_data, dtype=np.int16)
                self.gethighestresonance()
            except Exception as e:
                self.sb(f"Error during conversion: {e}")

    def extracttime(self):
        if self.wav_audio is not None:
            time_duration = len(self.wav_audio)/1000
            #wav_audio_time_length = np.linspace(0, time_duration, len(self.raw_data))

            wav_audio_time_length = self.frame_amount / self.wav_audio.frame_rate

            time_min = time_duration // 60
            time_sec = round(time_duration % (24 * 3600), 2)

            time_string = f'{time_min} minutes {time_sec} seconds'
            self.sb(f"Time is: {time_string}")

            # print(mediainfo(self._filepath.get()))
        else:
            self.sb(f'Make sure to press load')

    def createplot(self):
        if self.wav_audio is not None:
            # Calculate time values
            time_values = np.arange(len(self.raw_data)) / self.wav_audio.frame_rate
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(time_values, self.raw_data)
            ax.set_title('Waveform of ' + self._filepath.get().split('/')[-1])
            ax.set_xlabel('Time (seconds)')
            ax.set_ylabel('Amplitude')

            canvas = FigureCanvasTkAgg(fig, master=self.data_file_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=0, row=3)
        else:
            self.sb(f'Make sure to press load')

    def gethighestresonance(self):
        samples = np.array(self.wav_audio.get_array_of_samples())

        fft_result = np.fft.fft(samples)

        frequencies = np.fft.fftfreq(len(fft_result), d=1/self.wav_audio.frame_rate)

        highest_amplitude_index = np.argmax(np.abs(fft_result))
        highest_frequency = frequencies[highest_amplitude_index]

        self.highest_resonance.set(f'Frequency of Highest Amplitude: {round(highest_frequency, 2)}')
        self.lowest_resonance.set(f'Frequency of Lowest Amplitude: {round(abs(frequencies).min(), 2)}')





if __name__ == "__main__":
    root = Tk()
    app = AudioAnalyzerApp(root)
    root.mainloop()
