# response_generation.py

from typing import Any
from .enums import FiscusResponseType

class _AIOrchestratorResponseGenerationMixin:
    def generate_final_response(self, input_text: str, api_responses: Any, response_format: FiscusResponseType) -> str:
        """
        Use _LLMAdapter to generate the final response to the user, incorporating the results from API calls.
        """
        self.logger.debug("Generating final response using LLM.")

        few_shot_examples = self.few_shot_examples.get('final_response', [])

        # Prepare prompt
        api_response_content = api_responses if response_format == FiscusResponseType.JSON else str(api_responses)
        prompt = (
            f"User Input: {input_text}\n"
            f"API Responses: {api_response_content}\n"
            "Based on the user's request and the API responses, generate a final response to the user."
        )

        # Execute using _LLMAdapter
        result = self.llm_adapter.execute(
            action='generate_final_response',
            prompt=prompt,
            context=None,
            function_schema=None,
            few_shot_examples=few_shot_examples,
            temperature=0.7,
            max_tokens=512,
            response_format=FiscusResponseType.TEXT,
            final_response=True,
            **self.custom_options
        )

        if result is None:
            self.logger.warning("Failed to generate final response using LLM.")
            if self.error_callback:
                self.error_callback(Exception("Failed to generate final response using LLM."))
            return ""

        return result

    async def generate_final_response_async(self, input_text: str, api_responses: Any, response_format: FiscusResponseType) -> str:
        """
        Asynchronously use _LLMAdapter to generate the final response to the user.
        """
        # Since _LLMAdapter doesn't have async methods in this design, we'll use the synchronous method
        return self.generate_final_response(input_text, api_responses, response_format)
