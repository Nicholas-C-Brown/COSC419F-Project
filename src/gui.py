import tkinter as tk
from tkinter import filedialog, Text

# Write a function that opens a GUI and lets the user input their linkedin name

def prompt_for_url():
    window = tk.Tk()
    window.title("Enter Linkedin URL")
    window.geometry("400x400")
    window.resizable(0, 0)
    name = tk.StringVar()
    name_label = tk.Label(window, text="Enter your url:")
    name_label.pack()
    name_entry = tk.Entry(window, textvariable=name)
    name_entry.pack()
    submit_button = tk.Button(window, text="Submit", command=window.destroy)
    submit_button.pack()
    window.mainloop()
    return name.get()
