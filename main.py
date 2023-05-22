import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import preprocessing
import cv2


def set_filename():
    global filename
    filename.set(fd.askopenfilename())


def run_preprocessing():
    global filename, block_size, angle_limit, erosion_size, erosion_iterations, text
    text.delete("1.0", "end")
    try:
        img, dis = preprocessing.preprocess(filename.get(),
                                            int(block_size.get()),
                                            int(angle_limit.get()),
                                            int(erosion_size.get()),
                                            int(erosion_iterations.get()))
        cv2.imshow("Display", img)
        cv2.waitKey()
    except Exception as e:
        text.insert("end", "Error: "+str(e), ["error"])


window = tk.Tk()
window.title("OCR")
main_frame = ttk.Frame(window, padding="10")

filename = tk.StringVar()
file_label = ttk.Entry(main_frame, textvariable=filename)
file_select = ttk.Button(main_frame, text="Select file", command=set_filename)
file_label.grid()
file_select.grid()

block_label = ttk.Label(main_frame, text="Block size")
block_label.grid()
block_size = tk.StringVar()
block_size.set("101")
block_size_field = ttk.Spinbox(main_frame, from_=3.0, to=10000.0, textvariable=block_size)
block_size_field.grid()

angle_label = ttk.Label(main_frame, text="Angle limit")
angle_label.grid()
angle_limit = tk.StringVar()
angle_limit.set("5")
angle_limit_field = ttk.Spinbox(main_frame, from_=0.0, to=90.0, textvariable=angle_limit)
angle_limit_field.grid()

erosion_label = ttk.Label(main_frame, text="Erosion kernel size")
erosion_label.grid()
erosion_size = tk.StringVar()
erosion_size.set("1")
erosion_size_field = ttk.Spinbox(main_frame, from_=0, to=10, textvariable=erosion_size)
erosion_size_field.grid()

erosion_iter_label = ttk.Label(main_frame, text="Number of erosion iterations")
erosion_iter_label.grid()
erosion_iterations = tk.StringVar()
erosion_iterations.set("1")
erosion_iterations_field = ttk.Spinbox(main_frame, from_=0, to=10, textvariable=erosion_iterations)
erosion_iterations_field.grid()


preprocess_button = ttk.Button(main_frame, text="Preprocess",
                               command=run_preprocessing)
preprocess_button.grid()

output_label = ttk.Label(main_frame, text="Output:")
output_label.grid()
text = tk.Text(main_frame, width=40, height=10)
text.insert("1.0", "")  # OCR output goes here
text.tag_configure("error", foreground="red")
# text["state"] = "disabled"
text.grid()

main_frame.grid()
window.mainloop()
