import tkinter as tk
from tkinter import messagebox
import subprocess

def schedule_cron_task():
    """Reads user input, builds a cron expression, and updates the crontab."""
    command = command_entry.get().strip()
    minute = minute_entry.get().strip()
    hour = hour_entry.get().strip()
    day_of_month = day_month_entry.get().strip()
    month = month_entry.get().strip()
    day_of_week = day_week_entry.get().strip()

    # Basic input validation
    if not all([command, minute, hour, day_of_month, month, day_of_week]):
        messagebox.showerror("Input Error", "All fields must be filled to create a cron expression.")
        return

    # 1. Create the Cron Expression
    # Format: MIN HOUR DOM MON DOW COMMAND
    cron_expression = f"{minute} {hour} {day_of_month} {month} {day_of_week} {command}"

    # 2. Construct the Bash Command to Update Crontab
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
        # Check if the output suggests "no crontab"
        current_crontab = ""
        if current_crontab_result.returncode == 0:
            current_crontab = current_crontab_result.stdout
        elif "no crontab" not in current_crontab_result.stderr:
            # If it failed for a reason other than "no crontab for user"
            messagebox.showerror("Crontab Error", current_crontab_result.stderr.strip())
            return

        # Append the new job to the existing crontab
        new_crontab = current_crontab + f"\n{cron_expression}\n"

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
tk.Label(root, text="Bash Command to Run:", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')
command_entry = tk.Entry(root, width=50)
command_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
command_entry.insert(0, "/home/user/my_script.sh") # Example command

# --- Cron Expression Inputs ---
field_labels = ["Minute (0-59)", "Hour (0-23)", "Day of Month (1-31)", "Month (1-12)", "Day of Week (0-7)"]
default_values = ["0", "10", "*", "*", "*"] # Default is 10:00 AM daily

tk.Label(root, text="--- Cron Recurrence ---", font=('Arial', 10, 'bold')).grid(row=2, column=0, columnspan=2, pady=10)

input_entries = []
for i, label in enumerate(field_labels):
    tk.Label(root, text=label).grid(row=3, column=i, padx=1, sticky='w')

minute_entry = tk.Entry(root, width=8)
minute_entry.grid(row=4, column=0, padx=5)
minute_entry.insert(0, default_values[0])

hour_entry = tk.Entry(root, width=8)
hour_entry.grid(row=4, column=1, padx=5)
hour_entry.insert(0, default_values[1])

day_month_entry = tk.Entry(root, width=8)
day_month_entry.grid(row=4, column=2, padx=5)
day_month_entry.insert(0, default_values[2])

month_entry = tk.Entry(root, width=8)
month_entry.grid(row=4, column=3, padx=5)
month_entry.insert(0, default_values[3])

day_week_entry = tk.Entry(root, width=8)
day_week_entry.grid(row=4, column=4, padx=5)
day_week_entry.insert(0, default_values[4])


# --- Schedule Button ---
schedule_button = tk.Button(root, text="Add Cron Job", command=schedule_cron_task, font=('Arial', 12, 'bold'), bg='darkblue', fg='white')
schedule_button.grid(row=5, column=0, columnspan=5, pady=20)

# Start the Tkinter event loop
root.mainloop()