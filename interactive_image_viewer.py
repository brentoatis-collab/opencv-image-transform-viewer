# ======================================================
# CST 544 Week 1
# Interactive Image Viewer with Transformations
# Brent Oatis
# ======================================================

# Install required libraries if needed
# !pip install opencv-python pillow matplotlib

import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# ======================================================
# Initialize Main Window
# ======================================================

root = Tk()
root.title("Interactive Image Viewer - Brent Oatis")
root.geometry("1000x700")
root.configure(bg="#1e1e1e")

# ======================================================
# Global Variables
# ======================================================

original_image = None
current_image = None

# ======================================================
# Canvas Setup
# ======================================================

canvas = Canvas(root, width=800, height=500, bg="gray")
canvas.pack(pady=20)

status_label = Label(
    root,
    text="Load an image to begin.",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 12)
)
status_label.pack()

# ======================================================
# Helper Function to Display Image
# ======================================================

def update_canvas(img):
    global current_image

    current_image = img.copy()

    # Convert OpenCV BGR to RGB
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert to PIL Image
    pil_image = Image.fromarray(rgb_image)

    # Resize image for display
    pil_image.thumbnail((800, 500))

    # Convert to ImageTk format
    tk_image = ImageTk.PhotoImage(pil_image)

    # Update canvas
    canvas.image = tk_image
    canvas.create_image(400, 250, image=tk_image)

# ======================================================
# Load Image Function
# ======================================================

def load_image():
    global original_image

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )

    if file_path:
        original_image = cv2.imread(file_path)
        update_canvas(original_image)
        status_label.config(text=f"Loaded Image: {file_path}")

# ======================================================
# Resize Function
# ======================================================

def resize_image():
    global current_image

    if current_image is not None:
        resized = cv2.resize(current_image, (400, 400))
        update_canvas(resized)
        status_label.config(text="Image resized to 400x400")

# ======================================================
# Rotate Function
# ======================================================

def rotate_image():
    global current_image

    if current_image is not None:
        (h, w) = current_image.shape[:2]
        center = (w // 2, h // 2)

        rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1.0)

        rotated = cv2.warpAffine(current_image, rotation_matrix, (w, h))

        update_canvas(rotated)
        status_label.config(text="Image rotated 45 degrees")

# ======================================================
# Flip Function
# ======================================================

def flip_image():
    global current_image

    if current_image is not None:
        flipped = cv2.flip(current_image, 1)
        update_canvas(flipped)
        status_label.config(text="Image flipped horizontally")

# ======================================================
# Convert to Grayscale
# ======================================================

def grayscale_image():
    global current_image

    if current_image is not None:
        gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)

        # Convert back to BGR for consistent display
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        update_canvas(gray_bgr)
        status_label.config(text="Converted to Grayscale")

# ======================================================
# Convert to HSV
# ======================================================

def hsv_image():
    global current_image

    if current_image is not None:
        hsv = cv2.cvtColor(current_image, cv2.COLOR_BGR2HSV)

        # Convert HSV to BGR for display
        hsv_bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        update_canvas(hsv_bgr)
        status_label.config(text="Converted to HSV Color Space")

# ======================================================
# Reset Image
# ======================================================

def reset_image():
    global original_image

    if original_image is not None:
        update_canvas(original_image)
        status_label.config(text="Image reset to original")

# ======================================================
# Save Image
# ======================================================

def save_image():
    global current_image

    if current_image is not None:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
        )

        if save_path:
            cv2.imwrite(save_path, current_image)
            status_label.config(text=f"Image saved to: {save_path}")

# ======================================================
# Button Frame
# ======================================================

button_frame = Frame(root, bg="#1e1e1e")
button_frame.pack(pady=10)

# ======================================================
# Buttons
# ======================================================

Button(button_frame, text="Load Image", command=load_image, width=15).grid(row=0, column=0, padx=5)
Button(button_frame, text="Resize", command=resize_image, width=15).grid(row=0, column=1, padx=5)
Button(button_frame, text="Rotate", command=rotate_image, width=15).grid(row=0, column=2, padx=5)
Button(button_frame, text="Flip", command=flip_image, width=15).grid(row=0, column=3, padx=5)
Button(button_frame, text="Grayscale", command=grayscale_image, width=15).grid(row=0, column=4, padx=5)
Button(button_frame, text="HSV", command=hsv_image, width=15).grid(row=0, column=5, padx=5)
Button(button_frame, text="Reset", command=reset_image, width=15).grid(row=0, column=6, padx=5)
Button(button_frame, text="Save", command=save_image, width=15).grid(row=0, column=7, padx=5)

# ======================================================
# Start Application
# ======================================================

root.mainloop()