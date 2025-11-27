#!/bin/bash
# A sample file that can end in an error. Used for testing.
# --- Failure Mechanism ---
RANDOM_NUM=$(( RANDOM % 100 ))

# Check if the random number is less than 50 (i.e., 50% chance)
if [ $RANDOM_NUM -lt 30 ]; then
    echo "--- FAILED RANDOMLY ---"
    echo "The script has randomly decided to fail (Random number: $RANDOM_NUM)."
    exit 1
fi

OUTPUT_DIR="/home/steve/Desktop/Systems_Programming_Project/sample_output"

BASE_NAME="hello_output"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${OUTPUT_DIR}/${BASE_NAME}_${TIMESTAMP}.txt"

mkdir -p "$OUTPUT_DIR"

echo "Hello" > "$OUTPUT_FILE"

echo "Successfully wrote 'Hello' to $OUTPUT_FILE"

exit 0