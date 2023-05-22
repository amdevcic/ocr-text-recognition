import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import preprocessing
import cv2


def set_filename():
    global filename
    filename.set(fd.askopenfilename())


def run_preprocessing():
    global filename
    img, dis = preprocessing.preprocess(filename.get(), 11, 5, 1, 1)
    cv2.imshow("Display", img)
    cv2.waitKey()


window = tk.Tk()
window.title("OCR")
main_frame = ttk.Frame(window, padding="10")

filename = tk.StringVar()
file_label = ttk.Entry(main_frame, textvariable=filename)
file_select = ttk.Button(main_frame, text="Select file", command=set_filename)
file_label.grid()
file_select.grid()

preprocess_button = ttk.Button(main_frame, text="Preprocess",
                               command=run_preprocessing)
preprocess_button.grid()

output_label = ttk.Label(main_frame, text="Output:")
output_label.grid()
text = tk.Text(main_frame, width=40, height=10)
text.insert("1.0", "hello world")  # OCR output goes here
text["state"] = "disabled"
text.grid()

main_frame.grid()
window.mainloop()
