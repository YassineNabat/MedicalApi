import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import csv
import pyttsx3
from PIL import Image, ImageTk
import dateutil.parser


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
def set_medication_reminders():
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

#add medication to the schedule
def add_medication_schedule(medication_name, dosage, frequency, schedule_time):
    try:
        datetime.datetime.strptime(schedule_time, "%H:%M")  # Validate time format
        with open(MEDICATION_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([medication_name, dosage, frequency, schedule_time])
        messagebox.showinfo("Success", "Medication schedule added successfully.")
        speak_text("Medication schedule added successfully.")
    except ValueError:
        messagebox.showerror("Invalid Time Format", "Please enter time in HH:MM format.")


#display add medication form
def add_medication():
    def submit_medication():
        add_medication_schedule(entry_medication_name.get(), entry_dosage.get(), entry_frequency.get(), entry_schedule_time.get())
        top1.destroy()

    top1 = tk.Toplevel()
    top1.title("Add Medication")
    top1.geometry("450x400")
    top1.config(bg="#f4f4f4")

    fields = ["Medication Name", "Dosage", "Frequency", "Schedule Time (HH:MM)"]
    entries = []
    for field in fields:
        tk.Label(top1, text=f"{field}:", font=("Helvetica", 12), fg="#333333", bg="#f4f4f4").pack(pady=5)
        entry = tk.Entry(top1, font=("Helvetica", 12), width=30)
        entry.pack(pady=5)
        entries.append(entry)

    entry_medication_name, entry_dosage, entry_frequency, entry_schedule_time = entries

    ttk.Button(top1, text="Add Medication", command=submit_medication).pack(pady=20)
    top1.after(500, speak_text, "Please enter your medication details.")
    top1.mainloop()

#display add medication form
def add_medication():
    def submit_medication():
        add_medication_schedule(entry_medication_name.get(), entry_dosage.get(), entry_frequency.get(), entry_schedule_time.get())
        top1.destroy()

    top1 = tk.Toplevel()
    top1.title("Add Medication")
    top1.geometry("450x400")
    top1.config(bg="#f4f4f4")

    fields = ["Medication Name", "Dosage", "Frequency", "Schedule Time (HH:MM)"]
    entries = []
    for field in fields:
        tk.Label(top1, text=f"{field}:", font=("Helvetica", 12), fg="#333333", bg="#f4f4f4").pack(pady=5)
        entry = tk.Entry(top1, font=("Helvetica", 12), width=30)
        entry.pack(pady=5)
        entries.append(entry)

    entry_medication_name, entry_dosage, entry_frequency, entry_schedule_time = entries

    ttk.Button(top1, text="Add Medication", command=submit_medication).pack(pady=20)
    top1.after(500, speak_text, "Please enter your medication details.")
    top1.mainloop()

#close the application
def close_app():
    window.destroy()

# Create the main window
window = tk.Tk()
window.title("Medication Reminder App")
window.geometry("500x500")
window.config(bg="#f4f4f4")

# Main header
header_label = tk.Label(window, text="Medication Reminder App", font=("Helvetica", 24, "bold"),
                        bg="#4CAF50", fg="white", pady=20)
header_label.pack(fill="x")

# Button frame and buttons
button_frame = ttk.Frame(window, padding=20)
button_frame.pack(pady=50)

buttons = [
    ("Add Medication", add_medication),
    ("Display Medication", display_medication_info),
    ("Set Reminder", set_medication_reminders),
    ("Exit", close_app)
]

for text, command in buttons:
    ttk.Button(button_frame, text=text, command=command, style="Custom.TButton").pack(pady=10, ipadx=20)

# Define custom button styling
style = ttk.Style()
style.configure("Custom.TButton", font=("Helvetica", 14), foreground="#ffffff", background="#4CAF50")
style.map("Custom.TButton", foreground=[('active', 'white')], background=[('active', '#45a049')])

window.after(500, speak_text, "Welcome to the Medication Reminder App.")

# Start the application loop
window.mainloop()
