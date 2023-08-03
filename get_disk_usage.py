import shutil

def get_disk_usage(directory):
    total, used, free = shutil.disk_usage(directory)
    return total, used, free
