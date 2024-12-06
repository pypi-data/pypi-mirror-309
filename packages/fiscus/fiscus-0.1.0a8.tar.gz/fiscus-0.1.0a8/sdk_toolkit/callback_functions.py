# callback_functions.py

def on_fetch_categories(data):
    print("Fetched Categories:", data["available_categories"])

def on_category_selection(data):
    print("Selected Categories:", data["selected_categories"])

def on_fetch_connectors(data):
    print("Fetched Connectors:", data["available_connectors"])

def on_connector_selection(data):
    print("Selected Connectors:", data["selected_connectors"])

def on_fetch_operations(data):
    print("Fetched Operations:", data["available_operations"])

def on_operation_selection(data):
    print("Selected Operations:", data["selected_operations"])

def on_fetch_operation_details(data):
    print("Operation Details:", data["connectors_operations"])

def on_task_creation(data):
    print("Planned Tasks:", data["planned_tasks"])

# Uncomment this function if needed
# def on_auth_error(error):
#     print("Auth Error:", error['authorization_url'])
