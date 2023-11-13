import os.path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from pathlib import Path
from pydub import AudioSegment


def getfilepath():
    _filepath.set(tk.filedialog.askopenfilename())


# checks if file is in wav format


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


if __name__ == "__main__":  # execute logic if run directly


    _root = Tk()  # instantiate instance of Tk class
    _root.title('Sound App')
    _root.geometry('600x500')
    _mainframe = ttk.Frame(_root, padding='5 5 5 5 ')  # root is parent of frame
    _mainframe.grid(row=0, column=0, sticky=("E", "W", "N", "S"))  # placed on first row,col of parent
    # frame can extend itself in all cardinal directions

    _filepath = StringVar()

    _choose_file_label = ttk.Label(
        _mainframe,
        text='Please input the path file you would like to analyze: ',
    )
    _choose_file_label.grid(
        column=0,
        row=0,
        columnspan=1,
        sticky='W'
    )

    _choose_file_textbox = ttk.Entry(
        _mainframe,
        width=80,
        textvariable=_filepath
    )
    _choose_file_textbox.grid(
        column=0,
        row=1
    )

    _choose_file_button = ttk.Button(
        _mainframe,
        text='Browse',
        command=getfilepath
    )
    _choose_file_button.grid(
        column=0,
        row=2,
        sticky='W'
    )

    _root.mainloop()  # listens for events, blocks any code that comes after it



