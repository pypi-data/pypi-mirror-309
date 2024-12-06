
# from typing import Any, Dict
# from fiscus import (
# 	FiscusClient,
# 	FiscusUser,
# 	FiscusConnectionType,
# 	FiscusLogLevel,
# 	FiscusLLMType,
# 	FiscusAICategorySelection,
# 	FiscusAIFetchCategories,
#     FiscusCallbackType,
#     FiscusOnSuccess
# )
# from anthropic import Anthropic # type: ignore
# from openai import OpenAI # type: ignore

# # Initialize Fiscus client
# client = FiscusClient(
#     api_key='fiscus_production_394a5d73_f3cbabd01364dde698bea9bb8125d1f7cab7606c429d644ebc7869651a094e92',
#     logging_level=FiscusLogLevel.DEBUG
# )

# # Initialize Fiscus user for stateful environment
# user = FiscusUser(
#     user_id="12345",
#     client=client
# )

# anthropic_client = Anthropic(api_key="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")
# open_ai_client = OpenAI(api_key='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')

# # Define callback functions for various AI-driven steps
# def on_fetch_categories(data):
#     print("Fetched Categories:", data["available_categories"])

# def on_category_selection(data):
#     print("Selected Categories:", data["selected_categories"])

# def on_fetch_connectors(data):
#     print("Fetched Connectors:", data["available_connectors"])

# def on_connector_selection(data):
#     print("Selected Connectors:", data["selected_connectors"])

# def on_fetch_operations(data):
#     print("Fetched Operations:", data["available_operations"])

# def on_operation_selection(data):
#     print("Selected Operations:", data["selected_operations"])

# def on_fetch_operation_details(data):
#     print("Operation Details:", data["connectors_operations"])

# def on_task_creation(data):
#     print("Planned Tasks:", data["planned_tasks"])
    
# def on_auth_error(error):
#     print("Auth Error:", error['authorization_url'])


# response = client.execute_ai(
# 	input='What\'s the current price of bitcoin?',
# 	llm=anthropic_client,
#     # llm=open_ai_client,
# 	llm_type=FiscusLLMType.ANTHROPIC,
#     # llm_type=FiscusLLMType.OPENAI,
# 	user=user,
#     callbacks={
#         FiscusCallbackType.AI_FETCH_CATEGORIES: on_fetch_categories,
#         FiscusCallbackType.AI_CATEGORY_SELECTION: on_category_selection,
#         FiscusCallbackType.AI_FETCH_CONNECTORS: on_fetch_connectors,
#         FiscusCallbackType.AI_CONNECTOR_SELECTION: on_connector_selection,
#         FiscusCallbackType.AI_FETCH_OPERATIONS: on_fetch_operations,
#         FiscusCallbackType.AI_OPERATION_SELECTION: on_operation_selection,
#         FiscusCallbackType.AI_FETCH_OPERATION_DETAILS: on_fetch_operation_details,
#         FiscusCallbackType.AI_TASK_CREATION: on_task_creation
#     }
# )



# if response.success:
# 	print(response.data)
# else:
# 	print(response.error)

# Add a connector
# Synchronously set dynamic preferences
# preferences = {
#     "notifications": "enabled",
#     "language": "fr"
# }

# key = "language"
# value = "es"

# preferences = user.set_user_id('try')

# if preferences.success:
# 	print(preferences.result)
# 	print(preferences.data)
# else:
# 	print(preferences.error_message)

# connectors = user.list_connectors()
# print("Connected Connectors:", connectors.results)

# response = client.execute(
#     connector_name='plaid',
#     operation='get_balance',
#     user=user,
#     connection_type=FiscusConnectionType.REST,
#     params={
#          "client_id": "670eea8749f6f5001b6de324",
#     "secret": "1da6bc28ddb0c8bc353ace04d1c841",
#     "institution_id": "ins_20",
#     "initial_products": ["transactions"]
# 	},
#     callbacks={
#         FiscusCallbackType.ON_AUTH: on_auth_error
# 	}
#     # connection_type=FiscusConnectionType.REST
# )

# response = user.authenticate_connector('gmail')

# # print(response)

# if response.success:
# 	print(response.result)

# # Success callback that receives only result data
# def handle_success(data: Dict[str, Any]) -> None:
#     print(f"Operation successful! Data: {data}")

# # Error callback that receives the error message
# def handle_error(error_info: Dict[str, Any]) -> None:
#     print(f"Operation failed! Error: {error_info['error']}")

# Define tasks with their individual callbacks
# tasks = [
#     {
#         "connector": "coindesk",
#         "operation": "get_current_bitcoin_price",
#         "params": {},
#     },
#     {
#         "connector": "coindesk",
#         "operation": "get_current_bitcoin_price",
#         "params": {},
#     }
# ]

# # Execute a streaming operation
# response = client.execute(
#     tasks=tasks,
#     user=user,
#     # connection_type=FiscusConnectionType.REST,
# )


# # Check and print each task's response
# if response.success:
#     for idx, result in enumerate(response.results):
#         print(f"Operation {idx + 1} result: {result}")
# else:
#     print(f"Error: {response.error_message}")

# Keep the program running to maintain the WebSocket connection
# try:
#     while True:
#         # You can perform other tasks here or simply pass to keep the loop running
#         pass
# except KeyboardInterrupt:
#     # Handle graceful shutdown
#     client.stop_stream()
#     print("WebSocket connection closed.")

from __future__ import annotations
from anthropic import Anthropic
from anthropic.types import ToolParam, MessageParam
from fiscus import FiscusClient, FiscusUser, FiscusLogLevel

# Set up Anthropic and Fiscus clients
anthropic_client = Anthropic(api_key="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")
fiscus_client = FiscusClient(api_key='fiscus_production_394a5d73_f3cbabd01364dde698bea9bb8125d1f7cab7606c429d644ebc7869651a094e92', logging_level=FiscusLogLevel.DEBUG)
fiscus_user = FiscusUser(user_id="abc", client=fiscus_client)

# Define available tools with general tool parameters (examples included)
tools: list[ToolParam] = [
    {
        "name": "get_balance_and_transactions",
        "description": (
            "This tool securely fetches the user's bank account balance and transaction history for the purpose of analyzing "
            "spending patterns and providing budgeting advice. It has pre-configured access to authentication parameters, "
            "bank institution details, and permissions to retrieve transaction data. This tool will automatically pull the "
            "necessary information without requiring additional user input."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "client_id": {"type": "string", "description": "Client ID for pre-configured authentication"},
                "secret": {"type": "string", "description": "Secret for pre-configured authentication"},
                "institution_id": {"type": "string", "description": "The pre-configured Plaid institution ID"},
                "initial_products": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Initial products to use, such as transactions"
                }
            },
            "required": ["client_id", "secret", "institution_id", "initial_products"]
        }
    },
    {
        "name": "send_email",
        "description": (
            "This tool sends an email using a pre-configured Gmail account. It requires the subject and body of the email, "
            "and will automatically send to the user's registered email address."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "Subject of the email"},
                "body": {"type": "string", "description": "Body content of the email"},
            },
            "required": ["subject", "body"]
        }
    },
    # Add other tools here as needed
]

# Define a general tool executor function
def execute_tool(tool_name: str, params: dict):
    try:
        if tool_name == "get_balance_and_transactions":
            response = fiscus_client.execute(
                connector_name="plaid",
                operation="get_balance",
                user=fiscus_user,
                params=params
            )
            return response.result if isinstance(response.result, dict) else response.result[0]
        
        elif tool_name == "send_email":
            email_response = fiscus_client.execute(
                connector_name="gmail",
                operation="send_email",
                user=fiscus_user,
                params={"emailData": {
                    "headers": [
                        {"name": "To", "value": "hearsch@gmail.com"},
                        {"name": "From", "value": "dustin@fiscusflows.com"},
                        {"name": "Subject", "value": params['subject']}
                    ],
                    "body": {
                        "mimeType": "text/plain",
                        "data": params['body']
                    }
                }}
            )
            return email_response.result

        # Add more tool execution logic here for additional tools

    except Exception as e:
        print(f"Error executing tool {tool_name}: {e}")
        return None

# Function to handle messages and detect tool usage requests dynamically
def handle_model_response(message, user_message):
    if message.stop_reason == "tool_use":
        for tool_request in message.content:
            if tool_request.type == "tool_use" and tool_request.name:
                # Retrieve tool parameters if specified
                tool_name = tool_request.name
                params = tool_request.params or {}

                # Execute the requested tool
                tool_result = execute_tool(tool_name, params)

                # Check if tool execution was successful
                if tool_result is None:
                    print(f"No data retrieved from tool: {tool_name}")
                else:
                    # Format the result to send back to the model
                    response = anthropic_client.messages.create(
                        model="claude-3-5-sonnet-20240620",
                        max_tokens=1024,
                        messages=[
                            user_message,
                            {"role": message.role, "content": message.content},
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": tool_request.id,
                                        "content": [{"type": "text", "text": f"Tool result for {tool_name}: {tool_result}"}],
                                    }
                                ],
                            },
                        ],
                        tools=tools,
                    )
                    
                    # Process the response and handle next steps if needed
                    response_content = response.content[0].text.strip()
                    print(f"Response from model after {tool_name} execution: {response_content}")

                    # Optionally, trigger additional actions, like sending an email, if specified by the response
                    if tool_name == "get_balance_and_transactions":
                        # Send an email with the final advice from the model
                        send_email_subject = "Your Spending Pattern Analysis & Budgeting Advice"
                        send_email_body = f"Here is the advice based on your transactions data:\n\n{response_content}"
                        execute_tool("send_email", {"subject": send_email_subject, "body": send_email_body})

# Initial model message setup
user_message: MessageParam = {
    "role": "user",
    "content": "Can you analyze my spending patterns and provide some budgeting advice?"
}

# Initial interaction with the model
message = anthropic_client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    messages=[user_message],
    tools=tools,
)

print(f"Initial response from Claude: {message.model_dump_json(indent=2)}")

# Handle response and process tools
handle_model_response(message, user_message)
