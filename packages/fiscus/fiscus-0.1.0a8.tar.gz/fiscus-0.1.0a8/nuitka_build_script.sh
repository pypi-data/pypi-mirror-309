#!/bin/bash

# Exit script on any error
set -e

# Step 1: Ensure __init__.py Exists
echo "Ensuring src/fiscus/__init__.py exists..."
if [ ! -f src/fiscus/__init__.py ]; then
    echo "__init__.py not found in src/fiscus. Creating an empty file..."
    touch src/fiscus/__init__.py
fi

# Step 2: Clean Previous Builds and Nuitka Cache
echo "Cleaning previous builds and Nuitka cache..."
rm -rf dist build obfuscated_package obfuscated_output .nuitka-cache

# Step 3: Uninstall Any Existing Version of Fiscus
echo "Uninstalling any existing version of fiscus..."
pip uninstall -y fiscus || true

# Step 4: Clear All __pycache__ Directories
echo "Clearing all __pycache__ directories..."
find . -name "__pycache__" -type d -exec rm -rf {} +

# Step 5: Compile Each Python File in the Fiscus Package with Nuitka
echo "Compiling fiscus package files with Nuitka..."

for py_file in $(find src/fiscus -name "*.py" -not -name "__init__.py"); do
    nuitka --module "$py_file" --output-dir=obfuscated_output --nofollow-imports
done

# Step 6: Verify Obfuscated Output Structure
echo "Verifying that compiled files exist in obfuscated_output..."
compiled_files_count=$(find obfuscated_output -name "*.so" | wc -l)
if [ "$compiled_files_count" -eq 0 ]; then
    echo "Error: No compiled modules found in obfuscated_output. Please check Nuitka configuration."
    exit 1
fi
echo "Compiled files verified."

# Step 7: Prepare Package Directory
echo "Preparing package directory structure..."
mkdir -p obfuscated_package/src/fiscus

# Step 8: Copy Essential Files
echo "Copying setup.py, LICENSE, and README.md to the package directory..."
cp setup.py LICENSE README.md obfuscated_package/

# Step 9: Copy All Compiled Modules and Ensure Directory Structure
echo "Copying compiled modules into the package directory..."
cp -R obfuscated_output/* obfuscated_package/src/fiscus/

# Step 10: Copy __init__.py
echo "Copying __init__.py to the package directory..."
cp src/fiscus/__init__.py obfuscated_package/src/fiscus/

# Step 11: Double-check Package Structure in obfuscated_package/src/fiscus
echo "Verifying directory structure in obfuscated_package/src/fiscus..."
tree obfuscated_package/src/fiscus || ls -R obfuscated_package/src/fiscus

# Step 12: Build the Package
echo "Building the package..."
cd obfuscated_package
python setup.py sdist bdist_wheel

# Step 13: Install and Test the Package in a Fresh Environment
echo "Installing and testing the package in a fresh virtual environment..."
cd ..
python -m venv test_env
source test_env/bin/activate

pip install --force-reinstall --no-cache-dir obfuscated_package/dist/*.whl
python -c "import fiscus; print(fiscus.__version__)"

# Step 14: Run Additional Tests
echo "Running additional tests..."
cat > test_fiscus.py << EOF
from fiscus import FiscusClient, FiscusLogLevel, FiscusConnectionType, FiscusFile

client = FiscusClient(
    api_key='fiscus_production_394a5d73_f3cbabd01364dde698bea9bb8125d1f7cab7606c429d644ebc7869651a094e92',
    user_id='1234',
    logging_level=FiscusLogLevel.DEBUG,
)

response = client.execute(
    connector_name='office_365',
    operation='get_task_lists',
)

if response.success:
    print(response.data)
else:
    print(response.error_message)
EOF

python test_fiscus.py
rm test_fiscus.py

# Step 15: Deactivate and Clean Up
echo "Deactivating and cleaning up the test environment..."
deactivate
# rm -rf test_env

echo "Build, installation, and test completed successfully!"
