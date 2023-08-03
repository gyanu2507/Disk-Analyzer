import os
import shutil

def copy_data(source_file, destination_dir):
    try:
        if os.path.exists(source_file) and os.path.isfile(source_file):
            # Use shutil.copy() to copy the file to the destination directory
            shutil.copy(source_file, destination_dir)
            print(f"File '{source_file}' copied to '{destination_dir}' successfully.")
        else:
            print(f"Invalid source file path: '{source_file}'")
    except Exception as e:
        print(f"Error occurred during copying: {e}")