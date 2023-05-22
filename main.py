import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import preprocessing
import postprocessing
import white_black_list
import detectdigits
import cv2
import numpy as np


def set_filename():
    global filename
    filename.set(fd.askopenfilename())


def run_ocr():
    global filename, block_size, angle_limit, erosion_size, erosion_iterations, text
    text.delete("1.0", "end")
    try:
        img, dis = preprocessing.preprocess(filename.get(),
                                            int(block_size.get()),
                                            int(angle_limit.get()),
                                            int(erosion_size.get()),
                                            int(erosion_iterations.get()))
        img = img.astype(np.uint8)
        output = postprocessing.postprocess(img)
        text.insert("1.0", output)
    except Exception as e:
        text.insert("end", "Error: " + str(e), ["error"])


def run_preview():
    global filename, block_size, erosion_size, erosion_iterations, text
    try:
        img = preprocessing.preview(filename.get(),
                                    int(block_size.get()),
                                    int(erosion_size.get()),
                                    int(erosion_iterations.get()))
        cv2.imshow("Display", img)
        cv2.waitKey()
    except Exception as e:
        text.insert("end", "Error: " + str(e), ["error"])


window = tk.Tk()
window.title("OCR")
main_frame = ttk.Frame(window, padding=10)
settings_frame = ttk.Frame(main_frame, borderwidth=5, relief="ridge", width=200, height=100, padding="5")

filename = tk.StringVar()
file_label = ttk.Label(settings_frame, text="Enter file location or URL:", justify="left")
file_entry = ttk.Entry(settings_frame, textvariable=filename, width=35)
file_select = ttk.Button(settings_frame, text="Select file", command=set_filename)

parameters_frame = ttk.Frame(settings_frame, padding="10")

block_label = ttk.Label(parameters_frame, text="Block size (must be odd)", justify="left", width=25)
block_size = tk.StringVar(value="101")
block_size_field = ttk.Spinbox(parameters_frame, from_=3.0, to=10000.0, textvariable=block_size)

angle_label = ttk.Label(parameters_frame, text="Angle limit", justify="left", width=25)
angle_limit = tk.StringVar(value="5")
angle_limit_field = ttk.Spinbox(parameters_frame, from_=0.0, to=90.0, textvariable=angle_limit)

erosion_label = ttk.Label(parameters_frame, text="Erosion kernel size", justify="left", width=25)
erosion_size = tk.StringVar(value="1")
erosion_size_field = ttk.Spinbox(parameters_frame, from_=0, to=10, textvariable=erosion_size)

erosion_iter_label = ttk.Label(parameters_frame, text="Erosion iterations", justify="left", width=25)
erosion_iterations = tk.StringVar(value="1")
erosion_iterations_field = ttk.Spinbox(parameters_frame, from_=0, to=10, textvariable=erosion_iterations)

# preview preprocessed image
preview_button = ttk.Button(settings_frame, text="Preview",
                            command=run_preview, width=20)
# run OCR and display text output
run_button = ttk.Button(settings_frame, text="Run",
                        command=run_ocr, width=20)

output_frame = ttk.Frame(main_frame)

output_label = ttk.Label(output_frame, text="Output:")
text = tk.Text(output_frame, width=40, height=10)
text.insert("1.0", "")  # OCR output goes here
text.tag_configure("error", foreground="red")

main_frame.grid()

settings_frame.grid(column=0, row=0, columnspan=4, rowspan=6)

file_label.grid(column=0, row=0, columnspan=4)
file_entry.grid(column=0, row=1, columnspan=3)
file_select.grid(column=3, row=1)

parameters_frame.grid(column=0, row=2, columnspan=4)

block_label.grid(column=0, row=2, columnspan=2)
block_size_field.grid(column=2, row=2, columnspan=2)

angle_label.grid(column=0, row=3, columnspan=2)
angle_limit_field.grid(column=2, row=3, columnspan=2)

erosion_label.grid(column=0, row=4, columnspan=2)
erosion_size_field.grid(column=2, row=4, columnspan=2)

erosion_iter_label.grid(column=0, row=5, columnspan=2)
erosion_iterations_field.grid(column=2, row=5, columnspan=2)

preview_button.grid(column=0, row=6, columnspan=2)
run_button.grid(column=2, row=6, columnspan=2)

output_frame.grid(columnspan=6)
output_label.grid()
text.grid()

window.mainloop()
