import os, shutil

# Directories and Filetypes
FILE_CATEGORIES = {
    "Images": (".jpg", ".png", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff", ".tif", ".HEIC"),
    "JSON": (".json", ".jsonc", ".geojson"),
    "Documents": (".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md", ".pages"),
    "PairDrop": "PairDrop_",
    "Archives": (".zip", ".rar", ".7z", ".tar", ".gz"),
    "Videos": (".mp4", ".mov", ".mkv", ".avi"),
    "Audio": (".mp3", ".wav", ".ogg", ".flac", ".m4a"),
    "Books": (".epub", ".mobi"),
    "Packages": (".deb", ".rpm", ".apk", ".exe", ".msi", ".dmg", ".pkg", ".appimage", ".jar", ".flatpak", ".snap"),
    "YML": (".yml", ".yaml"),
    "Excalidraw": (".excalidraw", ".excalidrawlib"),
    "Data": (".csv", ".tsv", ".xls", ".xlsx", ".sqlite", ".db", ".sql"),
    "HTML": (".html", ".htm"),
    "CSS": ".css",
    "Config": (".env", ".ini", ".cfg", ".conf", ".config", ".properties"),
    "Logs": (".log",),
    "RSS": (".rss", ".atom"),
}

def create_dir(directory):
    """
    Creates a directory if it does not already exist.
    
    Parameters
    ----------
    directory : str
        The name of the directory to create.
    """
    if not os.path.exists(directory):
        os.mkdir(directory)
        print(f"*****Created Directory: {directory}*****\n")
        

def move_files(files, directory, prefix=None):
    """
    Moves a list of files to a specified directory, optionally filtering by a prefix.

    Parameters
    ----------
    files : list
        A list of file names to be moved.
    directory : str
        The target directory where files should be moved. The directory will be created if it does not exist.
    prefix : str, optional
        A prefix to filter the files by. Only files starting with this prefix will be moved. If None, all files in the list are moved.

    Behavior
    --------
    - Creates the target directory if it does not exist and there are files to move.
    - Moves each file from the list to the specified directory.
    - Adds each successfully moved file to the global `files_moved` list.
    - Prints a message indicating the move for each file.
    - Catches and prints a message for `FileNotFoundError` if a file is not found.

    Note
    ----
    Ensure that `create_dir` and `shutil` are properly imported and that `files_moved` is defined globally.
    """
    if files:  
        create_dir(directory)
        for file in files:
            try:
                print(f"Moving {file} to {directory}")
                shutil.move(file, directory)
                files_moved.append(file)
            except FileNotFoundError:
                print(f"File not found: {file}")

files = [f for f in os.listdir('.') if os.path.isfile(f)]   # List Comprehension - iterates through all files in current directory while skipping directories

files_moved: list[str] = []

for directory, types in FILE_CATEGORIES.items():
    if directory == "PairDrop":
        pairdrop_files = [f for f in files if f.startswith("PairDrop_") and f.endswith(".zip")]
        move_files(pairdrop_files, "PairDrop", prefix=FILE_CATEGORIES["PairDrop"])
        files = [f for f in files if f not in pairdrop_files]
    else:
        sorted_files = [f for f in files if any(f.endswith(t) for t in types)]
        move_files(sorted_files, directory)
        files = [f for f in files if f not in sorted_files]

category_files: dict[str, list[str]] = {category: [] for category in FILE_CATEGORIES}

for file in files_moved:
    for category, types in FILE_CATEGORIES.items():
        if category == "PairDrop":
            if file.startswith("PairDrop_"):
                category_files[category].append(file)
                break
        elif any(file.endswith(t) for t in types):
            category_files[category].append(file)
            break

# Dictionary Comprehension - creates a dictionary with the number of files moved for each category and the files that were moved
report = {
    category: f"{len(files)} Files moved: {', '.join(files)}"
    for category, files in category_files.items() if files
} 

print("Summary of moved files:\n" + "-" * 25)
for category, count in report.items():
    print(f"{category}: {count}\n")


# Things to Fix - 
# 