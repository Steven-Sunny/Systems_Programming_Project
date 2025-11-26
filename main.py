import tkinter as tk
from tkinter import messagebox
import subprocess

import runnable_check as rc
import retries_failure as rf

def schedule_cron_task():
    """Reads user input, builds a cron expression, and updates the crontab."""
    command = command_entry.get().strip()
    minute = minute_entry.get().strip()
    hour = hour_entry.get().strip()
    day_of_month = day_month_entry.get().strip()
    month = month_entry.get().strip()
    day_of_week = day_week_entry.get().strip()

    r_seconds = r_seconds_entry.get().strip()
    r_number = r_number_tries.get().strip()
    
    # Basic input validation
    if not all([r_seconds, r_number]):
        messagebox.showerror("Input Error", "All fields must be filled to create a retry expression.")
        return
    try:
        if(int(r_seconds)>60 or int(r_seconds)<1 and int(r_number)>99 or int(r_number)<0):
            messagebox.showwarning("Input Bounds", "All values have to be within bounds.")
            return
    except ValueError:
        messagebox.showerror("Input Error", "Please enter an integer value.")
        return
    
    if not all([command, minute, hour, day_of_month, month, day_of_week]):
        messagebox.showerror("Input Error", "All fields must be filled to create a cron expression.")
        return

    # Format: MIN HOUR DOM MON DOW COMMAND
    cron_expression = f"{minute} {hour} {day_of_month} {month} {day_of_week} {command}"
    #print (cron_expression)

    # Check file path and execution permissions
    if (not rc.is_script_runnable(command)):
        messagebox.showerror("Script cannot be run", "Check file path and execution permission.")
    else: 
        try:
            # Get the current crontab entries
            # Use subprocess.run to capture the current crontab safely
            current_crontab_result = subprocess.run(
                ['crontab', '-l'], 
                capture_output=True, 
                text=True, 
                check=False  # Allow non-zero exit code if crontab is empty
            )
            
            # If the crontab is empty, subprocess.run(['crontab', '-l']) might return an error
            current_crontab = ""
            if current_crontab_result.returncode == 0:
                current_crontab = current_crontab_result.stdout
            elif "no crontab" not in current_crontab_result.stderr:
                # If it failed for a reason other than "no crontab for user"
                messagebox.showerror("Crontab Error", current_crontab_result.stderr.strip())
                return

            if(int(r_number) == 0):
                # Append the new job to the existing crontab
                new_crontab = current_crontab + f"\n{cron_expression}\n"
            else:
                # Append the new job with retries to the existing crontab
                new_crontab = current_crontab + rf.retry_failures(r_number, r_seconds, command)

            # Write the new combined crontab back using a pipe
            p1 = subprocess.Popen(['echo', new_crontab], stdout=subprocess.PIPE, text=True)
            p2 = subprocess.Popen(['crontab', '-'], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            p1.stdout.close() # Allow p1 to receive a SIGPIPE if p2 exits
            
            # Wait for p2 to finish and get the output
            stdout, stderr = p2.communicate()
            
            if p2.returncode == 0:
                messagebox.showinfo("Success", f"Cron job scheduled successfully:\n{cron_expression}")
            else:
                messagebox.showerror("Scheduling Error", f"Failed to update crontab:\n{stderr.strip()}")

        except FileNotFoundError:
            messagebox.showerror("Error", "The 'crontab' command was not found.")
        except Exception as e:
            messagebox.showerror("General Error", f"An unexpected error occurred: {e}")

# --- GUI Setup ---

# Create the main window
root = tk.Tk()
root.title("Bash Cron Job Scheduler")

# --- Command Input ---
tk.Label(root, text="Bash Command to Run:", font=('Arial', 10, 'bold')).grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky='w')
command_entry = tk.Entry(root, width=50)
command_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
command_entry.insert(0, "/home/vboxuser/Desktop/Systems_Programming_Project/sample_script.sh") # Starter command

# --- Cron Expression Inputs ---
field_labels = ["Minute (0-59)", "Hour (0-23)", "Day of Month (1-31)", "Month (1-12)", "Day of Week (0-7)"]
retry_labels = ["Interval (0-60)", "Max Tries (0-99)"]
retry_values = ["0", "0"] # Default is 0 retries
default_values = ["*", "*", "*", "*", "*"] # Default is every minute

cron_frame = tk.Frame(root, padx=10, pady=10, relief=tk.GROOVE, borderwidth=2)

retry_frame = tk.Frame(root, padx=10, pady=10, relief=tk.GROOVE, borderwidth=2)

cron_frame.grid(row=0, column=0, padx=10, pady=10)

retry_frame .grid(row=1, column=0, padx=10, pady=10)

input_entries = []
retry_entries = []

# Cron frame
# Loop to create the labels inside the frame
# # Add the title Label inside the frame
tk.Label(cron_frame, text="--- Cron Recurrence ---", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=5, pady=10)
for i, label in enumerate(field_labels):
    # Note: Using cron_frame as the parent for the Label
    tk.Label(cron_frame, text=label).grid(row=1, column=i, padx=1, sticky='w')

minute_entry = tk.Entry(cron_frame, width=8)
minute_entry.grid(row=2, column=0, padx=5)
minute_entry.insert(0, default_values[0])
input_entries.append(minute_entry)

hour_entry = tk.Entry(cron_frame, width=8)
hour_entry.grid(row=2, column=1, padx=5)
hour_entry.insert(0, default_values[1])
input_entries.append(hour_entry)

day_month_entry = tk.Entry(cron_frame, width=8)
day_month_entry.grid(row=2, column=2, padx=5)
day_month_entry.insert(0, default_values[2])
input_entries.append(day_month_entry)

month_entry = tk.Entry(cron_frame, width=8)
month_entry.grid(row=2, column=3, padx=5)
month_entry.insert(0, default_values[3])
input_entries.append(month_entry)

day_week_entry = tk.Entry(cron_frame, width=8)
day_week_entry.grid(row=2, column=4, padx=5)
day_week_entry.insert(0, default_values[4])
input_entries.append(day_week_entry)

#retries
tk.Label(retry_frame, text="--- Cron Retries---", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=5, pady=10)
for i, label in enumerate(retry_labels):
    tk.Label(retry_frame, text=label).grid(row=1, column=i, padx=1, sticky='w')

r_seconds_entry = tk.Entry(retry_frame, width=8)
r_seconds_entry.grid(row=2, column=0, padx=5)
r_seconds_entry.insert(0, retry_values[0])
retry_entries.append(r_seconds_entry)

r_number_tries = tk.Entry(retry_frame, width=8)
r_number_tries.grid(row=2, column=1, padx=5)
r_number_tries.insert(0, retry_values[1])
retry_entries.append(r_number_tries)

# --- Schedule Button ---
schedule_button = tk.Button(root, text="Add Cron Job", command=schedule_cron_task, font=('Arial', 12, 'bold'), bg='darkblue', fg='white')
schedule_button.grid(row=5, column=0, columnspan=5, pady=20)

# Start the Tkinter event loop
root.mainloop()