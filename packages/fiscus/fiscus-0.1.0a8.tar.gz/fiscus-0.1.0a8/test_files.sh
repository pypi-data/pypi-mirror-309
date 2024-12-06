#!/bin/bash

# Directory containing your Python source files
SOURCE_DIR="src/fiscus"
OUTPUT_DIR="nuitka_test_output"

# Clean up previous test output
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Iterate through each Python file
echo "Testing each Python file in $SOURCE_DIR with Nuitka..."
for py_file in $(find "$SOURCE_DIR" -name "*.py"); do
    echo "Testing: $py_file"
    nuitka --module "$py_file" --output-dir="$OUTPUT_DIR" --nofollow-imports &> "$OUTPUT_DIR/$(basename $py_file).log"

    # Check if compilation succeeded
    if [ $? -ne 0 ]; then
        echo "Error compiling $py_file. See log: $OUTPUT_DIR/$(basename $py_file).log"
    else
        echo "Compiled successfully: $py_file"
    fi
done

echo "Testing completed. Check $OUTPUT_DIR for logs."
