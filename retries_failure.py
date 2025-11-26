import time
import os
import bash_template as bt
from pathlib import Path

new_template = bt.BASH_TEMPLATE

def retry_failures (tries=0, interval=0, command="/home/user/my_script.sh"):
    config_values = {
        "MAX_TRIES": tries,
        "WAIT_SECONDS": interval,
        "COMMAND_TO_RUN": command,
        "TIMESTAMP": int(time.time())
    }
    generated_script_content = new_template.format(**config_values)

    # Get path name
    path_string = command
    path_obj = Path(path_string)
    script_name_noext = path_obj.stem

    # Create new path
    output_directory = "./retry_scripts/" 
    output_filename = "./retry_scripts/" + script_name_noext + "_retry_" + str(tries) + "_" + str(interval) + "_" + str(time.time()) + "_.sh"
    
    try:
        # Make new directory for scripts
        os.makedirs(output_directory, exist_ok = True)

        # Open/Create file for Writing
        with open(output_filename, "w") as f:
            f.write(generated_script_content)

        
        os.chmod(output_filename, 0o755)
        return output_filename
    
    except Exception as e:
        return None

retry_failures()