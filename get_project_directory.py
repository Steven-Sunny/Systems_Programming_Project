from pathlib import Path
import os

# 1. Path(__file__) creates a Path object for the script's file.
# 2. .resolve() converts it to an absolute path, resolving any symlinks.
# 3. .parent gets the directory containing the file.
def get_proj_dir():
    script_directory = Path(__file__).resolve().parent

    # If you need it as a string instead of a Path object, use str():
    project_directory_string = str(script_directory)

    return project_directory_string