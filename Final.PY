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
