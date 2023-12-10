import tkinter as tk
from tkinter import filedialog
import os

import matplotlib.pyplot as plt
import mutagen
import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile


class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view


    def save(self, filepath):
        try:
            # save the model
            self.model.filepath = filepath

            # show a success message
            self.view.sb(f'The filepath {filepath} saved!')
            self.convert_to_wav()

        except ValueError as error:
            # show an error message
            self.view.sb(error)

    def get_file_extension(self):
        return os.path.splitext(self.model.filepath)[-1]

    def get_file_name_with_extension(self):
        return self.model.filepath.get().split('/')[-1]

    def remove_metadata(self):
        metadata = mutagen.Metadata.load(self.model.filepath)
        metadata.delete()

    def convert_to_wav(self):
        if self.get_file_extension() == '.wav':
            # self.remove_metadata()
            self.model.sample_rate, self.model.data = wavfile.read(self.model.filepath)
            self.model.length = self.model.data.shape[0] / self.model.sample_rate
            self.model.timedata = np.linspace(0., self.model.length, self.model.data.shape[0])

        else:
            # self.remove_metadata()
            user_audio_file = AudioSegment.from_file(
                self.model.filepath,
                format=self.get_file_extension().strip('.')
            )
            # new_audio_file = AudioSegment(
            #     data=user_audio_file.raw_data,
            #     frame_rate=user_audio_file.frame_rate,
            #     sample_width=user_audio_file.sample_width,
            #     channels=user_audio_file.channels,
            #
            # )
            temp_wav_filepath = "temp.wav"

            os.system(f'ffmpeg -i {self.model.filepath} ./{temp_wav_filepath}')

            self.model.sample_rate, self.model.data = wavfile.read(temp_wav_filepath)
            self.model.spectrum, self.model.freqs, self.model.timedata, self.model.image = plt.specgram(
                self.model.data, Fs=self.model.sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r')
            )

            os.remove(temp_wav_filepath)


    def check_for_wav(self):
        file_extension = self.get_file_extension()
        return file_extension == '.wav'

