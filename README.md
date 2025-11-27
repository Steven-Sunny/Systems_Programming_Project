# 📅 GUI Cron Job Scheduler

A simple graphical user interface (GUI) application built with **Python's Tkinter** library to easily schedule new cron jobs on a Linux or macOS system. This scheduler not only sets up standard cron entries but also includes optional **retry logic** for the command being scheduled.


## ✨ Features

* **Interactive GUI:** User-friendly interface built with Tkinter.
* **Full Cron Schedule:** Allows input for all five standard cron fields (Minute, Hour, Day of Month, Month, Day of Week).
* **Command Input:** Easily specify the Bash script or command to be executed.
* **Retry Logic (Optional):** Define a maximum number of retries and an interval between retries for the command if its initial execution fails.
* **Crontab Integration:** Automatically checks the current crontab and appends the new job using the `crontab -` command.
* **Validation:** Basic validation for input bounds and mandatory fields.
* **User Email Save:** All cron tasks and their outcomes are posted by the cron daemon to the user's email. Available through the `mail` command.
* **Runnable Check:** Verifies if the specified command file exists and has execution permissions (via an external `runnable_check` module).


## 🛠️ Prerequisites

* **Python 3:** The application is written in Python 3.
* **Tkinter:** Usually bundled with standard Python installations.
* **Linux/macOS:** The `cron` and `crontab` command must be available on your operating system.

## 🚀 Installation and Setup

1.  **Download or Clone This GitHub Repo**

    Make sure to save check all files exist locally.

2.  **Run the Application:**

    ```bash
    python3 main.py
    ```

## 💻 Usage

### 1. Bash Command to Run

Enter the **full path** to the executable script or command you wish to schedule.

### 2. Cron Recurrence

Fill in the standard **five cron fields**. Use numbers, ranges (e.g., `1-5`), steps (e.g., `*/10`), or the asterisk (`*`) for "any value".

| Field | Range | Description | Default |
| :--- | :--- | :--- | :--- |
| **Minute** | 0-59 | Minute within the hour. | `*` (Every minute) |
| **Hour** | 0-23 | Hour of the day. | `*` (Every hour) |
| **Day of Month**| 1-31 | Day of the month. | `*` (Every day) |
| **Month** | 1-12 | Month of the year. | `*` (Every month) |
| **Day of Week** | 0-7 | Day of the week (0 and 7 are Sunday).| `*` (Every day) |

### 3. Cron Retries (Optional)

These fields configure the retry mechanism. Set **Max Tries** to **0** to disable retries.

| Field | Range | Description | Default |
| :--- | :--- | :--- | :--- |
| **Interval**| 0-60 | Time to wait **in seconds** before retrying the command. | `0` |
| **Max Tries** | 0-99 | The **total** number of times the command should attempt to run (including the first attempt). | `0` |

### 4. Scheduling

Click the **Add Cron Job** button. The application will attempt to add the entry to your user's crontab and provide feedback on success or failure through cron emails.

## 🛑 How the Cron Job is Scheduled

The application updates the crontab by:

1.  Fetching the current active crontab using `crontab -l`.
2.  Constructing the new cron job line (using the `rf.retry_failures` function if retries are enabled).
3.  Combining the old crontab content and the new cron job.
4.  Piping the entire new content back to the `crontab` command: `echo new_crontab_content | crontab -`.

This method ensures that existing cron jobs are preserved.