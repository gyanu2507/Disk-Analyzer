import os

# Function to detect temporary files
def detect_temp_files(file_sizes):
    temp_file_extensions = [".tmp", ".temp", ".bak"]
    temp_files = []

    for file_size, files in file_sizes.items():
        for file_path in files:
            file_format = os.path.splitext(file_path)[1].lower()
            if file_format in temp_file_extensions:
                temp_files.append(file_path)

    return temp_files