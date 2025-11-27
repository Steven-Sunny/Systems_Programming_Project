import time
import os
import stat
import bash_template as bt
from pathlib import Path

import get_project_directory as getp

def retry_failures(tries=0, interval=0, commands=[]):
    """
    Args:
        tries (int): Max retries per task.
        interval (int): Seconds between retries.
        commands (list or str): A list of strings ["/path/a", "/path/b"] OR a single string.
    """

    if isinstance(commands, str):
        commands = [commands]
    
    # If the list is empty, return None to avoid errors
    if not commands:
        return None

    localdirectory = getp.get_proj_dir()
    
    config_values = {
        "MAX_TRIES": tries,
        "WAIT_SECONDS": interval,
        "LOG_DIR": localdirectory
    }
    
    script_content = bt.BASH_HEADER.format(**config_values)


    for cmd in commands:

        cmd_safe = cmd.replace('"', '\\"') 
        task_name = os.path.basename(cmd)
        
        # Add the line that runs the specific task
        script_content += f'\nrun_task_with_retry "{cmd_safe}" "{task_name}"'

    # 3. Append Footer (Success message)
    script_content += '\n\nlog_message "INFO" "--- WORKFLOW COMPLETED SUCCESSFULLY ---"\nexit 0'

    try:
        first_task_path = Path(commands[0])
        first_task_name = first_task_path.stem 
    except:
        first_task_name = "unknown_task"
        
    cur_time = time.time()
    
    scripts_dir = os.path.join(localdirectory, "retry_scripts")
    logging_dir = os.path.join(localdirectory, "logging_file")
    
    # Unique filename so multiple schedules don't overwrite each other
    script_filename = f"chain_{first_task_name}_{int(cur_time)}.sh"
    output_filename = os.path.join(scripts_dir, script_filename)
    
    try:
        os.makedirs(scripts_dir, exist_ok=True)
        os.makedirs(logging_dir, exist_ok=True)

        with open(output_filename, "w") as f:
            f.write(script_content)

        # Make the generated script executable
        os.chmod(output_filename, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        
        return output_filename
    
    except Exception as e:
        print(f"Error creating script: {e}")
        return None