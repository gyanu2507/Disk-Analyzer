import os
from tkinter import messagebox

# List of popular system file extensions in Windows and macOS
WINDOWS_SYSTEM_EXTENSIONS = [".sys", ".dll", ".exe"]
MAC_SYSTEM_EXTENSIONS = [".kext", ".dylib", ".app"]

# Function to check if a file is a system file based on its extension
def is_system_file(file_path):
    if os.name == 'nt':  # Windows
        return os.path.splitext(file_path)[1].lower() in WINDOWS_SYSTEM_EXTENSIONS
    elif os.name == 'posix':  # macOS (and Linux)
        return os.path.splitext(file_path)[1].lower() in MAC_SYSTEM_EXTENSIONS
    else:
        return False

def delete_temp_files(file_paths):
    try:
        system_files_found = False
        for file_path in file_paths:
            if is_system_file(file_path):
                print(f"Warning: Skipping deletion of system file: {file_path}")
                system_files_found = True

        if system_files_found:
            confirm = messagebox.askquestion("Confirm Deletion", "System files found. Do you still want to delete the files?")
            if confirm != 'yes':
                print("Deletion canceled.")
                return

        for file_path in file_paths:
            if not is_system_file(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")
    except OSError as e:
        print(f"Error deleting files: {e}")
