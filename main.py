#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from camera.webcam import get_camera, read_frame
from services.detection_service import process_frame
from picamera2 import Picamera2
from PIL import Image, ImageTk
import time


class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.configure(bg="#1e1e1e")

        self.is_detecting = False
        self.picam2 = get_camera()

        # Detection timer settings
        self.last_detection_time = 0
        self.detection_delay = 7  # seconds

        # --- Main layout ---
        main_frame = tk.Frame(self.window, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame, bg="#1e1e1e", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        right_frame = tk.Frame(main_frame, bg="#1e1e1e", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Canvas for video ---
        self.canvas = tk.Canvas(left_frame, width=640, height=450, bg="black")
        self.canvas.pack()

        # --- Start/Stop Button below video ---
        self.toggle_button = ttk.Button(
            left_frame,
            text="Start Detection",
            command=self.toggle_detection
        )
        self.toggle_button.pack(pady=10)

        # --- Counters on the right ---
        self.counter_label = tk.Label(
            right_frame,
            text="Biodegradable: 0\nNon-Biodegradable: 0",
            font=("Helvetica", 16, "bold"),
            bg="#1e1e1e",
            fg="white",
            justify=tk.LEFT
        )
        self.counter_label.pack(anchor=tk.NW, pady=5)

        # --- Countdown Timer ---
        self.timer_label = tk.Label(
            right_frame,
            text="Next detection in: -",
            font=("Helvetica", 12),
            bg="#1e1e1e",
            fg="lightgray"
        )
        self.timer_label.pack(anchor=tk.NW, pady=(0, 10))

        # --- Log box below counters ---
        self.log_text = tk.Text(
            right_frame,
            height=25,
            width=40,
            font=("Courier", 10),
            bg="black",
            fg="lime",
            insertbackground="white"
        )
        self.log_text.pack(pady=10, fill=tk.Y)

        # --- Init ---
        self.image_on_canvas = None
        self.biodegradable_counter = 0
        self.non_biodegradable_counter = 0

        # --- Start update loop ---
        self.update()
        self.window.mainloop()

    def toggle_detection(self):
        self.is_detecting = not self.is_detecting
        self.toggle_button.config(text="Stop Detection" if self.is_detecting else "Start Detection")
        if self.is_detecting:
            self.last_detection_time = time.time()

    def update(self):
        try:
            frame = read_frame(self.picam2)
            current_time = time.time()

            if self.is_detecting:
                time_since_last = current_time - self.last_detection_time
                remaining_delay = max(0, int(self.detection_delay - time_since_last))
                self.timer_label.config(text=f"Next detection in: {remaining_delay}s")

                if time_since_last >= self.detection_delay:
                    frame, self.biodegradable_counter, self.non_biodegradable_counter, logs = process_frame(
                        frame,
                        self.biodegradable_counter,
                        self.non_biodegradable_counter
                    )

                    # Reset timer ONLY if a valid detection was made
                    if any("Biodegradable detected" in log or "Non-Biodegradable detected" in log for log in logs):
                        self.last_detection_time = current_time

                    self.counter_label.config(
                        text=f"Biodegradable: {self.biodegradable_counter}\nNon-Biodegradable: {self.non_biodegradable_counter}"
                    )

                    if logs:
                        for log in logs:
                            self.log_text.insert(tk.END, log + "\n")
                        self.log_text.see(tk.END)
            else:
                self.timer_label.config(text="Detection paused.")

            # Show the frame
            frame_rgb = frame[..., ::-1]  # Convert BGR to RGB
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            if self.image_on_canvas is None:
                self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            else:
                self.canvas.itemconfig(self.image_on_canvas, image=img_tk)

            self.canvas.image = img_tk

        except Exception as e:
            print(f"Error: {e}")

        self.window.after(10, self.update)


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root, "eTapon - Smart Trash Segregation Bin")

