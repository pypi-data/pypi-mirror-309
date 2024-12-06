# ai_execution.py
import sys
import os

# Add the 'src' directory to the Python path for access to the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from fiscus import FiscusLLMType, FiscusResponseType

from .fiscus_config import client
from anthropic import Anthropic # type: ignore

# Initialize Anthropics client
anthropic_client = Anthropic(api_key="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")

# Step 4: Execute an AI task using the Anthropics client
def execute_ai_task():
    # response = client.ai_execute(
    #     input='Can you check my bank account balance and see if I have enough money to purchase bitcoin, if so how much can I buy?',
    #     llm=anthropic_client,
    #     llm_type=FiscusLLMType.ANTHROPIC,
    #     response_format=FiscusResponseType.TEXT,
    #     state_id='12345 Session',
    # )
    response = client.ai_execute(
		input='Can you provide a summary of my recent transactions over the past month?',
		llm=anthropic_client,
		llm_type=FiscusLLMType.ANTHROPIC,
		response_format=FiscusResponseType.TEXT,
		state_id='account_summary_123',
		storage_type='pickle',       # Use local file storage
		is_short_term=False
	)
    if response.success:
        print(response.data)
    else:
        print(response.error.message)
