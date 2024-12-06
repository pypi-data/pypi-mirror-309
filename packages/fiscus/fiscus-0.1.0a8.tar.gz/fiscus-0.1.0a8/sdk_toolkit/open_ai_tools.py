from __future__ import annotations
from anthropic import Anthropic
from anthropic.types import ToolParam, MessageParam
from fiscus import FiscusClient, FiscusUser, FiscusLogLevel

# Set up Anthropic and Fiscus clients
anthropic_client = Anthropic(api_key="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")
fiscus_client = FiscusClient(api_key='fiscus_production_394a5d73_f3cbabd01364dde698bea9bb8125d1f7cab7606c429d644ebc7869651a094e92', logging_level=FiscusLogLevel.DEBUG)
fiscus_user = FiscusUser(user_id="abc", client=fiscus_client)

# Define available tools with general tool parameters (examples included)
# Define available tools with minimal configuration
tools = [
    {
        "name": "get_balance_and_transactions",
        "description": (
            "Fetches the user's bank account balance and transaction history for analyzing spending patterns."
        ),
        "connector_name": "plaid",
        "operation": "get_balance"
    },
    {
        "name": "send_email",
        "description": (
            "Sends an email using a pre-configured Gmail account. Automatically sends to the user's registered email."
        ),
        "connector_name": "gmail",
        "operation": "send_email"
    },
    # Additional tools can be added here
]

# Function to execute a tool based on connector name and operation
def execute_tool(tool_name: str):
    # Look up the tool configuration
    tool = next((t for t in tools if t["name"] == tool_name), None)
    if not tool:
        print(f"Tool {tool_name} not found.")
        return None
    
    try:
        response = fiscus_client.execute(
            connector_name=tool["connector_name"],
            operation=tool["operation"],
            user=fiscus_user
        )
        return response.result if isinstance(response.result, dict) else response.result[0]

    except Exception as e:
        print(f"Error executing tool {tool_name}: {e}")
        return None

# Function to handle and process the model's response
def handle_model_response(message, user_message):
    while message.stop_reason == "tool_use":
        # Process each tool request in sequence, if any
        for tool_request in message.content:
            if tool_request.type == "tool_use" and tool_request.name:
                # Execute the requested tool and capture the result
                tool_result = execute_tool(tool_request.name)

                # Check if tool execution was successful
                if tool_result is None:
                    print(f"No data retrieved from tool: {tool_request.name}")
                    continue  # Move to the next tool or stop if none left

                # Format the tool result and send it back to the model
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
                                    "content": [{"type": "text", "text": f"Tool result for {tool_request.name}: {tool_result}"}],
                                }
                            ],
                        },
                    ],
                    tools=tools,
                )

                # Process the response
                response_content = response.content[0].text.strip()
                print(f"Response from model after {tool_request.name} execution: {response_content}")

                # Set the message to the new response for the next iteration
                message = response

                # Break out of the for-loop and re-check the new message for further tool requests
                break

        # If there are no more tool requests, stop the loop
        if message.stop_reason != "tool_use":
            print("Model indicates it has completed tool usage.")
            break

    # Process final response if available
    final_response_content = message.content[0].text.strip()
    print(f"\nFinal response from model: {final_response_content}")

# Initial model message setup
user_message = {
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

# Handle responses and process tools until the model completes
handle_model_response(message, user_message)
