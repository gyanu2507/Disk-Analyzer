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

def delete_duplicate_files(file_paths):
    for file_path in file_paths:
        try:
            if is_system_file(file_path):
                print(f"Warning: Skipping deletion of system file: {file_path}")
                confirm = messagebox.askquestion(f"Warning: Skipping deletion of system file: {file_path}", f"Do you still want to delete the file?\n{file_path}")
                if confirm != 'yes':
                    print("Deletion canceled.")
                    continue

            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")
