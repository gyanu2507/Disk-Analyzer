import os

def delete_duplicate_files(file_paths):
    for file_path in file_paths:
        try:
            # Check if the file is a system file before deletion
            file_attributes = os.stat(file_path).st_file_attributes
            if file_attributes & 0x4:
                print(f"Warning: Skipping deletion of system file: {file_path}")
                confirm = input("Do you still want to delete the file? (y/n): ").lower()
                if confirm != 'y':
                    print("Deletion canceled.")
                    continue  # Skip the current file and proceed to the next one

            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")
