#!/bin/bash

echo "Running pre-commit hook for Bicep builds..."

# Ensure shell profile is sourced to load environment variables
source ~/.bashrc || source ~/.bash_profile || source ~/.zshrc

# Function to manually install Bicep if az bicep install fails
install_bicep_manually() {
    echo "⚠️  Trying to manually install Bicep..."

    # Create install directory
    INSTALL_PATH="$RUNNER_TEMP/bicep"
    BICEP_PATH="$INSTALL_PATH/bicep"
    mkdir -p $INSTALL_PATH

    # Fetch the latest Bicep CLI binary
    OS=$(uname -s)
    case "$OS" in
        Linux)
            echo "🔹 Detected Linux. Installing Bicep..."
            curl -sLo bicep https://github.com/Azure/bicep/releases/latest/download/bicep-linux-x64
            ;;
        Darwin)
            echo "🔹 Detected macOS. Installing Bicep..."
            curl -sLo bicep https://github.com/Azure/bicep/releases/latest/download/bicep-osx-x64
            ;;
        CYGWIN*|MINGW*|MSYS*)
            echo "🔹 Detected Windows. Installing Bicep..."
            curl -sLo bicep.exe https://github.com/Azure/bicep/releases/latest/download/bicep-win-x64.exe
            mv bicep.exe "$INSTALL_PATH/bicep.exe"
            ;;
        *)
            echo "❌ Unsupported OS: $OS"
            exit 1
            ;;
    esac

    chmod +x ./bicep
    sudo mv ./bicep $INSTALL_PATH
    export PATH="$INSTALL_PATH:$PATH"

    echo "✅ Using Bicep at $BICEP_PATH"
    $BICEP_PATH --version
}

# Check if Bicep CLI is installed
if ! command -v bicep &> /dev/null; then
    echo "⚠️  Bicep CLI is not installed. Trying to install via Azure CLI..."

    # Attempt installation via Azure CLI
    az bicep install || install_bicep_manually

    # Refresh environment
    export PATH="$HOME/.azure/bin:$PATH"
    source ~/.bashrc || source ~/.bash_profile || source ~/.zshrc
fi

echo "✅ Bicep CLI is installed: $(which bicep)"

# Find modified main.bicep files in the Agents/setup/ folder
REPO_ROOT=$(git rev-parse --show-toplevel)  # Get the repo root directory
MODIFIED_BICEP_FILES=$(git diff --cached --name-only | find "$REPO_ROOT/scenarios/Agents/setup/" -type f -name "main.bicep")

if [ -z "$MODIFIED_BICEP_FILES" ]; then
    echo "No modified Bicep files detected. Skipping build."
    exit 0
fi

echo "Found modified Bicep files:"
echo "$MODIFIED_BICEP_FILES"

EXIT_CODE=0

# Loop through each modified Bicep file and build it
for BICEP_FILE in $MODIFIED_BICEP_FILES; do
    BICEP_DIR=$(dirname "$BICEP_FILE")  # Get directory of main.bicep
    JSON_FILE="$BICEP_DIR/azuredeploy.json"  # Force output to azuredeploy.json
    echo "Building: $BICEP_FILE -> $JSON_FILE"

    # Run Bicep build
     if ! bicep build "$BICEP_FILE" --outfile "$JSON_FILE" 2>&1 | tee /tmp/bicep_error.log; then
        echo "❌ Failed to build $BICEP_FILE"
        cat /tmp/bicep_error.log
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