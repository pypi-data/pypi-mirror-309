#!/bin/bash

# Exit script on any error
set -e

# Determine target (test or production)
TARGET=${1:-test} # Default to "test" if no argument is passed
if [[ "$TARGET" == "prod" ]]; then
    REPOSITORY_URL="https://upload.pypi.org/legacy/"
    SECRET_KEY_NAME="pypi_api_key"
elif [[ "$TARGET" == "test" ]]; then
    REPOSITORY_URL="https://test.pypi.org/legacy/"
    SECRET_KEY_NAME="test_pypi_api_key"
else
    echo "Invalid target: $TARGET. Use 'test' or 'prod'."
    exit 1
fi

echo "Preparing package deployment to $TARGET..."

# Step 1: Ensure __init__.py Exists
if [ ! -f src/fiscus/__init__.py ]; then
    echo "__init__.py not found in src/fiscus. Creating an empty file..."
    touch src/fiscus/__init__.py
fi

# Step 2: Clean Previous Builds
echo "Cleaning up old build artifacts..."
rm -rf dist build .egg-info

# Step 3: Build the Package with Hatch
echo "Building the package with Hatch..."
hatch build

# Step 4: Read API Key from .secrets
if [ ! -f .secrets ]; then
    echo "Error: .secrets file not found!"
    exit 1
fi

# Extract the appropriate API key from the .secrets file
API_KEY=$(grep "$SECRET_KEY_NAME" .secrets | cut -d'=' -f2 | tr -d '[:space:]')

if [ -z "$API_KEY" ]; then
    echo "Error: $SECRET_KEY_NAME not found in .secrets file!"
    exit 1
fi

# Step 5: Publish the Package
echo "Publishing the package to $TARGET PyPI ($REPOSITORY_URL)..."
python -m twine upload --repository-url "$REPOSITORY_URL" dist/* -u __token__ -p "$API_KEY"

echo "Package published to $TARGET PyPI successfully!"
