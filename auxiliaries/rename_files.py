import os

path = "data/00_raw-data/"

# Get current name of all files as list
files = os.listdir(path)

# Iterate files and rename ".txt" to ".json"
for file in files:
    os.rename(
        os.path.join(path, file), os.path.join(path, "".join([str(file[:-4]), ".json"]))
    )
