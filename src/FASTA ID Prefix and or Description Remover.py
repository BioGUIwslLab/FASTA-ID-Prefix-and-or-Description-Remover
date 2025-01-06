import os
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def run_pipeline(input_file, prefix, desc, progress_bar):

    # Start the progress bar
    progress_bar.start()

    # Select input directory
    input_directory = os.path.dirname(input_file)

    # Select input file
    infile = os.path.basename(input_file)
    
    # Change to the input file's directory
    os.chdir(input_directory)

    # Run command
    if prefix and desc:
        command = f"sed -i 's/^\(>\)[^|]*|/>/' {infile}; sed -i '/^>/ s/[ |].*//' {infile}"
    elif prefix and not desc:
        command = f"sed -i 's/^\(>\)[^|]*|/>/' {infile}"
    else:
        command = f"sed -i '/^>/ s/[ |].*//' {infile}"

    try:
        subprocess.run(["wsl", "bash", "-c", command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        progress_bar.stop()
        if prefix and desc:
            messagebox.showinfo("Success","ID prefix and FASTA description removed")
        elif prefix and not desc:
            messagebox.showinfo("Success","ID prefix removed")
        else:
            messagebox.showinfo("Success","FASTA description removed")

    except subprocess.CalledProcessError as e:
        progress_bar.stop()
        print(f"Error: {e}")
        
def start_thread():
    input_file = input_file_var.get()
    prefix = prefix_var.get()
    desc = desc_var.get()

    if not input_file:
        messagebox.showwarning("Input Error", "Please select an input FASTA file.")
        return
    if not prefix and not desc:
        messagebox.showwarning("Error", "Please select to Remove a prefix or description")
        return

    # Start command in a new thread
    thread = threading.Thread(target=run_pipeline, args=(input_file, prefix, desc, progress_bar))
    thread.start()

def select_file():
    file_path = filedialog.askopenfilename()
    input_file_var.set(file_path)

# Set up tkinter app
app = tk.Tk()
app.title("FASTA ID Prefix and or Description Remover")

# Input file selection
input_file_var = tk.StringVar()
tk.Label(app, text="Input FASTA File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(app, textvariable=input_file_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

# Checkbox for additional option
prefix_var = tk.BooleanVar(value=False)
tk.Checkbutton(app, text="Remove prefix", variable=prefix_var).grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Checkbox for additional option
desc_var = tk.BooleanVar(value=True)
tk.Checkbutton(app, text="Remove description", variable=desc_var).grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Progress Bar (indeterminate)
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=200)
progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=20)

# Start button
tk.Button(app, text="Run program", command=start_thread).grid(row=5, column=1, padx=10, pady=20)

app.mainloop()
