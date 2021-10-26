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
    # Add a buttongroup with 2 buttons
    button_frame = tk.Frame(window)
    button_frame.pack()
    submit_button = tk.Button(
        button_frame, text="Submit", command=window.destroy)
    submit_button.pack(side=tk.LEFT)
    # Add a cancel button that will exit(1) when clicked
    cancel_button = tk.Button(
        button_frame, text="Cancel", command=lambda: exit(1))
    cancel_button.pack(side=tk.RIGHT)
    window.mainloop()
    # On window close, exit the program
    if name.get() == base_url:
        exit(1)
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
