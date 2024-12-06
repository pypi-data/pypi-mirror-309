# Fiscus SDK

The **Fiscus SDK** is your ultimate **AI Integration Engineer**. It seamlessly connects AI agents and language models to any API or service, simplifying and automating complex integrations. With Fiscus, you can dynamically orchestrate workflows, execute API operations, and build intelligent AI-powered applications without manual coding.

---

## Features

- **Dynamic API Operations**: Integrate with any API or service using connectors, enabling seamless task execution and workflow management.
- **AI Framework Integration**: Easily work with frameworks like LangChain, Crew, and OpenAI Function Calling.
- **Flexible Data Handling**: Retrieve responses in plain text or JSON format based on your configuration.
- **Comprehensive Callbacks**: Manage success, errors, authentication, streaming, logging, and debugging with ease.
- **Secure User Management**: Handle tokens, OAuth flows, and RBAC to support multiple users and services.
- **Effortless Connector Expansion**: Add new connectors without manual integration, empowering you to scale rapidly.
- **Advanced Orchestration**: Automatically route and manage workflows across unlimited connectors for scalable operations.
- **Robust Error Handling**: Handle issues dynamically with pre-built hooks and authentication retries.

---

## Installation

Install the Fiscus SDK via pip:

```
pip install fiscus-sdk
```

### System Requirements

- **Operating Systems**: Windows, macOS, Linux
- **Python Versions**: 3.9+

---

## Quick Start

### Example: Sending an Email

**Stateless Backend**

```python
from fiscus import FiscusClient

# Initialize the Fiscus client
client = FiscusClient(
	api_key='YOUR_FISCUS_API_KEY',
	user_id='user_123'
)

# Define email parameters
email_params = {
	"emailData": {
		"headers": [
			{"name": "To", "value": "example@test.com"},
			{"name": "From", "value": "support@fiscusflows.com"},
			{"name": "Subject", "value": "Test Email"}
		],
		"body": {
			"mimeType": "text/plain",
			"data": "Hello, this is a test email sent via API."
		}
	}
}

# Execute the email operation
response = client.execute(
	connector_name='gmail',
	operation='send_email',
	params=email_params
)

# Check response
if response.success:
    print('Email sent successfully!')
else:
    print(f'Error: {response.error_message}')
```

**Stateful Backend**

```python
from fiscus import FiscusClient, FiscusUser

# Initialize the Fiscus client
client = FiscusClient(api_key='YOUR_FISCUS_API_KEY')

# Create a user instance
user = FiscusUser(user_id='user_456', client=client)

# Execute the email operation
response = client.execute(
	connector_name='gmail',
	operation='send_email',
	params=email_params
)

# Check response
if response.success:
    print('Email sent successfully!')
else:
    print(f'Error: {response.error_message}')
```

---

## Core Concepts

- **FiscusClient**: The main entry point for the SDK. Create and manage users, and execute operations.
- **FiscusUser**: Represents a user, managing user-specific authentication, preferences, and RBAC.
- **FiscusConnector**: Manages integrations with external APIs or services.
- **Operation**: A specific function provided by a connector, like sending an email.
- **Callbacks**: Customizable hooks for logging, debugging, and handling responses.
- **Dynamic Preferences**: Customize behavior per user for seamless API operations.

---

## AI-Driven Workflows

### Using `ai_execute` for Adaptive Automation

The `ai_execute` function dynamically interprets natural language instructions to execute workflows using connectors and language models. It supports sequential and conditional execution, making it the backbone for intelligent task automation.

### Benefits

- **Natural Language to Workflow**: Converts user input into actionable tasks.
- **Multi-LLM Compatibility**: Supports OpenAI, Anthropic, and others.
- **Memory Management**: Stateful and stateless configurations.
- **Flexible Execution**: Use callbacks and custom decision logic for complex workflows.

### Example

```python
from fiscus import FiscusClient, FiscusUser, FiscusLLMType

# Initialize Fiscus client and user
client = FiscusClient(api_key='YOUR_FISCUS_API_KEY')
user = FiscusUser(user_id='user_123', client=client)

# Execute AI workflow
response = client.ai_execute(
    input="Schedule a meeting and email participants.",
    llm_type=FiscusLLMType.OPENAI,
    user=user
)

if response.success:
    print("Workflow executed:", response.result)
else:
    print(f"Error: {response.error_message}")
```

---

## Troubleshooting

### Common Installation Issues

- **Permission Errors**: Use `sudo` or a virtual environment.
- **Proxy Issues**: Configure pip to use proxy settings.

For additional help, contact [support@fiscusflows.com](mailto:support@fiscusflows.com).

---

## License

The Fiscus SDK is proprietary software developed by Fiscus Flows, Inc. By using this SDK, you agree to the terms and conditions outlined in the LICENSE file included with the distribution. For any licensing questions, contact [support@fiscusflows.com](mailto:support@fiscusflows.com).
