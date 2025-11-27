import time
import os
import bash_template as bt
from pathlib import Path

import get_project_directory as getp

new_template = bt.BASH_TEMPLATE

def retry_failures (tries=0, interval=0, command="/home/user/my_script.sh"):

    localdirectory = getp.get_proj_dir()
    config_values = {
        "MAX_TRIES": tries,
        "WAIT_SECONDS": interval,
        "COMMAND_TO_RUN": command,
        "LOG_DIR": localdirectory,
        "TIMESTAMP": int(time.time())
    }
    generated_script_content = new_template.format(**config_values)

    # Get path name
    path_string = command
    path_obj = Path(path_string)
    script_name_noext = path_obj.stem

    # Create new path
    cur_time = time.time()
    output_directory = "./retry_scripts/" 
    output_filename = "./retry_scripts/" + script_name_noext + "_retry_" + str(tries) + "_" + str(interval) + "_" + str(cur_time) + "_.sh"
    executable_filename = localdirectory + "/retry_scripts/" + script_name_noext + "_retry_" + str(tries) + "_" + str(interval) + "_" + str(cur_time) + "_.sh"
    
    try:
        # Make new directory for scripts
        os.makedirs(output_directory, exist_ok = True)

        # Make new directory for logging
        os.makedirs("./logging_file/", exist_ok = True)

        # Open/Create file for Writing
        with open(output_filename, "w") as f:
            f.write(generated_script_content)

        
        os.chmod(output_filename, 0o755)
        return executable_filename
    
    except Exception as e:
        return None