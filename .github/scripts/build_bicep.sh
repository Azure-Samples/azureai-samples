#!/bin/bash

echo "Running pre-commit hook for Bicep builds..."

# Find modified main.bicep files in the Agents/setup/ folder
MODIFIED_BICEP_FILES=$(find Agents/setup/ -type f -name "main.bicep")

if [ -z "$MODIFIED_BICEP_FILES" ]; then
    echo "No modified Bicep files detected. Skipping build."
    exit 0
fi

echo "Found modified Bicep files:"
echo "$MODIFIED_BICEP_FILES"

EXIT_CODE=0

# Loop through each modified Bicep file and build it
for BICEP_FILE in $MODIFIED_BICEP_FILES; do
    JSON_FILE="${BICEP_FILE%.bicep}.json"  # Change extension from .bicep to .json
    echo "Building: $BICEP_FILE -> $JSON_FILE"

    # Run Bicep build
    if ! bicep build "$BICEP_FILE" --outfile "$JSON_FILE"; then
        echo "Failed to build $BICEP_FILE"
        EXIT_CODE=1
    else
        # Stage the built JSON file for commit
        git add "$JSON_FILE"
    fi
done

# Abort commit if any Bicep file failed to compile
if [ "$EXIT_CODE" -ne 0 ]; then
    echo "Pre-commit hook failed. Fix Bicep errors before committing."
    exit 1
fi

echo "Bicep files successfully built and staged!"
exit 0
