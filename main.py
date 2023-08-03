import os
import shutil
import get_disk_usage
import analyze_disk_space
import detect_duplicate_files
import delete_duplicate_files
import detect_large_files
import delete_files_by_format
import detect_rarely_accessed_files
import delete_rarely_accessed_files
import detect_temp_files
import delete_temp_files
import get_user_input
import copy_data
import print_welcome_screen
import format_size
import delete_file_by_filepath
import delete_folder_by_directorypath


def main():
    print_welcome_screen.print_welcome_screen()
    
    directories = get_user_input.get_user_input()

    if not directories:
        print("No valid folder paths provided. Exiting...")
        return

    for directory_path in directories:
        # Disk space analysis for the current directory/drive
        total_space, used_space, free_space = get_disk_usage.get_disk_usage(directory_path)
        print(f"\nDirectory/Drive: {directory_path}")
        print(f"Total Disk Space: {format_size.format_size(total_space)}")
        print(f"Used Disk Space: {format_size.format_size(used_space)}")
        print(f"Free Disk Space: {format_size.format_size(free_space)}")

        # Analyze disk space usage and scan for specific file format
        file_sizes, format_sizes, folder_sizes, last_access_times = analyze_disk_space.analyze_disk_space(directory_path)

        # Display space breakdown by file formats
        print("\nSpace Breakdown by File Formats:")
        for format, size in format_sizes.items():
            print(f"  {format}: {format_size.format_size(size)}")

        # Display space breakdown by folders and their file formats
        print("\nSpace Breakdown by Folders and File Formats:")
        for folder, format_sizes in folder_sizes.items():
            print(f"\nFolder: {os.path.join(directory_path, folder)}")
            for format, size in format_sizes.items():
                print(f"    {format}: {format_size.format_size(size)}")

        while True:
            print("\nOptions:")
            print("  1. Search for Files of a Specific Format")
            print("  2. Detect Duplicate Files")
            print("  3. Delete Duplicate Files")
            print("  4. Detect Large Files")
            print("  5. Delete Files by Format")
            print("  6. Detect Rarely Accessed Files")
            print("  7. Delete Rarely Accessed Files")
            print("  8. Detect Temporary Files")
            print("  9. Delete Temporary Files")
            print("  10. Copy Data from One Directory to Another")
            print("  11. Delete File by Filepath")
            print("  12. Delete Folder by Directory Path")
            print("  0. Exit")

            try:
                option = int(input("Enter the option number: "))

                if option == 0:
                    break
                elif option == 1:
                    target_format_response = input("Do you want to search for files of a specific format? (y/n): ").lower()
                    target_file_paths = []
                    if target_format_response == 'y':
                        target_format = input("Enter the target file format (e.g., .mp3, .jpg, .txt): ").lower()
                        for file_size, files in file_sizes.items():
                            for file_path in files:
                                file_format = os.path.splitext(file_path)[1].lower()
                                if file_format == target_format:
                                    target_file_paths.append(file_path)

                        if target_file_paths:
                            print(f"\nFiles with {target_format} format:")
                            for file_path in target_file_paths:
                                print(f"    {file_path}")
                                print()
                        else:
                            print(f"No files found with {target_format} format.")
                elif option == 2:
                    duplicate_files = detect_duplicate_files.detect_duplicate_files(file_sizes)
                    if duplicate_files:
                        print("\nDuplicate Files:")
                        for file_path in duplicate_files:
                            print(f"    {file_path}")
                            print()
                    else:
                        print("No duplicate files found.")
                elif option == 3:
                    duplicate_files = detect_duplicate_files.detect_duplicate_files(file_sizes)
                    if duplicate_files:
                        print("\nDuplicate Files:")
                        for file_path in duplicate_files:
                            print(f"    {file_path}")
                            print()

                        delete_duplicates_response = input("Do you want to delete duplicate files (y/n)? ").lower()
                        if delete_duplicates_response == 'y':
                            delete_duplicate_files.delete_duplicate_files(duplicate_files)
                    else:
                        print("No duplicate files found.")
                elif option == 4:
                    format_thresholds = {
                        ".jpg": 1024 * 1024 * 5,   # 5 MB for JPEG Images
                        ".jpeg": 1024 * 1024 * 5,  # 5 MB for JPEG Images
                        ".png": 1024 * 1024 * 10,  # 10 MB for PNG Images
                        ".doc": 1024 * 1024 * 20,   # 20 MB for Microsoft Word Documents
                        ".docx": 1024 * 1024 * 20,  # 20 MB for Microsoft Word Documents
                        ".pdf": 1024 * 1024 * 15,   # 15 MB for PDF Documents
                        ".xls": 1024 * 1024 * 25,   # 25 MB for Microsoft Excel Spreadsheets
                        ".xlsx": 1024 * 1024 * 25,  # 25 MB for Microsoft Excel Spreadsheets
                        ".ppt": 1024 * 1024 * 30,   # 30 MB for Microsoft PowerPoint Presentations
                        ".pptx": 1024 * 1024 * 30,  # 30 MB for Microsoft PowerPoint Presentations
                        ".mp3": 1024 * 1024 * 8,    # 8 MB for MP3 Audio Files
                        ".mp4": 1024 * 1024 * 50,   # 50 MB for MP4 Video Files
                        ".txt": 1024 * 1024 * 2,    # 2 MB for Plain Text Files
                        ".zip": 1024 * 1024 * 30,   # 30 MB for Compressed Archive Files
                    }
                    large_files = detect_large_files.detect_large_files(file_sizes, format_sizes, format_thresholds)
                    if large_files:
                        print("\nLarge Files:")
                        for file_path, file_size in large_files:
                            print(f"    {file_path} - {format_size.format_size(file_size)}")
                            print()

                        delete_option = input("Do you want to delete large files (y/n)? ").lower()
                        if delete_option == "y":
                            delete_files_option = input("Do you want to delete files of a specific format (y/n)? ").lower()
                            if delete_files_option == 'y':
                                delete_format = input("Enter the file format to delete (e.g., .mp3, .jpg, .txt): ").lower()
                                delete_files_by_format.delete_files_by_format([file_path for file_path, _ in large_files], delete_format)
                            else:
                                for file_path, _ in large_files:
                                    try:
                                        os.remove(file_path)
                                        print(f"Deleted: {file_path}")
                                        print()
                                    except OSError as e:
                                        print(f"Error deleting {file_path}: {e}")
                    else:
                        print("No large files found.")
                elif option == 5:
                    format_to_delete = input("Enter the file format to delete (e.g., .mp3, .jpg, .txt): ").lower()
                    delete_files = []
                    for file_size, files in file_sizes.items():
                        for file_path in files:
                            file_format = os.path.splitext(file_path)[1].lower()
                            if file_format == format_to_delete:
                                delete_files.append(file_path)
                    if delete_files:
                        print(f"\nFiles with {format_to_delete} format:")
                        for file_path in delete_files:
                            print(f"    {file_path}")
                            print()

                        delete_files_response = input("Do you want to delete these files (y/n)? ").lower()
                        if delete_files_response == 'y':
                            delete_files_by_format.delete_files_by_format(delete_files, format_to_delete)
                    else:
                        print(f"No files found with {format_to_delete} format.")
                elif option == 6:
                    days_threshold = int(input("Enter the number of days threshold for rarely accessed files: "))
                    rarely_accessed_files = detect_rarely_accessed_files.detect_rarely_accessed_files(last_access_times, days_threshold)
                    if rarely_accessed_files:
                        print("\nRarely Accessed Files:")
                        for file_path in rarely_accessed_files:
                            print(f"    {file_path}")
                            print()

                        delete_rarely_accessed_response = input("Do you want to delete rarely accessed files (y/n)? ").lower()
                        if delete_rarely_accessed_response == "y":
                            delete_rarely_accessed_files.delete_rarely_accessed_files(rarely_accessed_files)
                    else:
                        print("No rarely accessed files found.")
                elif option == 7:
                    days_threshold = int(input("Enter the number of days threshold for rarely accessed files: "))
                    rarely_accessed_files = detect_rarely_accessed_files.detect_rarely_accessed_files(last_access_times, days_threshold)
                    if rarely_accessed_files:
                        print("\nRarely Accessed Files:")
                        for file_path in rarely_accessed_files:
                            print(f"    {file_path}")
                            print()

                        delete_rarely_accessed_response = input("Do you want to delete rarely accessed files (y/n)? ").lower()
                        if delete_rarely_accessed_response == "y":
                            delete_rarely_accessed_files.delete_rarely_accessed_files(rarely_accessed_files)
                    else:
                        print("No rarely accessed files found.")
                elif option == 8:
                    temp_files = detect_temp_files.detect_temp_files(file_sizes)
                    if temp_files:
                        print("\nTemporary Files:")
                        for file_path in temp_files:
                            print(f"    {file_path}")
                            print()

                        delete_temp_files_response = input("Do you want to delete temporary files (y/n)? ").lower()
                        if delete_temp_files_response == "y":
                            delete_temp_files.delete_temp_files(temp_files)
                    else:
                        print("No temporary files found.")
                elif option == 9:
                    temp_files = detect_temp_files.detect_temp_files(file_sizes)
                    if temp_files:
                        print("\nTemporary Files:")
                        for file_path in temp_files:
                            print(f"    {file_path}")
                            print()

                        delete_temp_files_response = input("Do you want to delete temporary files (y/n)? ").lower()
                        if delete_temp_files_response == "y":
                            delete_temp_files.delete_temp_files(temp_files)
                    else:
                        print("No temporary files found.")
                elif option == 10:
                    source_file = input("Enter the source file path: ").strip()
                    destination_dir = input("Enter the destination directory path: ").strip()
                    copy_data.copy_data(source_file, destination_dir)
                elif option == 11:
                    file_to_delete = input("Enter the file path to delete: ").strip()
                    delete_file_by_filepath.delete_file_by_filepath(file_to_delete)
                elif option == 12:
                    folder_to_delete = input("Enter the folder path to delete: ").strip()
                    delete_folder_by_directorypath.delete_folder_by_directorypath(folder_to_delete)
                else:
                    print("Invalid option. Please enter a valid option number.")
            except ValueError:
                print("Invalid input. Please enter a valid option number.")

if __name__ == "__main__":
    main()
