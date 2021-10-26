import tkinter as tk

# Write a function that opens a GUI and lets the user input their linkedin name

def prompt_for_url(base_url):
    window = tk.Tk()
    window.title("Enter Linkedin URL")
    window.geometry("400x80")
    window.resizable(0, 0)
    name = tk.StringVar(window, value=base_url)
    name_label = tk.Label(window, text="Enter your url:")
    name_label.pack()
    name_entry = tk.Entry(window, width=70, textvariable=name)
    name_entry.pack()
    submit_button = tk.Button(window, text="Submit", command=window.destroy)
    submit_button.pack()
    window.mainloop()
    return name.get()

# Write a function that shows an error message
def show_error_message(message):
    window = tk.Tk()
    window.title("Error")
    window.geometry("400x80")
    window.resizable(0, 0)
    error_label = tk.Label(window, text=message)
    error_label.pack()
    submit_button = tk.Button(window, text="OK", command=window.destroy)
    submit_button.pack()
    window.mainloop()
