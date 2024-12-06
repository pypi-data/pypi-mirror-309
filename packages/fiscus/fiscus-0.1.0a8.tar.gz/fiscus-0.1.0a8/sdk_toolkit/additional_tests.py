# additional_tests.py
import sys
import os

# Add the 'src' directory to the Python path for access to the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from .fiscus_config import user, client

def test_coinbase_authentication():
    response = user.authenticate_connector('coindesk')
    if response.success:
        print(response.data)
    else:
        print(response.error.message)

def test_coinbase_deauthentication():
    response = user.deauthenticate_connector('coindesk')
    if response.success:
        print(response.data)
    else:
        print(response.error.message)

def execute_plaid_task():
    response = client.execute(
        connector_name='plaid',
        operation='get_balance',
    )
    if response.success:
        print(response.data)
    else:
        print(response.error.message)
