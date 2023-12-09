import tkinter as tk
from tkinter import filedialog
import os
import mutagen
from pydub import AudioSegment


class Controller:
    filepath = str()

    def set_file_path(self, filepath):
        self.filepath = filepath

    def get_file_path(self):
        return self.filepath

    def get_file_path_with_window(self):
        self.set_file_path(tk.filedialog.askopenfilename())
        return self.get_file_path()

    def get_file_extension(self):
        return os.path.splitext(self.filepath)[-1]


class AudioFileController(Controller):

    def __init__(self, filepath):
        # self.set_file_path(filepath)
        # if not self.check_for_wav():
        #     self.audio_file = self.convert_to_wav()
        # else:
        #     self.audio_file = AudioSegment.from_file(self.get_file_path(), format='.wav')
        pass

    def remove_metadata(self):
        metadata = mutagen.Metadata.load(self.get_file_path())
        metadata.delete()

    def convert_to_wav(self):
        user_audio_file = AudioSegment.from_file(
            self.get_file_path(),
            format=self.get_file_extension().strip('.')
        )
        new_audio_file = AudioSegment(
            data=user_audio_file.raw_data,
            frame_rate=user_audio_file.frame_rate,
            sample_width=user_audio_file.sample_width,
            channels=user_audio_file.channels
        )
        return new_audio_file

    def check_for_wav(self):
        file_extension = self.get_file_extension()
        return file_extension == '.wav'
