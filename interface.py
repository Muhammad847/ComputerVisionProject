import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from FinalMergingProject import *

# Function to open an image file and display it in a label
def open_image(label, image_path):
    img = Image.open(image_path)
    img = img.resize((300, 300), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo
    return cv2.imread(image_path)

def open_image_file(label, target):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
    if file_path:
        img = open_image(label, file_path)
        if target == 1:
            global src_image
            src_image = img
        elif target == 2:
            global ref_image
            ref_image = img

def apply_histogram_matching():
    global src_image, ref_image
    if src_image is not None and ref_image is not None:
        output_image = match_histograms(src_image, ref_image)
        output_image = Image.fromarray(output_image)
        output_image = output_image.resize((300, 300), Image.ANTIALIAS)
        output_photo = ImageTk.PhotoImage(output_image)

        output_window = tk.Toplevel(app)
        output_window.title("Output Image")
        output_label = tk.Label(output_window, image=output_photo)
        output_label.image = output_photo
        output_label.pack()

        global output_image_path
        output_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_image_path:
            cv2.imwrite(output_image_path, cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR))

# Create the main application window
app = tk.Tk()
app.title("Histogram Matching")

src_image = None
ref_image = None
output_image_path = None

src_label = tk.Label(app)
ref_label = tk.Label(app)

button1 = tk.Button(app, text="Open Source Image", command=lambda: open_image_file(src_label, 1))
button2 = tk.Button(app, text="Open Reference Image", command=lambda: open_image_file(ref_label, 2))
apply_button = tk.Button(app, text="Apply Histogram Matching", command=apply_histogram_matching)
save_button = tk.Button(app, text="Save Image", command=lambda: save_output_image(output_image_path))

def save_output_image(output_path):
    if output_path:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            import shutil
            shutil.copy(output_path, save_path)

button1.pack()
src_label.pack()
button2.pack()
ref_label.pack()
apply_button.pack()
save_button.pack()

app.mainloop()
