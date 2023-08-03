import os

def delete_file_by_filepath(file_path):
    try:
        # Check if the file is a system file before deletion
        file_attributes = os.stat(file_path).st_file_attributes
        if file_attributes & 0x4:
            print(f"Warning: Skipping deletion of system file: {file_path}")
            confirm = input("Do you still want to delete the file? (y/n): ").lower()
            if confirm != 'y':
                print("Deletion canceled.")
                return

        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    except OSError as e:
        print(f"Error deleting {file_path}: {e}")
