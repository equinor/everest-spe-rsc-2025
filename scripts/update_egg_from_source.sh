#!/bin/bash

# Check if the source directory is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <source_directory>"
    exit 1
fi

# Define the source and destination directories
SOURCE_DIR="$1"
DEST_DIR="./data/egg/eclipse/include/realizations"

for N in {1..10}; do

done


# Loop through numbers 1 to 100
for N in {1..10}; do
    REALIZATION_DIR="$DEST_DIR/realization-${(N-1)}"
    # Define the source and destination file paths
    SOURCE_FILE="$SOURCE_DIR/PERM${N}_ECL.INC"
    DEST_FILE="$REALIZATION_DIR/PERM.INC"
    
    # Copy the file from source to destination
    # cp "$SOURCE_FILE" "$DEST_FILE"
    
    echo "Copied $SOURCE_FILE to $DEST_FILE"
done

echo "Update completed."
