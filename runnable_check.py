import os
import stat

def is_script_runnable(file_path):
    # Does file exist
    if not os.path.exists(file_path):
        return False

    file_stat = os.stat(file_path)
    # Can the file be run
    if bool(file_stat.st_mode & stat.S_IXUSR):
        return True
    else:
        # No execute permission
        return False