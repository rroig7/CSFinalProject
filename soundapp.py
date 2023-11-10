import os.path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from pathlib import Path


# simple function returns file from a file_path parameter


def getfilepath() -> str:
    _filepath.set(tk.filedialog.askopenfilename())

# checks if file is in wav format
def checkforwav(file_path):
    file_extension = os.path.splitext(file_path)[1]
    return file_extension.lower() == '.wav'

print(checkforwav('..\\test.wav'))


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
