# sdk_tests/__init__.py

from .fiscus_config import client, user
from .gmail_operations import (
    add_gmail_connector,
    authenticate_gmail_connector,
    execute_gmail_get_email,
    execute_gmail_list_emails,
    execute_gmail_send_email
)
from .ai_execution import execute_ai_task
from .callback_functions import (
    on_fetch_categories,
    on_category_selection,
    on_fetch_connectors,
    on_connector_selection,
    on_fetch_operations,
    on_operation_selection,
    on_fetch_operation_details,
    on_task_creation
    # Uncomment if needed:
    # on_auth_error
)
from .additional_tests import (
    test_coinbase_authentication,
    test_coinbase_deauthentication,
    execute_plaid_task
)
