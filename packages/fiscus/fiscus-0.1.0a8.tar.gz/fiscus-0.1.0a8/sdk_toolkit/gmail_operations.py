# gmail_operations.py
import sys
import os

# Add the 'src' directory to the Python path for access to the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from .fiscus_config import user, client

# Step 2: Add a connector (e.g., Gmail)
def add_gmail_connector():
    user.add_connector('gmail')

# Step 3: Authenticate the connector (if required)
def authenticate_gmail_connector():
    connector_response = client.user.authenticate_connector('gmail')
    if connector_response.success:
        print(connector_response.data)
    else:
        print(connector_response.error.code.value)
            
# Execute different Gmail tasks
def execute_gmail_get_email():
    response = client.execute(
        connector_name='gmail',
        operation='get_email',
        params={"id": "192f61d0b74bb32f"}
    )
    if response.success:
        print(response.data)
    else:
        print(response.error.message)

def execute_gmail_list_emails():
    response = client.execute(
        connector_name='gmail',
        operation='list_emails',
        params={"maxResults": 20}
    )
    if response.success:
        print(response.data)
    else:
        print(response.error.message)

def execute_gmail_send_email():
    response = client.execute(
        connector_name='gmail',
        operation='send_email',
        params={
            "emailData": {
                "headers": [
                    {"name": "To", "value": "chronorhc@gmail.com"},
                    {"name": "From", "value": "dustin@fiscusflows.com"},
                    {"name": "Subject", "value": "Test Email"}
                ],
                "body": {
                    "mimeType": "text/plain",
                    "data": "Hello, this is a test email sent via API."
                }
            }
        }
    )
    if response.success:
        print(response.data)
    else:
        print(response.error.message)
