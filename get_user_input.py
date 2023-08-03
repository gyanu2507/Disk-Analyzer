import os

def get_user_input():
    # Ask the user to enter the folder path
    directories = []
    print("Enter the folder paths you want to analyze (press Enter to proceed):")

    directory = input().strip()
    if not directory:
        print("No folder paths provided. Exiting...")
        return directories
    if os.path.exists(directory):
        directories.append(directory)
    else:
        print("Invalid folder path. Please enter a valid path.")
    return directories