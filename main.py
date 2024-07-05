import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import uuid
import os


class PhotoBackSwapApp:
    def __init__(self, root):
        self.root = root
        self.photo_path = ""
        self.background_path = ""
        self.device_ip = ""

        self.create_widgets()

    def create_widgets(self):
        self.ip_label = tk.Label(self.root, text="Android Device IP:")
        self.ip_label.pack(pady=5)

        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack(pady=5)

        self.take_photo_button = tk.Button(self.root, text="Take Photo", command=self.take_photo)
        self.take_photo_button.pack(pady=10)

        self.select_background_button = tk.Button(self.root, text="Select Background Image",
                                                  command=self.select_background_image)
        self.select_background_button.pack(pady=10)

        self.generate_button = tk.Button(self.root, text="Generate", command=self.generate)
        self.generate_button.pack(pady=10)

    def take_photo(self):
        self.device_ip = self.ip_entry.get().strip()
        if not self.device_ip:
            messagebox.showerror("Error", "Please enter the Android device IP address.")
            return

        url = f'http://{self.device_ip}:8080/take_photo'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                photo_filename = f"/data/photos/{uuid.uuid4()}.jpg"
                with open(photo_filename, 'wb') as f:
                    f.write(response.content)
                self.photo_path = photo_filename
                messagebox.showinfo("Success", "Photo taken successfully")
            else:
                messagebox.showerror("Error", "Failed to take photo")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to the device: {e}")

    def select_background_image(self):
        self.background_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.background_path:
            messagebox.showinfo("Success", "Background image selected")
        else:
            messagebox.showerror("Error", "No image selected")

    def generate(self):
        if not self.photo_path or not self.background_path:
            messagebox.showerror("Error", "Photo or Background image not selected")
            return

        from BG_Swap import solve

        success, result_path = solve(self.photo_path, self.background_path)
        if success:
            messagebox.showinfo("Success", f"Image generated successfully: {result_path}")
        else:
            messagebox.showerror("Error", "Image generation failed")


if __name__ == "__main__":
    if not os.path.exists("/data/photos"):
        os.makedirs("/data/photos")

    root = tk.Tk()
    app = PhotoBackSwapApp(root)
    root.mainloop()
