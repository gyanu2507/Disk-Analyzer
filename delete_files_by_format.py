import os

def delete_files_by_format(file_paths, target_format):
    try:
        # Check if the file is a system file before deletion
        system_files_found = False
        for file_path in file_paths:
            file_attributes = os.stat(file_path).st_file_attributes
            if file_attributes & 0x4:
                print(f"Warning: Skipping deletion of system file: {file_path}")
                system_files_found = True

        if system_files_found:
            confirm = input("Do you still want to delete the files? (y/n): ").lower()
            if confirm != 'y':
                print("Deletion canceled.")
                return

        for file_path in file_paths:
            if os.path.splitext(file_path)[1].lower() == target_format:
                try:
                    # Delete the file
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")
    except OSError as e:
        print(f"Error deleting files: {e}")
