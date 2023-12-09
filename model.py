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
from controller import AudioFileController
from scipy.io import wavfile
from view import View


class Model:

    def init(self, view):
        self.view = view
        sample_rate, data = wavfile.read(self.view.audiofilecontroller.get_file_path())
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    def createplot(self):
        plt.plot()


view = View()
model = Model()