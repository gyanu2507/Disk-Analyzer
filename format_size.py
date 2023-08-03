def format_size(size_in_bytes):
    # Define units and their corresponding labels
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']

    # Find the appropriate unit and format the size
    unit_index = 0
    while size_in_bytes >= 1024 and unit_index < len(units) - 1:
        size_in_bytes /= 1024
        unit_index += 1

    # Format the size with up to two decimal places
    return f"{size_in_bytes:.2f} {units[unit_index]}"