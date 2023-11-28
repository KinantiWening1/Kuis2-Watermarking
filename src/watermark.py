import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

def compare_images(original_img, watermarked_img):
    original_img = cv2.imread(original_img, cv2.IMREAD_GRAYSCALE)

    watermarked_img = watermarked_img.astype(np.uint8)

    watermarked_img = cv2.resize(watermarked_img, (original_img.shape[1], original_img.shape[0]))

    total_diff = cv2.absdiff(original_img, watermarked_img)

    threshold = 15  

    if (total_diff > threshold).any():
        return "The image appears to be watermarked."
    else:
        return "The image does not seem to be watermarked."

def encode_image(img_path, k, seed):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = np.array(img, dtype=np.int16)
    img_width, img_height = img.shape[:2]

    watermark = generate_watermark(img_width, img_height, k, seed)

    watermarked_img = cv2.add(img, watermark)

    return watermarked_img

def generate_watermark(img_width, img_height, k, seed):
    np.random.seed(seed)

    watermark = np.random.randint(2, size=(img_width, img_height))
    watermark = watermark.astype(np.int16)
    watermark[watermark == 0] = -1
    watermark = watermark * k

    watermark = np.array(watermark, dtype=np.int16)
    return watermark

class WatermarkApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Watermark App")

        self.image_path = ""
        self.watermarked_image = None

        # Upload Image Button
        self.upload_button = tk.Button(self.master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        # Generate Watermark Button
        self.generate_button = tk.Button(self.master, text="Generate Watermark", command=self.generate_watermark)
        self.generate_button.pack(pady=10)
        self.generate_button['state'] = 'disabled'

        # Display Image
        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=10)

        # Save Watermarked Image Button
        self.save_button = tk.Button(self.master, text="Save Watermarked Image", command=self.save_watermarked_image)
        self.save_button.pack(pady=10)
        self.save_button['state'] = 'disabled'

        # Test Watermark Button
        self.test_button = tk.Button(self.master, text="Test Watermark", command=self.test_watermark)
        self.test_button.pack(pady=10)
        self.test_button['state'] = 'disabled'

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=
        [("PNG files","*.png"),("JPG files","*.jpg")])
        if self.image_path:
            self.display_image()
            self.generate_button['state'] = 'normal'

    def display_image(self):
        original_image = Image.open(self.image_path)
        original_image = original_image.resize((300, 300), Image.ANTIALIAS) 
        photo = ImageTk.PhotoImage(original_image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def generate_watermark(self):
        strength = 1
        seed = 345676543
        self.watermarked_image = self.add_watermark(self.image_path, strength, seed)
        self.display_watermarked_image(self.watermarked_image)
        self.save_button['state'] = 'normal'
        self.test_button['state'] = 'normal'  # Enable the test button

    def add_watermark(self, input_image_path, strength, seed):
        original_image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
        watermarked_result = encode_image(input_image_path, strength, seed)
        return watermarked_result

    def display_watermarked_image(self, watermarked_result):
        watermarked_image = Image.fromarray(watermarked_result.astype('uint8'))
        watermarked_image = watermarked_image.resize((300, 300), Image.ANTIALIAS)  # Use LANCZOS for antialiasing
        photo = ImageTk.PhotoImage(watermarked_image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def save_watermarked_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            cv2.imwrite(save_path, self.watermarked_image)

    def test_watermark(self):
        if self.image_path and self.watermarked_image is not None:
            print(type(self.watermarked_image))
            result = compare_images(self.image_path, self.watermarked_image)
            tk.messagebox.showinfo("Watermark Test Result", result)
        else:
            tk.messagebox.showwarning("Watermark Test", "Please generate a watermark first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
