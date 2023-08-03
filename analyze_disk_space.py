import os
from collections import defaultdict

def analyze_disk_space(directory):
    file_sizes = defaultdict(list)
    format_sizes = defaultdict(int)
    folder_sizes = defaultdict(lambda: defaultdict(int))
    last_access_times = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_sizes[file_size].append(file_path)

            file_format = os.path.splitext(file)[1].lower()
            format_sizes[file_format] += file_size

            folder_path = os.path.relpath(root, directory)
            folder_sizes[folder_path][file_format] += file_size

            last_access_time = os.path.getatime(file_path)
            last_access_times[file_path] = last_access_time

    return file_sizes, format_sizes, folder_sizes, last_access_times
