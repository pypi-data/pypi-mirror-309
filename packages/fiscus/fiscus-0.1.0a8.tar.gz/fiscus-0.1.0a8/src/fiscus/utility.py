# fiscus_sdk/utils.py

from typing import Any, List
import os
import base64

from .fiscus_file import FiscusFile

MAX_SIZE_MB = 10  # Maximum allowed size in MB
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024  # Convert MB to bytes

def validate_params(params: dict) -> bool:
    """
    Validate parameters before execution.

    :param params: Parameters to validate.
    :return: True if valid, False otherwise.
    """
    
    # Accept empty params as valid
    # if params is None:
    #     return True
    if not isinstance(params, dict):
        return False
    if not params:
        return False
    # Additional checks can be added here
    # For instance, checking required keys, value types, etc.
    return True

# Helper function to mask sensitive information
def _mask_sensitive_info(data: Any) -> Any:
    """
    Helper function to mask sensitive information in logs.
    """
    if isinstance(data, dict):
        data = data.copy()
        for key in data:
            if any(sensitive_word in key.lower() for sensitive_word in ['token', 'secret', 'password', 'api_key']):
                data[key] = '****'
    return data

# Helper function to process files
def _process_files(files: List[FiscusFile]) -> List[FiscusFile]:
    processed_files = []
    total_size = 0  # Initialize total size counter

    for file in files:
        content = file['content']

        # Check if `content` is a file path (and the file exists)
        if isinstance(content, str) and os.path.isfile(content):
            # Get file size and check against limit
            file_size = os.path.getsize(content)
            total_size += file_size
            if total_size > MAX_SIZE_BYTES:
                raise ValueError("Total size of files exceeds the 10 MB limit.")

            # Read and base64-encode the file content
            with open(content, 'rb') as f:
                file_content = f.read()
            encoded_content = base64.b64encode(file_content).decode('utf-8')
            file['content'] = encoded_content  # Update with encoded content

        elif isinstance(content, bytes):
            # Content is binary data, base64 encode it directly
            encoded_content = base64.b64encode(content).decode('utf-8')
            file['content'] = encoded_content

        else:
            # Assume content is already a text string to be encoded
            encoded_content = base64.b64encode(content.encode()).decode('utf-8')
            file['content'] = encoded_content

        processed_files.append(file)

    return processed_files