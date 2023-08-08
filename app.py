# Ease-Y by GL32
# A simple app for creating tweens!
import customtkinter as ctk
import easing_functions as ease
from tkinter import Canvas, DoubleVar
from lib import Spinbox

# Credits to Akascape for CTkXYFrame and pywinstyles (https://github.com/Akascape)
from CTkXYFrame import CTkXYFrame
import pywinstyles

class SettingsWindow(ctk.CTkToplevel):
	# Settings window for the app
	def __init__(self, parent):
		# Instantiate Window, and Window Config
		super().__init__(parent)
		self.title('Ease-Y Settings')
		self.geometry('350x550')
		self.resizable(False, False)
		self.parent = parent

		# App Label
		ctk.CTkLabel(self, text='Settings ⚙️').pack(pady=5)

		# Category Switcher
		self.categories = ctk.CTkTabview(self)
		self.categories.pack(padx=10, pady=(0, 10), fill='both', expand=1)
		self.projconfig_tab = self.categories.add('Project Config')
		self.display_tab = self.categories.add('Display')

		# Project Config Settings
		self.projconfig_tab.grid_columnconfigure(0, weight=1)
		self.projconfig_tab.grid_columnconfigure(1, weight=1)

		# Frame Rate
		ctk.CTkLabel(self.projconfig_tab, text='Frame Rate: ').grid(row=0, column=0)
		self.frame_rate_box = Spinbox(self.projconfig_tab)
		self.frame_rate_box.grid(row=0, column=1, pady=5, padx=5)

		ctk.CTkLabel(self.projconfig_tab, text='Animation Length (Seconds): ').grid(row=1, column=0)
		self.anim_length_box = Spinbox(self.projconfig_tab)
		self.anim_length_box.grid(row=1, column=1, pady=5, padx=5)

		# Save Button
		ctk.CTkButton(self.projconfig_tab, text='Save', command=self.save).grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

	def save(self):
		self.parent.frame_rate = self.frame_rate_box.get()

class EaseY(ctk.CTk):
	# The class containing the app. Everything is in here
	def __init__(self):
		# Instantiate Window, and Window Config
		super().__init__()
		pywinstyles.apply_style(self, 'mica')
		self.title('Ease-Y')
		self.geometry('1000x550')
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=2)
		self.grid_columnconfigure(1, weight=3)

		# Settings
		self.frame_rate = 30    # Measured in FPS (May not be accurate on low-end hardware)
		self.length = 1         # Measured in SECONDS
		self.zoom_factor = 1    # Zooming for the canvas. The default width and height is 640x360. This is a multiplier for that.
		self.current_frame = 0  # Frame the animation is currently on

		# Toolbar
		self.categories = ctk.CTkTabview(self)
		self.categories.grid(row=0, column=0, padx=10, pady=(0, 10), sticky='nwes')

		# Canvas Display
		self.display_container = CTkXYFrame(self)
		self.display_container.grid(row=0, column=1, sticky='nwes', pady=10, padx=10)
		self.display = Canvas(self.display_container, width=640, height=360, highlightthickness=0)
		self.display.grid()

		self.display.create_line(0, 40, 530, 210, width=10)

		# Frame Start/End & Settings Buttons
		self.frame_buttons = ctk.CTkFrame(self, height=30, fg_color='transparent')
		self.frame_buttons.grid(row=1, column=0, sticky='ew', padx=10, columnspan=2)

		self.frame_start = ctk.CTkButton(self.frame_buttons, text='Edit Start', cursor='hand2', fg_color='gray20')
		self.frame_start.place(relx=0, rely=0.5, anchor='w')
		self.proj_settings = ctk.CTkButton(self.frame_buttons, text='Settings ⚙️', cursor='hand2', fg_color='gray20', command=lambda: SettingsWindow(self))
		self.proj_settings.place(relx=0.5, rely=0.5, anchor='center')
		self.frame_end = ctk.CTkButton(self.frame_buttons, text='Edit End', cursor='hand2', fg_color='gray20')
		self.frame_end.place(relx=1, rely=0.5, anchor='e')

		# Time Slider
		self.timeslider_var = DoubleVar(self, 0.0)
		self.timeslider_var.trace('w', lambda *args: self.scrub(self.timeslider_var.get()))
		self.timeslider = ctk.CTkSlider(self, from_=0, to=1, variable=self.timeslider_var)
		self.timeslider.grid(row=2, column=0, sticky='ew', padx=10, pady=10, columnspan=2)

	def scrub(self, time):
		# Scrubs the animation to the specified time (IN SECONDS)
		self.current_frame = time//(1/self.frame_rate)
		print(self.current_frame)

# Start Ease-Y and run it
root = EaseY()
root.mainloop()