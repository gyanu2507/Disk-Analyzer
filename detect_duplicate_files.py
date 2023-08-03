import calculate_md5

def detect_duplicate_files(file_sizes):
    duplicate_files = []

    # Filter out files with the same size (potential duplicates)
    for size, files in file_sizes.items():
        if len(files) > 1:
            duplicate_files.extend(files)

    # Compare content of potential duplicates to find actual duplicates
    unique_hashes = set()
    actual_duplicates = []

    for file_path in duplicate_files:
        file_hash = calculate_md5.calculate_md5(file_path)
        if file_hash not in unique_hashes:
            unique_hashes.add(file_hash)
        else:
            actual_duplicates.append(file_path)

    return actual_duplicates
