import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import csv
import pyttsx3


MEDICATION_FILE = 'medication.csv'

#Initialize text-to-speech engine
speech_engine = pyttsx3.init()