import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import csv
import pyttsx3


MEDICATION_FILE = 'medication.csv'

#Initialize text-to-speech engine
speech_engine = pyttsx3.init()

def speak_text(command):
    speech_engine.say(command)
    speech_engine.runAndWait()


def load_medication_data():
    try:
        with open(MEDICATION_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            return list(reader)
    except FileNotFoundError:
        messagebox.showerror("Error", f"{MEDICATION_FILE} not found.")
        return []

#display medication information
def display_medication_info():
    top = tk.Toplevel()
    top.title("Medication List")
    top.geometry("450x350")
    top.config(bg="#f4f4f4")

    medication_data = load_medication_data()

    if medication_data:
        ttk.Label(top, text="Your Medication List", font=("Helvetica", 16, "bold"), anchor="center").pack(pady=10)
        for row in medication_data:
            tk.Label(top, text=f"• {row[0]}: {row[1]} - {row[2]} (Time: {row[3]})",
                     font=("Helvetica", 12), bg="#f4f4f4").pack(pady=5, anchor="w")
    else:
        tk.Label(top, text="No medication data found.", font=("Helvetica", 12), fg="#ff0000", bg="#f4f4f4").pack(pady=10)

    top.after(500, speak_text, "Displaying all medications.")
    top.mainloop()

#set reminders for medication
def et_medication_reminders():
    medication_data = load_medication_data()
    current_time = datetime.datetime.now().strftime("%H:%M")
    reminders_triggered = False

    for row in medication_data:
        medication_name, _, _, schedule_time_str = row
        schedule_time = dateutil.parser.parse(schedule_time_str).strftime("%H:%M")

        if current_time == schedule_time:
            messagebox.showinfo("Medication Reminder", f"It's time to take {medication_name}.")
            speak_text(f"Reminder: Take your medication {medication_name}.")
            reminders_triggered = True

    if not reminders_triggered:
        speak_text("No reminders at this time.")
