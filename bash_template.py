BASH_HEADER = """#!/bin/bash

MAX_RETRIES={MAX_TRIES}
RETRY_DELAY={WAIT_SECONDS}
PROJECT_DIR="{LOG_DIR}"

# Log File Configuration
LOG_FILE="$PROJECT_DIR/logging_file/workflow_system.log"
ADMIN_EMAIL="student@ontariotech.ca" 

log_message() {{
    local LEVEL=$1
    local MESSAGE=$2
    local TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    # Write to log file
    echo "[$TIMESTAMP] [$LEVEL] $MESSAGE" >> "$LOG_FILE"
    # Print to console so you can see it working
    echo "[$TIMESTAMP] [$LEVEL] $MESSAGE"
}}

send_notification() {{
    local SUBJECT=$1
    local BODY=$2
    if command -v mail &> /dev/null; then
        echo "$BODY" | mail -s "$SUBJECT" "$ADMIN_EMAIL"
    fi
}}

# This function allows us to run multiple tasks in a row
run_task_with_retry() {{
    local CMD="$1"
    local TASK_NAME="$2"
    local ATTEMPT=1
    local SUCCESS=0

    log_message "INFO" "--- STARTING TASK: $TASK_NAME ---"

    while [ $ATTEMPT -le $MAX_RETRIES ]; do
        
        # Execute the command
        # We use eval to handle arguments safely
        eval "$CMD"
        EXIT_CODE=$?
        
        if [ $EXIT_CODE -eq 0 ]; then
            log_message "INFO" "Task Success: $TASK_NAME"
            return 0
        else
            log_message "ERROR" "Task Failed: $TASK_NAME (Attempt $ATTEMPT/$MAX_RETRIES)"
            ((ATTEMPT++))
            if [ $ATTEMPT -le $MAX_RETRIES ]; then
                sleep $RETRY_DELAY
            fi
        fi
    done

    # If we exit the loop, it means all retries failed
    log_message "CRITICAL" "Workflow Aborted. $TASK_NAME failed all attempts."
    send_notification "Workflow Failure" "Task '$TASK_NAME' failed after $MAX_RETRIES attempts."
    exit 1
}}

log_message "INFO" "--- STARTING WORKFLOW ---"
"""