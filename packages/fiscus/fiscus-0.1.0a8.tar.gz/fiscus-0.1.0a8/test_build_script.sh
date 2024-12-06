#!/bin/bash

# Exit script on any error
set -e

echo "Preparing package deployment with Hatch..."

# Step 1: Ensure __init__.py Exists
echo "Ensuring src/fiscus/__init__.py exists..."
if [ ! -f src/fiscus/__init__.py ]; then
    echo "__init__.py not found in src/fiscus. Creating an empty file..."
    touch src/fiscus/__init__.py
fi

# Step 2: Clean Previous Builds
echo "Cleaning up old build artifacts..."
rm -rf dist build .egg-info

# Step 3: Uninstall Any Existing Version of Fiscus
echo "Uninstalling any existing version of fiscus..."
pip uninstall -y fiscus || true

# Step 4: Clear All __pycache__ Directories
echo "Clearing all __pycache__ directories..."
find . -name "__pycache__" -type d -exec rm -rf {} +

# Step 5: Verify Package Imports Correctly
echo "Testing import of fiscus before packaging..."
PYTHONPATH=src python -c "import fiscus" || { echo "Failed to import fiscus! Check your code."; exit 1; }

# Step 6: Build the Package with Hatch
echo "Building the package with Hatch..."
hatch build

# Step 7: Install and Test the Package in a Fresh Environment
echo "Installing and testing the package in a fresh virtual environment..."
python -m venv test_env
source test_env/bin/activate

# Ensure pip is installed and upgraded in the virtual environment
source test_env/bin/activate
python -m ensurepip --upgrade
pip install --upgrade pip

pip install --force-reinstall --no-cache-dir dist/*.whl
python -c "import fiscus; print(fiscus.__version__)"

# Step 9: Deactivate and Clean Up
echo "Deactivating and cleaning up the test environment..."
deactivate
# rm -rf test_env

echo "Build, installation, and test completed successfully!"
