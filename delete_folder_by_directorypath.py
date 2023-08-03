import os
import shutil

def delete_folder_by_directorypath(directory_path):
    try:
        if not os.path.exists(directory_path):
            print(f"Error: The folder '{directory_path}' does not exist.")
            return

        if not os.path.isdir(directory_path):
            print(f"Error: '{directory_path}' is not a valid folder.")
            return

        # Check if the folder contains any system files
        system_files_found = False
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_attributes = os.stat(file_path).st_file_attributes
                if file_attributes & 0x4:
                    print(f"Warning: Skipping deletion of system file: {file_path}")
                    system_files_found = True

        if system_files_found:
            confirm = input("Do you still want to delete the folder? (y/n): ").lower()
            if confirm != 'y':
                print("Deletion canceled.")
                return

        # Delete the folder and its contents
        shutil.rmtree(directory_path)
        print(f"Deleted folder: {directory_path}")
    except OSError as e:
        print(f"Error deleting {directory_path}: {e}")
