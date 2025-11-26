#!/bin/bash

# Define the directory where the output should always go
OUTPUT_DIR="/home/vboxuser/Desktop/Systems_Programming_Project/sample_output"

# --- Original code modified ---
BASE_NAME="hello_output"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${OUTPUT_DIR}/${BASE_NAME}_${TIMESTAMP}.txt"

# Make sure the directory exists before writing (good practice)
mkdir -p "$OUTPUT_DIR"

# Write the output
echo "Hello" > "$OUTPUT_FILE"

# Print a confirmation message (this goes to the cron job's mail log)
echo "Successfully wrote 'Hello' to $OUTPUT_FILE"