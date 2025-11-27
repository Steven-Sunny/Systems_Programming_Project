#!/bin/bash
# A sample file that always runs. Used for testing.
OUTPUT_DIR="/home/steve/Desktop/Systems_Programming_Project/sample_output"

BASE_NAME="hello_output"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${OUTPUT_DIR}/${BASE_NAME}_${TIMESTAMP}.txt"

mkdir -p "$OUTPUT_DIR"

echo "Hello" > "$OUTPUT_FILE"

# Print a confirmation message (this goes to the cron job's mail log)
echo "Successfully wrote 'Hello' to $OUTPUT_FILE"