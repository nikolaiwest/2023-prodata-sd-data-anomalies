import os
import json
import shutil

# Get name of all json files that contain the file names of the scenarios
path_02_01 = "data/02_surface-friction-x25/file-names_01_base-line.json"
path_02_02 = "data/02_surface-friction-x25/file-names_02_up-to-fifty.json"
path_02_03 = "data/02_surface-friction-x25/file-names_03_with-lubricant.json"
path_02_04 = "data/02_surface-friction-x25/file-names_04_sand-paper-40.json"
path_02_05 = "data/02_surface-friction-x25/file-names_05_sand-paper-400.json"

paths = [
    path_02_01,
    path_02_02,
    path_02_03,
    path_02_04,
    path_02_05,
]

# Source of the raw data to copy from
source_folder = "data/00_raw-data/"

# Iterated all selected paths and copy files to new sub folders
for path in paths:
    with open(path, "r") as json_file:
        # Get a list of JSON file names to be copied
        files_to_copy = json.load(json_file)

    # Set destination folders (Warning: only works for S2 at the moment!)
    destination_folder = f"{path[:29]}{path[40:-5]}"

    # Ensure the destination folder exists, create it if necessary
    os.makedirs(destination_folder, exist_ok=True)

    # Iterate through the list of files and copy them
    for file_name in files_to_copy:
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)

        try:
            # Use shutil.copy2 to preserve metadata (timestamps, etc.)
            shutil.copy2(source_path, destination_path)
            print(f"Successfully copied {file_name} to {destination_folder}")
        except FileNotFoundError:
            print(f"File {file_name} not found in {source_folder}")
        except PermissionError:
            print(f"Permission error while copying {file_name}")
        except Exception as e:
            print(f"Error copying {file_name}: {e}")
