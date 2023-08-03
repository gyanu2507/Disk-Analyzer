import os

def detect_large_files(file_sizes, format_sizes, format_thresholds):
    large_files = []

    for file_size, files in file_sizes.items():
        for file_path in files:
            file_format = os.path.splitext(file_path)[1].lower()
            if file_format in format_thresholds and file_size >= format_thresholds[file_format]:
                large_files.append((file_path, file_size))

    return large_files