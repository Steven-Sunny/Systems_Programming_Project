import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # Needed for Tabs
import subprocess
import os

# Custom Imports
import runnable_check as rc
import retries_failure as rf
import get_project_directory as getp

def schedule_task(is_chain=False):
    """
    Unified scheduling function.
    is_chain=False -> Reads from the Single Task Entry.
    is_chain=True  -> Reads from the Workflow Listbox.
    """
    
    # 1. Gather Inputs
    minute = minute_entry.get().strip()
    hour = hour_entry.get().strip()
    day_of_month = day_month_entry.get().strip()
    month = month_entry.get().strip()
    day_of_week = day_week_entry.get().strip()
    r_seconds = r_seconds_entry.get().strip()
    r_number = r_number_tries.get().strip()

    # 2. Validate Inputs
    if not all([minute, hour, day_of_month, month, day_of_week, r_seconds, r_number]):
        messagebox.showerror("Error", "All timing and retry fields must be filled.")
        return

    try:
        if((int(r_seconds)<0 or int(r_seconds)>60) or (int(r_number) > 999 or int(r_number)<1)):
            messagebox.showwarning("Warning", "Values must be within bounds (0 - 60s and 1-999 attempts).")
            return
    except ValueError:
        messagebox.showerror("Error", "Retry values must be integers.")
        return

    r_sec_int = r_seconds
    r_num_int = r_number

    # 3. Determine Commands List
    commands_list = []
    
    if not is_chain:
        # Single Task Mode
        cmd = single_command_entry.get().strip()
        if not cmd:
            messagebox.showerror("Error", "Command field is empty.")
            return
        commands_list.append(cmd)
    else:
        # Chain Mode: Get all items from Listbox
        commands_list = list(chain_listbox.get(0, tk.END))
        if not commands_list:
            messagebox.showerror("Error", "Workflow list is empty. Add tasks first.")
            return

    # 4. Check Validity of Scripts
    for script in commands_list:
        if not rc.is_script_runnable(script):
            messagebox.showerror("Script Error", f"The script does not exist or is not executable:\n{script}")
            return

    # 5. Generate the Bash Wrapper (The "Bridge")
    # rf.retry_failures now handles lists!
    wrapper_script = rf.retry_failures(r_num_int, r_sec_int, commands_list)

    if not wrapper_script:
        messagebox.showerror("Error", "Failed to generate wrapper script.")
        return

    # 6. Schedule in Cron
    cron_expression = f"{minute} {hour} {day_of_month} {month} {day_of_week} {wrapper_script}"

    try:
        # Read current cron
        current_crontab_result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current_crontab = current_crontab_result.stdout if current_crontab_result.returncode == 0 else ""
        
        # Add new line
        new_crontab = current_crontab + f"{cron_expression}\n"

        # Write back
        p = subprocess.run(['crontab', '-'], input=new_crontab, text=True, capture_output=True)
        
        if p.returncode == 0:
            msg = "Single Task" if not is_chain else f"Chain of {len(commands_list)} Tasks"
            messagebox.showinfo("Success", f"{msg} Scheduled Successfully!\n\nCron Line:\n{cron_expression}")
        else:
            messagebox.showerror("Cron Error", p.stderr)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- UI Helper Functions for Chaining ---
def add_task_to_chain():
    cmd = chain_entry.get().strip()
    if cmd:
        if rc.is_script_runnable(cmd):
            chain_listbox.insert(tk.END, cmd)
            chain_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Invalid Script", "File not found or not executable.")
    else:
        messagebox.showwarning("Empty", "Please enter a script path.")

def remove_task_from_chain():
    selected_indices = chain_listbox.curselection()
    for i in reversed(selected_indices):
        chain_listbox.delete(i)

def clear_chain():
    chain_listbox.delete(0, tk.END)


# --- MAIN GUI SETUP ---
root = tk.Tk()
root.title("Advanced Task Scheduler")
root.geometry("700x550")

# 1. Header
tk.Label(root, text="System Project Scheduler", font=('Arial', 16, 'bold'), fg="darkblue").pack(pady=10)

# 2. Timing Frame (Shared by both Tabs)
# We put this outside the tabs because the Schedule applies to both logic types
timing_frame = tk.LabelFrame(root, text="Schedule Configuration (Cron & Retries)", padx=10, pady=10)
timing_frame.pack(padx=20, pady=5, fill="x")

# Grid layout for timing
lbls = ["Min", "Hour", "Day", "Month", "DayWeek", "Attempts", "Delay (s)"]
def_vals = ["*", "*", "*", "*", "*", "1", "0"]
entries = []

for i, txt in enumerate(lbls):
    tk.Label(timing_frame, text=txt, font=('Arial', 9)).grid(row=0, column=i, padx=5)
    e = tk.Entry(timing_frame, width=8)
    e.grid(row=1, column=i, padx=5)
    e.insert(0, def_vals[i])
    entries.append(e)

# Map entries to variable names for easy access
minute_entry, hour_entry, day_month_entry, month_entry, day_week_entry, r_number_tries, r_seconds_entry = entries

# 3. Tabs (The Split Section)
tab_control = ttk.Notebook(root)

# --- TAB 1: Single Task (Section 1) ---
tab1 = tk.Frame(tab_control)
tab_control.add(tab1, text='Single Task Reschedule')

tk.Label(tab1, text="Reschedule a Single Script", font=('Arial', 12, 'bold')).pack(pady=10)
tk.Label(tab1, text="Script Path:").pack(anchor="w", padx=20)
single_command_entry = tk.Entry(tab1, width=60)
single_command_entry.pack(padx=20, pady=5)
single_command_entry.insert(0, os.path.join(getp.get_proj_dir(), "sample_script.sh"))

btn_single = tk.Button(tab1, text="Schedule Single Task", bg="#dddddd", command=lambda: schedule_task(is_chain=False))
btn_single.pack(pady=20)

# --- TAB 2: Workflow Chain (Section 2) ---
tab2 = tk.Frame(tab_control)
tab_control.add(tab2, text='Workflow Chaining')

tk.Label(tab2, text="Chain Multiple Tasks (Sequential)", font=('Arial', 12, 'bold')).pack(pady=10)

# Chain Input Area
chain_input_frame = tk.Frame(tab2)
chain_input_frame.pack(fill="x", padx=20)

tk.Label(chain_input_frame, text="Add Script:").pack(side="left")
chain_entry = tk.Entry(chain_input_frame, width=40)
chain_entry.pack(side="left", padx=5)
tk.Button(chain_input_frame, text="+ Add", command=add_task_to_chain, bg="lightblue").pack(side="left")

# Listbox Area
list_frame = tk.Frame(tab2)
list_frame.pack(fill="both", expand=True, padx=20, pady=10)

chain_listbox = tk.Listbox(list_frame, height=8)
chain_listbox.pack(side="left", fill="both", expand=True)

# Scrollbar for listbox
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")
chain_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chain_listbox.yview)

# List Controls
btn_frame = tk.Frame(tab2)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Remove Selected", command=remove_task_from_chain, fg="red").pack(side="left", padx=10)
tk.Button(btn_frame, text="Clear All", command=clear_chain).pack(side="left", padx=10)

# Schedule Button for Chain
btn_chain = tk.Button(tab2, text="Schedule Workflow Chain", bg="green", fg="white", font=('Arial', 11, 'bold'), command=lambda: schedule_task(is_chain=True))
btn_chain.pack(pady=15)

tab_control.pack(expand=1, fill="both", padx=10, pady=10)

root.mainloop()