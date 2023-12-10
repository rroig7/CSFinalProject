from tkinter import StringVar
from tkinter import ttk
import numpy as np
from pydub import AudioSegment
import wave
import os
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import filedialog
from scipy.io import wavfile
import re

class Model:

    def init(self, filepath):
        self.__filepath = filepath



        # to be extracted once load is called
        self.sample_rate = None
        self.length = None
        self.data = None
        self.spectrum = None
        self.freqs = None
        self.timedata = None
        self.im = None


    @property
    def filepath(self):
        return self.__filepath

    @filepath.setter
    def filepath(self, value):
        self.__filepath = value


    def create_plot(self):
        plt.plot(self.timedata, self.data[:, 0], label="Left Channel")
        plt.plot(self.timedata, self.data[:, 1], label="Right Channel")

        plt.legend()
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.show()