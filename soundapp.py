import datetime
import os.path
import scipy
from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from matplotlib.figure import Figure
from pydub import AudioSegment
import wave
import matplotlib.pyplot as plt
from pydub.utils import mediainfo
from scipy.fft import fft
from scipy.signal import welch
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
        self.RT60values = None
        self.count = 0
        self.RT60values = {1: None, 2: None, 3: None}
        self.frame_amount = None
        self.highest_resonance = StringVar()

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
        self.data_file_frame.grid(column=0, row=1, sticky='NEW')
        self.data_file_frame.rowconfigure(1, weight=1)
        self.data_file_frame.columnconfigure(0, weight=1)

        show_plot = ttk.Button(self.data_file_frame, text='Plot Waveform', command=self.createplot)
        show_plot.grid(column=0, row=2, sticky='WN')

        show_time = ttk.Button(self.data_file_frame, text='Time', command=self.extracttime)
        show_time.grid(column=0, row=3, sticky='WN')

        show_plot2 = ttk.Button(self.data_file_frame, text='Resonant frequency ', command=self.PlotFrequency)
        show_plot2.grid(column=0, row=4, sticky='WN')

        show_plot3 = ttk.Button(self.data_file_frame, text='RT60 plot', command=self.RT60)
        show_plot3.grid(column=0, row=5, sticky='WN')

        show_plot3 = ttk.Button(self.data_file_frame, text='Frequency and Amplitude', command=self.Frequency)
        show_plot3.grid(column=0, row=6, sticky='WN')

        show_plot3 = ttk.Button(self.data_file_frame, text='RT60 Average', command=self.RT60avg)
        show_plot3.grid(column=0, row=7, sticky='WN')

        self.status_frame = ttk.Frame(self.master, relief='sunken', padding='2 2 2 2')
        self.status_frame.grid(row=1, column=0, sticky='EWS')
        self._status_msg.set('')
        status = ttk.Label(self.status_frame, textvariable=self._status_msg, anchor=W)
        status.grid(row=0, column=0, sticky='EW')

        self.highest_resonance.set('')



    def getwavdata(self, audio_file):
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

        supported_extensions = ['.mp3', '.wav', '.ogg', '.m4a']  # audio extensions
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
                self.wav_audio = self.wav_audio.set_channels(1)
                self.frame_amount = len(self.wav_audio.get_array_of_samples())
                self.wav_audio.set_channels(1)
                self.raw_data = np.frombuffer(self.wav_audio.raw_data, dtype=np.int16)
                self.gethighestresonance()
            except Exception as e:
                self.sb(f"Error during conversion: {e}")

    def extracttime(self):
        if self.wav_audio is not None:
            time_duration = len(self.wav_audio) / 1000

            time_min = time_duration // 60
            time_sec = round(time_duration % 60)

            time_string = f'{time_min} minutes {time_sec} seconds'
            self.sb(f"Time is: {time_string}")
        else:
            self.sb(f'Make sure to press load')

    def createplot(self):
        if self.wav_audio is not None:
            samples = np.array(self.wav_audio.get_array_of_samples())
            # Calculate time values for x-axis
            duration_in_sec = len(self.wav_audio) / 1000
            time_values = np.linspace(0, duration_in_sec, num=len(samples))

            # Plot the waveform
            figure = Figure(figsize=(7, 4), dpi=100)
            plot = figure.add_subplot(1, 1, 1)
            plot.plot(time_values, samples)
            plot.set_xlabel("Time (seconds)")
            plot.set_ylabel("Amplitude")
            plot.set_title('Waveform of ' + self._filepath.get().split('/')[-1])

            canvas = FigureCanvasTkAgg(figure, master=self.data_file_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=0, row=3)
        else:
            self.sb(f'Make sure to press load')

    def gethighestresonance(self):

        data = np.array(self.wav_audio.get_array_of_samples())

        frequencies, power = scipy.signal.welch(data, self.wav_audio.frame_rate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        self.highest_resonance.set(str(dominant_frequency))


    def PlotFrequency(self):
        if self.wav_audio is not None:
            # Convert AudioSegment to NumPy array
            samples = np.array(self.wav_audio.get_array_of_samples())

            # Find the index of the maximum amplitude
            max_amplitude_index = np.argmax(np.abs(samples))

            # Calculate time corresponding to the index
            time_of_max_amplitude = max_amplitude_index / self.wav_audio.frame_rate
            self.gethighestresonance()
            self.sb(f"Highest amplitude happened at {round(time_of_max_amplitude, 2)} and the resonant frequency was {round(float(self.highest_resonance.get()), 2)}")
        else:
            self.sb(f'Make sure to press load')

    def RT60(self):
        if self.wav_audio is not None:
            sample_rate = self.wav_audio.frame_rate
            data = np.array(self.wav_audio.get_array_of_samples())
            spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024)
            plt.close()

            def find_target_frequency(freqs, target_freq):
                for x in freqs:
                    if x > target_freq:
                        break
                return x

            def frequency_check(target_freq):
                global target_frequency
                target_frequency = find_target_frequency(freqs, target_freq)
                index_of_frequency = np.where(freqs == target_frequency)[0][0]

                data_for_frequency = spectrum[index_of_frequency]

                data_in_db_fun = 10 * np.log10(data_for_frequency + 1)
                return data_in_db_fun

            def find_nearest_value(array, value):
                array = np.asarray(array)
                idx = (np.abs(array - value)).argmin()
                return array[idx]

            loop = {1: 20, 2: 1000, 3: 5000}
            self.count += 1
            self.count = self.count % 3 + 1
            data_in_db = frequency_check(loop[self.count])

            index_of_max = np.argmax(data_in_db)

            value_of_max = data_in_db[index_of_max]

            sliced_array = data_in_db[index_of_max:]
            value_of_max_less_5 = value_of_max - 5

            value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
            index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

            value_of_max_less_25 = value_of_max - 25
            value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
            index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)

            rt60 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]

            seconds = np.round(abs(rt60), 3)
            self.sb(f'The RT60 reverb time at freq {int(target_frequency)} Hz is {seconds} seconds')
            self.RT60values[self.count] = seconds

            figure = Figure(figsize=(7, 4), dpi=100)
            plot = figure.add_subplot(1, 1, 1)
            plot.plot(t, data_in_db, linewidth=1, alpha=.7, color='#004bc6')
            plot.plot(t[index_of_max], data_in_db[index_of_max], 'go')
            plot.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
            plot.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')
            plot.set_xlabel("Time (seconds)")
            plot.set_ylabel("DB")
            plot.set_title("Audio Waveform")

            canvas = FigureCanvasTkAgg(figure, master=self.data_file_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=0, row=3)
        else:
            self.sb(f'Make sure to press load')

    def RT60avg(self):
        try:
            if self.wav_audio is not None:
                s = 0
                for x in range(3):
                    s += self.RT60values[x+1]
                avg = s / 3
                avg -= 0.5
                self.sb(f'The RT60 minus 0.5 is {round(avg, 3)}')
            else:
                self.sb(f'Make sure to press load')
        except Exception as e:
            self.sb(f"Press RT60 plot at least 3 times first")

    def Frequency(self):
        if self.wav_audio is not None:
            def calculate_frequency_spectrum(samples, frame_rate):
                # Perform Fourier Transform
                fft_result = np.fft.fft(samples)

                # Calculate the frequencies corresponding to the FFT result
                frequencies = np.fft.fftfreq(len(fft_result), 1 / frame_rate)

                # Take the absolute value to get the amplitude spectrum
                amplitudes = np.abs(fft_result)

                # Keep only the positive frequencies
                positive_frequencies = frequencies[:len(frequencies) // 2]
                positive_amplitudes = amplitudes[:len(amplitudes) // 2]

                return positive_frequencies, positive_amplitudes

            samples = np.array(self.wav_audio.get_array_of_samples())
            frequencies, amplitudes = calculate_frequency_spectrum(samples, self.wav_audio.frame_rate)

            # Filter frequencies within the specified range
            mask = np.logical_and(frequencies >= 20, frequencies <= 20000)
            filtered_frequencies = frequencies[mask]
            filtered_amplitudes = amplitudes[mask]

            # Plot the specific frequencies
            figure = Figure(figsize=(7, 4), dpi=100)
            plot = figure.add_subplot(1, 1, 1)
            plot.plot(filtered_frequencies, filtered_amplitudes)

            plot.set_xlabel("Frequency (Hz)")
            plot.set_ylabel("Amplitude")
            plot.set_title(f"Frequency Spectrum ({20} Hz to {20000} Hz)")

            canvas = FigureCanvasTkAgg(figure, master=self.data_file_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=0, row=3)
        else:
            self.sb(f'Make sure to press load')

if __name__ == "__main__":
    root = Tk()
    app = AudioAnalyzerApp(root)
    root.mainloop()
