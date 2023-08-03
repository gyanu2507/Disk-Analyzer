import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict
from tkinter import ttk
from copy_data import copy_data
from get_disk_usage import get_disk_usage
from analyze_disk_space import analyze_disk_space
from detect_duplicate_files import detect_duplicate_files
from delete_duplicate_files import delete_duplicate_files
from detect_large_files import detect_large_files
from delete_files_by_format import delete_files_by_format
from detect_rarely_accessed_files import detect_rarely_accessed_files
from delete_rarely_accessed_files import delete_rarely_accessed_files
from detect_temp_files import detect_temp_files
from delete_temp_files import delete_temp_files
from format_size import format_size


import subprocess

# Define common system file extensions for Windows and macOS
WINDOWS_SYSTEM_FILE_EXTENSIONS = [".sys", ".dll", ".exe", ".bat", ".cmd", ".com"]
MAC_SYSTEM_FILE_EXTENSIONS = [".kext", ".app", ".plugin"]

def is_system_file(file_path):
    """
    Check if the file is a system file based on its extension.
    """
    file_extension = os.path.splitext(file_path)[1].lower()

    if sys.platform.startswith("win32"):
        return file_extension in WINDOWS_SYSTEM_FILE_EXTENSIONS
    elif sys.platform.startswith("darwin"):
        return file_extension in MAC_SYSTEM_FILE_EXTENSIONS
    else:
        return False

def delete_file_by_filepath(file_path):
    try:
        if is_system_file(file_path):
            result_text.insert(tk.END, f"Warning: Skipping deletion of system file: {file_path}\n")
            confirm = messagebox.askquestion("Confirm Deletion", f"Do you still want to delete the file?\n{file_path}")
            if confirm != 'yes':
                result_text.insert(tk.END, "Deletion canceled.\n")
                return

        os.remove(file_path)
        result_text.insert(tk.END, f"Deleted file: {file_path}\n")
    except OSError as e:
        result_text.insert(tk.END, f"Error deleting {file_path}: {e}\n")

def delete_folder_by_directorypath(directory_path):
    try:
        if not os.path.exists(directory_path):
            result_text.insert(tk.END, f"Error: The folder '{directory_path}' does not exist.\n")
            return

        if not os.path.isdir(directory_path):
            result_text.insert(tk.END, f"Error: '{directory_path}' is not a valid folder.\n")
            return

        # Check if the folder is empty
        if os.listdir(directory_path):
            confirm = messagebox.askquestion("Non-Empty Folder", f"The folder '{directory_path}' is not empty. Do you still want to delete it?")
            if confirm != 'yes':
                result_text.insert(tk.END, "Deletion canceled.\n")
                return

        # Check for system files
        system_files_found = False
        system_files = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if is_system_file(file_path):
                    system_files_found = True
                    system_files.append(file_path)

        if system_files_found:
            confirm_system_files = messagebox.askquestion("Confirm Deletion", "System files found. Do you still want to delete the folder?")
            if confirm_system_files != 'yes':
                result_text.insert(tk.END, "Deletion canceled.\n")
                return

        # Proceed with deletion
        if system_files_found:
            for file_path in system_files:
                try:
                    os.remove(file_path)
                    result_text.insert(tk.END, f"Deleted system file: {file_path}\n")
                except OSError as e:
                    result_text.insert(tk.END, f"Error deleting system file {file_path}: {e}\n")

        shutil.rmtree(directory_path)
        result_text.insert(tk.END, f"Deleted folder: {directory_path}\n")
    except OSError as e:
        result_text.insert(tk.END, f"Error deleting {directory_path}: {e}\n")

def on_analyze_button_click():
    directories = entry_folder_paths.get().split(";")
    if not directories or all(dir.strip() == '' for dir in directories):
        messagebox.showerror("Error", "No valid folder paths provided.")
        return

    result_text.delete('1.0', tk.END)

    for directory_path in directories:
        total_space, used_space, free_space = get_disk_usage(directory_path)

        result_text.insert(tk.END, f"\nDirectory/Drive: {directory_path}\n")
        result_text.insert(tk.END, f"Total Disk Space: {format_size(total_space)}\n")
        result_text.insert(tk.END, f"Used Disk Space: {format_size(used_space)}\n")
        result_text.insert(tk.END, f"Free Disk Space: {format_size(free_space)}\n\n")

        file_sizes, format_sizes, folder_sizes, last_access_times = analyze_disk_space(directory_path)

        result_text.insert(tk.END, "Space Breakdown by File Formats:\n")
        max_format_length = max(len(format) for format in format_sizes.keys())
        for format, size in format_sizes.items():
            # Handle empty format (no extension) with a default value
            format_display = format if format else "No Format"
            result_text.insert(tk.END, f"  {format_display:{max_format_length}}: {format_size(size)}\n")

        result_text.insert(tk.END, "\nSpace Breakdown by Folders and File Formats:\n")
        for folder, format_sizes in folder_sizes.items():
            result_text.insert(tk.END, f"\nFolder: {os.path.join(directory_path, folder)}\n")
            for format, size in format_sizes.items():
                # Handle empty format (no extension) with a default value
                format_display = format if format else "No Format"
                result_text.insert(tk.END, f"    {format_display:{max_format_length}}: {format_size(size)}\n")


def on_detect_duplicate_files_button_click():
    directories = entry_folder_paths.get().split(";")
    if not directories or all(dir.strip() == '' for dir in directories):
        messagebox.showerror("Error", "No valid folder paths provided.")
        return

    result_text.delete('1.0', tk.END)

    for directory_path in directories:
        file_sizes, _, _, _ = analyze_disk_space(directory_path)
        duplicate_files = detect_duplicate_files(file_sizes)

        if duplicate_files:
            result_text.insert(tk.END, f"\nDuplicate Files in {directory_path}:\n")
            for file_path in duplicate_files:
                result_text.insert(tk.END, f"    {file_path}\n")
        else:
            result_text.insert(tk.END, f"No duplicate files found in {directory_path}\n")

def on_delete_duplicate_files_button_click():
    directories = entry_folder_paths.get().split(";")
    if not directories or all(dir.strip() == '' for dir in directories):
        messagebox.showerror("Error", "No valid folder paths provided.")
        return

    result_text.delete('1.0', tk.END)

    for directory_path in directories:
        file_sizes, _, _, _ = analyze_disk_space(directory_path)
        duplicate_files = detect_duplicate_files(file_sizes)

        if duplicate_files:
            result_text.insert(tk.END, f"\nDuplicate Files in {directory_path}:\n")
            for file_path in duplicate_files:
                result_text.insert(tk.END, f"    {file_path}\n")

            confirm = messagebox.askquestion("Confirm Deletion", "Do you want to delete duplicate files?")
            if confirm == 'yes':
                delete_duplicate_files(duplicate_files)
        else:
            result_text.insert(tk.END, f"No duplicate files found in {directory_path}\n")

def on_detect_large_files_button_click():
    directories = entry_folder_paths.get().split(";")
    if not directories or all(dir.strip() == '' for dir in directories):
        messagebox.showerror("Error", "No valid folder paths provided.")
        return

    result_text.delete('1.0', tk.END)

    format_thresholds = {
        ".jpg": 1024 * 1024 * 5,
        ".jpeg": 1024 * 1024 * 5,
        ".png": 1024 * 1024 * 10,
        ".doc": 1024 * 1024 * 20,
        ".docx": 1024 * 1024 * 20,
        ".pdf": 1024 * 1024 * 15,
        ".xls": 1024 * 1024 * 25,
        ".xlsx": 1024 * 1024 * 25,
        ".ppt": 1024 * 1024 * 30,
        ".pptx": 1024 * 1024 * 30,
        ".mp3": 1024 * 1024 * 8,
        ".mp4": 1024 * 1024 * 50,
        ".txt": 1024 * 1024 * 2,
        ".zip": 1024 * 1024 * 30,
    }

    for directory_path in directories:
        file_sizes, format_sizes, _, _ = analyze_disk_space(directory_path)
        large_files = detect_large_files(file_sizes, format_sizes, format_thresholds)

        if large_files:
            result_text.insert(tk.END, f"\nLarge Files in {directory_path}:\n")
            for file_path, file_size in large_files:
                result_text.insert(tk.END, f"    {file_path} - {format_size(file_size)}\n")

def on_delete_files_by_format_button_click():
    directories = entry_folder_paths.get().split(";")
    if not directories or all(dir.strip() == '' for dir in directories):
        messagebox.showerror("Error", "No valid folder paths provided.")
        return

    target_format = entry_target_format.get().lower()

    result_text.delete('1.0', tk.END)

    for directory_path in directories:
        file_sizes, _, _, _ = analyze_disk_space(directory_path)
        target_file_paths = []

        for file_size, files in file_sizes.items():
            for file_path in files:
                file_format = os.path.splitext(file_path)[1].lower()
                if file_format == target_format:
                    target_file_paths.append(file_path)

        if target_file_paths:
            result_text.insert(tk.END, f"\nFiles with {target_format} format in {directory_path}:\n")
            for file_path in target_file_paths:
                result_text.insert(tk.END, f"    {file_path}\n")

            confirm = messagebox.askquestion("Confirm Deletion", f"Do you want to delete these files?")
            if confirm == 'yes':
                delete_files_by_format(target_file_paths, target_format)
        else:
            result_text.insert(tk.END, f"No files found with {target_format} format in {directory_path}\n")

def on_detect_rarely_accessed_files_button_click():
    directories = entry_folder_paths.get().split(";")
    if not directories or all(dir.strip() == '' for dir in directories):
        messagebox.showerror("Error", "No valid folder paths provided.")
        return

    result_text.delete('1.0', tk.END)

    for directory_path in directories:
        _, _, _, last_access_times = analyze_disk_space(directory_path)

        days_threshold = int(entry_days_threshold.get())
        rarely_accessed_files = detect_rarely_accessed_files(last_access_times, days_threshold)

        if rarely_accessed_files:
            result_text.insert(tk.END, f"\nRarely Accessed Files in {directory_path}:\n")
            for file_path in rarely_accessed_files:
                result_text.insert(tk.END, f"    {file_path}\n")

def on_delete_rarely_accessed_files_button_click():
    directories = entry_folder_paths.get().split(";")
    if not directories or all(dir.strip() == '' for dir in directories):
        messagebox.showerror("Error", "No valid folder paths provided.")
        return

    result_text.delete('1.0', tk.END)

    for directory_path in directories:
        _, _, _, last_access_times = analyze_disk_space(directory_path)

        days_threshold = int(entry_days_threshold.get())
        rarely_accessed_files = detect_rarely_accessed_files(last_access_times, days_threshold)

        if rarely_accessed_files:
            result_text.insert(tk.END, f"\nRarely Accessed Files in {directory_path}:\n")
            for file_path in rarely_accessed_files:
                result_text.insert(tk.END, f"    {file_path}\n")

            confirm = messagebox.askquestion("Confirm Deletion", "Do you want to delete rarely accessed files?")
            if confirm == 'yes':
                delete_rarely_accessed_files(rarely_accessed_files)

def on_detect_temp_files_button_click():
    directories = entry_folder_paths.get().split(";")
    if not directories or all(dir.strip() == '' for dir in directories):
        messagebox.showerror("Error", "No valid folder paths provided.")
        return

    result_text.delete('1.0', tk.END)

    for directory_path in directories:
        file_sizes, _, _, _ = analyze_disk_space(directory_path)
        temp_files = detect_temp_files(file_sizes)

        if temp_files:
            result_text.insert(tk.END, f"\nTemporary Files in {directory_path}:\n")
            for file_path in temp_files:
                result_text.insert(tk.END, f"    {file_path}\n")

def on_delete_temp_files_button_click():
    directories = entry_folder_paths.get().split(";")
    if not directories or all(dir.strip() == '' for dir in directories):
        messagebox.showerror("Error", "No valid folder paths provided.")
        return

    result_text.delete('1.0', tk.END)

    for directory_path in directories:
        file_sizes, _, _, _ = analyze_disk_space(directory_path)
        temp_files = detect_temp_files(file_sizes)

        if temp_files:
            result_text.insert(tk.END, f"\nTemporary Files in {directory_path}:\n")
            for file_path in temp_files:
                result_text.insert(tk.END, f"    {file_path}\n")

            confirm = messagebox.askquestion("Confirm Deletion", "Do you want to delete temporary files?")
            if confirm == 'yes':
                delete_temp_files(temp_files)

def on_copy_data_button_click():
    source_file = entry_source_file.get()
    destination_dir = entry_destination_dir.get()

    copy_data(source_file, destination_dir)

def on_delete_file_by_filepath_button_click():
    file_path = entry_file_path.get()
    delete_file_by_filepath(file_path)

def on_delete_folder_by_directorypath_button_click():
    folder_path = entry_folder_path.get()
    delete_folder_by_directorypath(folder_path)

def clear_result_text():
    result_text.delete('1.0', tk.END)

def browse_folder():
    """
    Open a file dialog to select a single folder path and populate the entry field.
    """
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_folder_paths.delete(0, tk.END)
        entry_folder_paths.insert(tk.END, folder_path)

# GUI setup
root = tk.Tk()
root.title("Disk Space Analyzer")
root.geometry("1600x1200")

frame_main = tk.Frame(root)
frame_main.pack(fill=tk.BOTH, expand=True)

frame_folder_paths = tk.Frame(frame_main)
frame_folder_paths.pack(fill=tk.BOTH, padx=10, pady=5)

label_folder_paths = tk.Label(frame_folder_paths, text="Enter The Folder Paths You Want To Analyze (separated by ';'): ")
label_folder_paths.pack(side=tk.LEFT)

entry_folder_paths = tk.Entry(frame_folder_paths)
entry_folder_paths.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

browse_button = tk.Button(frame_folder_paths, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT, padx=5)


frame_buttons = tk.Frame(frame_main)
frame_buttons.pack(padx=10, pady=5)

button_analyze = tk.Button(frame_buttons, text="Analyze Disk Space", command=on_analyze_button_click)
button_analyze.pack(side=tk.LEFT)

button_detect_duplicate_files = tk.Button(frame_buttons, text="Detect Duplicate Files", command=on_detect_duplicate_files_button_click)
button_detect_duplicate_files.pack(side=tk.LEFT)

button_delete_duplicate_files = tk.Button(frame_buttons, text="Delete Duplicate Files", command=on_delete_duplicate_files_button_click)
button_delete_duplicate_files.pack(side=tk.LEFT)

button_detect_large_files = tk.Button(frame_buttons, text="Detect Large Files", command=on_detect_large_files_button_click)
button_detect_large_files.pack(side=tk.LEFT)

button_delete_files_by_format = tk.Button(frame_buttons, text="Delete Files by Format", command=on_delete_files_by_format_button_click)
button_delete_files_by_format.pack(side=tk.LEFT)

button_detect_rarely_accessed_files = tk.Button(frame_buttons, text="Detect Rarely Accessed Files", command=on_detect_rarely_accessed_files_button_click)
button_detect_rarely_accessed_files.pack(side=tk.LEFT)

button_delete_rarely_accessed_files = tk.Button(frame_buttons, text="Delete Rarely Accessed Files", command=on_delete_rarely_accessed_files_button_click)
button_delete_rarely_accessed_files.pack(side=tk.LEFT)

frame_buttons = tk.Frame(frame_main)
frame_buttons.pack(padx=10, pady=5)

button_detect_temp_files = tk.Button(frame_buttons, text="Detect Temporary Files", command=on_detect_temp_files_button_click)
button_detect_temp_files.pack(side=tk.LEFT)

button_delete_temp_files = tk.Button(frame_buttons, text="Delete Temporary Files", command=on_delete_temp_files_button_click)
button_delete_temp_files.pack(side=tk.LEFT)


button_copy_data = tk.Button(frame_buttons, text="Copy Data", command=on_copy_data_button_click)
button_copy_data.pack(side=tk.LEFT)

frame_clear_button = tk.Frame(frame_main)
frame_clear_button.pack(fill=tk.BOTH, padx=10, pady=5)

button_clear = tk.Button(frame_clear_button, text="Clear Screen", command=clear_result_text)
button_clear.pack(side=tk.LEFT, padx=5)

frame_delete_file_by_filepath = tk.Frame(frame_main)
frame_delete_file_by_filepath.pack(fill=tk.BOTH, padx=10, pady=5)

frame_delete_folder_by_directorypath = tk.Frame(frame_main)
frame_delete_folder_by_directorypath.pack(fill=tk.BOTH, padx=10, pady=5)

frame_target_format = tk.Frame(frame_main)
frame_target_format.pack(fill=tk.BOTH, padx=10, pady=5)

label_target_format = tk.Label(frame_target_format, text="Enter The Target File Format (e.g., .mp3, .jpg, .txt): ")
label_target_format.pack(side=tk.LEFT)

entry_target_format = tk.Entry(frame_target_format)
entry_target_format.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_days_threshold = tk.Frame(frame_main)
frame_days_threshold.pack(fill=tk.BOTH, padx=10, pady=5)

label_days_threshold = tk.Label(frame_days_threshold, text="Enter The Number of Days Threshold For Rarely Accessed Files: ")
label_days_threshold.pack(side=tk.LEFT)

entry_days_threshold = tk.Entry(frame_days_threshold)
entry_days_threshold.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_copy_data = tk.Frame(frame_main)
frame_copy_data.pack(fill=tk.BOTH, padx=10, pady=5)

label_source_file = tk.Label(frame_copy_data, text="Source File Path: ")
label_source_file.pack(side=tk.LEFT)

entry_source_file = tk.Entry(frame_copy_data)
entry_source_file.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

label_destination_dir = tk.Label(frame_copy_data, text="Destination Directory Path: ")
label_destination_dir.pack(side=tk.LEFT)

entry_destination_dir = tk.Entry(frame_copy_data)
entry_destination_dir.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_delete_file_by_filepath = tk.Frame(frame_main)
frame_delete_file_by_filepath.pack(fill=tk.BOTH, padx=10, pady=5)

label_file_path = tk.Label(frame_delete_file_by_filepath, text="Enter The File Path You Want To Delete: ")
label_file_path.pack(side=tk.LEFT)

entry_file_path = tk.Entry(frame_delete_file_by_filepath)
entry_file_path.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

button_delete_file_by_filepath = tk.Button(frame_delete_file_by_filepath, text="Delete File By Path", command=on_delete_file_by_filepath_button_click)
button_delete_file_by_filepath.pack(side=tk.LEFT, padx=5)

frame_delete_folder_by_directorypath = tk.Frame(frame_main)
frame_delete_folder_by_directorypath.pack(fill=tk.BOTH, padx=10, pady=5)

label_folder_path = tk.Label(frame_delete_folder_by_directorypath, text="Enter The Directory Path You Want To Delete: ")
label_folder_path.pack(side=tk.LEFT)

entry_folder_path = tk.Entry(frame_delete_folder_by_directorypath)
entry_folder_path.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

button_delete_folder_by_directorypath = tk.Button(frame_delete_folder_by_directorypath, text="Delete Folder By Path", command=on_delete_folder_by_directorypath_button_click)
button_delete_folder_by_directorypath.pack(side=tk.LEFT, padx=5)

frame_result_text = tk.Frame(frame_main)
frame_result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

result_text = tk.Text(frame_result_text, wrap=tk.WORD)
result_text.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(result_text)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result_text.yview)

root.mainloop()
