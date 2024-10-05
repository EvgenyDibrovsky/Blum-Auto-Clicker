from mss import mss
import numpy as np
import cv2
import pyautogui
import tkinter as tk
from pynput import mouse
import threading
import time
import keyboard
import win32api, win32con
import random
from tkinter import Toplevel, Text, Scrollbar, RIGHT, Y, END


class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.roi = (0, 0, pyautogui.size().width, pyautogui.size().height)
        self.running = False
        self.point = None
        self.setup_ui()
        self.setup_hotkeys()
        self.sct = mss()  

    def setup_ui(self):
        self.root.title("Blum - Auto Clicker")
        self.root.geometry("300x500")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        self.root.iconbitmap('icon.ico')

        # Заголовок
        self.title_label = tk.Label(self.root, text="Blum - Auto Clicker", font=("Helvetica", 16, "bold"), bg="black", fg="white")
        self.title_label.pack(pady=(20, 10))

        # Общий стиль для кнопок
        button_style = {
            "font": ("Helvetica", 12),
            "bg": "#c8f364",  
            "fg": "black",
            "activebackground": "#a3d432",  
            "relief": "raised",
            "bd": 2,
            "highlightthickness": 2,
            "highlightbackground": "#000000",
            "highlightcolor": "#3e8e41",
            "width": 25
        }
        
        self.start_button = tk.Button(self.root, text="Start clicker", command=self.start_clicker, **button_style)
        self.start_button.pack(pady=10, ipadx=10, ipady=5)
        
        self.stop_button = tk.Button(self.root, text="Stop clicker", command=self.stop_clicker, state=tk.DISABLED, **button_style)
        self.stop_button.pack(pady=10, ipadx=10, ipady=5)
        
        self.setup_roi_button = tk.Button(self.root, text="Set Clickable Area", command=self.setup_roi, **button_style)
        self.setup_roi_button.pack(pady=10, ipadx=10, ipady=5)
        
        self.setup_point_button = tk.Button(self.root, text="Set Start Button", command=self.setup_point, **button_style)
        self.setup_point_button.pack(pady=10, ipadx=10, ipady=5)
        
        self.instructions_button = tk.Button(self.root, text="Instruction", command=self.show_instructions, **button_style)
        self.instructions_button.pack(pady=10, ipadx=10, ipady=5)
        
        self.coords_label = tk.Label(self.root, text="Click coordinates: (not set)", font=("Helvetica", 10), bg="black", fg="white")
        self.coords_label.pack(pady=5)
        
        self.point_label = tk.Label(self.root, text="Button coordinates: (not set)", font=("Helvetica", 10), bg="black", fg="white")
        self.point_label.pack(pady=5)
        
        self.credit_label = tk.Label(self.root, text="Developed by @edwebdev", font=("Helvetica", 10, "italic"), bg="black", fg="gray")
        self.credit_label.pack(pady=10)
    
    def show_instructions(self):
        instructions = """
1. Starting the Application:
- Open the Blum - Auto Clicker application.
- You will see the main window with several buttons for configuration and control.

2. Setting the Clickable Area:
- Click the "Set Clickable Area" button.
- A semi-transparent green window will appear.
- Use your mouse to select the area on the screen where you want the clicks to occur.
- Once the area is selected, the window will close, and the coordinates of the area will be saved.

3. Defining the Start Button:
- Click the "Set Start Button" button.
- A semi-transparent blue window will appear.
- Click on the specific button in your game or application that will trigger the auto clicker to start.
- After clicking, the window will close, and the coordinates of the button will be saved.

4. Starting the Auto Clicker:
- Click the "Start Clicker" button or press the hotkey combination Ctrl+Alt+S to begin the auto-clicking process.
- To pause or resume the auto clicker, press Ctrl+Alt+S again.

"""

        instruction_window = Toplevel(self.root)
        instruction_window.title("Инструкция")
        instruction_window.geometry("450x450")

        text_widget = Text(instruction_window, wrap='word', font=("Helvetica", 12), bg="black", fg="white")

        text_widget.tag_configure("padding", lmargin1=10, lmargin2=10, rmargin=10)
        text_widget.tag_configure("bold", font=("Helvetica", 12, "bold"))
        text_widget.tag_configure("top_padding", spacing1=15)

        text_widget.insert(END, "\n", "top_padding")
        text_widget.insert(END, "1. Starting the Application\n", "bold")
        text_widget.insert(END, "- Open the Blum - Auto Clicker application.\n- You will see the main window with several buttons for configuration and control.\n\n")

        text_widget.insert(END, "2. Setting the Clickable Area\n", "bold")
        text_widget.insert(END, "- Click the \"Set Clickable Area\" button.\n- A semi-transparent green window will appear.\n- Use your mouse to select the area on the screen where you want the clicks to occur.\n- Once the area is selected, the window will close, and the coordinates of the area will be saved.\n\n")

        text_widget.insert(END, "3. Defining the Start Button\n", "bold")
        text_widget.insert(END, "- Click the \"Set Start Button\" button.\n- A semi-transparent blue window will appear.\n- Click on the specific button in your game or application that will trigger the auto clicker to start.\n- After clicking, the window will close, and the coordinates of the button will be saved.\n\n")

        text_widget.insert(END, "4. Starting the Auto Clicker\n", "bold")
        text_widget.insert(END, "- Click the \"Start Clicker\" button or press the hotkey combination Ctrl+Alt+S to begin the auto-clicking process.\n- To pause or resume the auto clicker, press Ctrl+Alt+S again.\n\n")

        text_widget.tag_add("padding", "1.0", END)
        text_widget.config(state='disabled')
        text_widget.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(instruction_window, command=text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        text_widget.config(yscrollcommand=scrollbar.set)


        text_widget.tag_add("padding", "1.0", END)
        text_widget.config(state='disabled')
        text_widget.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(instruction_window, command=text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        text_widget.config(yscrollcommand=scrollbar.set)
  
    def setup_hotkeys(self):
        keyboard.add_hotkey('ctrl+alt+s', self.toggle_clicker)
    
    def toggle_clicker(self):
        if self.running:
            self.stop_clicker()
        else:
            self.start_clicker()

    def setup_roi(self):
        threading.Thread(target=self.select_roi, daemon=True).start()

    def select_roi(self):
        self.roi_window = tk.Toplevel(self.root)
        self.roi_window.overrideredirect(1)
        self.roi_window.attributes('-alpha', 0.3)
        self.roi_window['bg'] = 'green'
        self.roi_window.geometry(f"{pyautogui.size().width}x{pyautogui.size().height}+0+0")

        self.start_x = None
        self.start_y = None

        def on_click(x, y, button, pressed):
            if pressed:
                self.start_x, self.start_y = x, y
            else:
                if self.start_x is not None and self.start_y is not None:
                    roi_width = abs(x - self.start_x)
                    roi_height = abs(y - self.start_y)
                    self.roi = (min(self.start_x, x), min(self.start_y, y), roi_width, roi_height)
                    self.roi_window.destroy()
                    self.coords_label.config(text=f"Click coordinates: {self.roi}")
                    return False   

        def on_move(x, y):
            if self.start_x is not None and self.start_y is not None:
                self.roi_window.geometry(f'{abs(x - self.start_x)}x{abs(y - self.start_y)}+{min(x, self.start_x)}+{min(y, self.start_y)}')

        listener = mouse.Listener(on_click=on_click, on_move=on_move)
        listener.start()
        listener.join()

    def setup_point(self):
        threading.Thread(target=self.select_point, daemon=True).start()

    def select_point(self):
        self.point_window = tk.Toplevel(self.root)
        self.point_window.overrideredirect(1)
        self.point_window.attributes('-alpha', 0.3)
        self.point_window['bg'] = 'blue'
        self.point_window.geometry(f"{pyautogui.size().width}x{pyautogui.size().height}+0+0")

        def on_click(x, y, button, pressed):
            if pressed:
                self.point = (x, y)
                self.point_window.destroy()
                self.point_label.config(text=f"Button coordinates: {self.point}")
                return False   

        listener = mouse.Listener(on_click=on_click)
        listener.start()
        listener.join()

    def start_clicker(self):
        self.running = True
        threading.Thread(target=self.run_clicker, daemon=True).start()
        threading.Thread(target=self.periodic_check, daemon=True).start()
        threading.Thread(target=self.click_start_button, daemon=True).start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_clicker(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def run_clicker(self):
        with mss() as sct:
            monitor = {"top": self.roi[1], "left": self.roi[0], "width": self.roi[2], "height": self.roi[3]}
            while self.running:
                sct_img = sct.grab(monitor)
                frame = np.array(sct_img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower_green = np.array([40, 100, 100])
                upper_green = np.array([80, 255, 255])
                mask = cv2.inRange(hsv, lower_green, upper_green)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    M = cv2.moments(contour)
                    if M['m00'] != 0:
                        cx = int(M['m10'] / M['m00']) + self.roi[0]
                        cy = int(M['m01'] / M['m00']) + self.roi[1]
                        self.click_mouse(cx, cy + 10)
                        time.sleep(random.uniform(0.005, 0.01))

    def periodic_check(self):
        check_interval = 2  
        while self.running:
            if self.point:
                self.check_and_click_point()
            time.sleep(check_interval)

    def click_start_button(self):
        while self.running:
            if self.point:
                self.click_mouse(self.point[0], self.point[1])
            time.sleep(5)

    def check_and_click_point(self):
        if not self.point:
            return
        x, y = self.point
        color = pyautogui.screenshot().getpixel((x, y))
        if color == (255, 255, 255):   
            self.click_mouse(x, y)

    def click_mouse(self, x, y):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()