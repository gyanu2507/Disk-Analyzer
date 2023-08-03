import os

# Function to delete temporary files
def delete_temp_files(file_paths):
    for file_path in file_paths:
        try:
            # Get file attributes
            file_attributes = os.stat(file_path).st_file_attributes

            # Check if the file is a system file (0x4 is the system file attribute)
            if file_attributes & 0x4:
                print(f"Skipping deletion of system file: {file_path}")
            else:
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")
