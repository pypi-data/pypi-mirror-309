# llm_adapter.py

import json
import re
import logging
from typing import Any, Dict, List, Optional, Callable
from .llm_config import _LLMConfig
from .enums import FiscusLLMType, FiscusResponseType

class _LLMAdapter:
	def __init__(
		self,
		llm: Any,
		llm_type: FiscusLLMType,
		logger: Optional[logging.Logger] = None,
		error_callback: Optional[Callable[[Exception], None]] = None,
	):
		"""
		Initialize the LLMAdapter with the given LLM object and type.

		:param llm: The instantiated LLM client object.
		:param llm_type: The type of the LLM (from FiscusLLMType enum).
		:param logger: Optional logger for logging.
		:param error_callback: Optional callback for handling errors.
		"""
		self.llm = llm
		self.llm_type = llm_type
		self.logger = logger or logging.getLogger(__name__)
		self.error_callback = error_callback
		self.config = _LLMConfig()  # Initialize configuration class

	def execute(
		self,
		action: str,
		prompt: str,
		context: Optional[str] = None,
		function_schema: Optional[Dict[str, Any]] = None,
		few_shot_examples: Optional[List[Dict[str, Any]]] = None,
		temperature: Optional[float] = None,
		max_tokens: Optional[int] = None,
		model: Optional[str] = None,
		response_format: Optional[FiscusResponseType] = FiscusResponseType.JSON,
		final_response: Optional[bool] = False,
		**kwargs,
	) -> Any:
		"""
		Execute an action using the specified LLM.

		:param action: The action to perform (e.g., 'classify_input', 'plan_tasks').
		:param prompt: The prompt to send to the LLM.
		:param context: Optional contextual information.
		:param function_schema: The function schema for structured outputs.
		:param few_shot_examples: Few-shot examples to include.
		:param temperature: Sampling temperature.
		:param max_tokens: Maximum tokens to generate.
		:param model: Model name to use.
		:param response_format: Expected response format (FiscusResponseType.JSON or FiscusResponseType.TEXT).
		:param kwargs: Additional LLM-specific parameters.
		:return: The LLM's response.
		"""
		try:
			# Retrieve action-specific configurations including prompt suffix and response key
			action_config = self.config.get_action_config(action, self.llm_type)
			prompt_suffix = action_config.get('prompt_suffix', '')
			prompt_with_suffix = f"{prompt}{prompt_suffix}"  # Append suffix if it exists

			# Log the prompt with suffix for debugging
			self.logger.debug(f"Executing action '{action}' with prompt suffix: {prompt_suffix}")
			self.logger.debug(f"Final prompt with suffix: {prompt_with_suffix}")

			response_key = action_config.get('response_key', 'result')

			# Execute with the appropriate LLM handler
			if self.llm_type == FiscusLLMType.OPENAI:
				return self._execute_openai(
					action=action,
					prompt=prompt_with_suffix,
					context=context,
					function_schema=function_schema,
					few_shot_examples=few_shot_examples,
					temperature=temperature,
					max_tokens=max_tokens,
					model=model,
					response_format=response_format,
					response_key=response_key,
					final_response=final_response,
					**kwargs
				)
			elif self.llm_type == FiscusLLMType.ANTHROPIC:
				return self._execute_anthropic(
					action=action,
					prompt=prompt_with_suffix,
					context=context,
					function_schema=function_schema,
					few_shot_examples=few_shot_examples,
					temperature=temperature,
					max_tokens=max_tokens,
					model=model,
					response_format=response_format,
					response_key=response_key,
					final_response=final_response,
					**kwargs
				)
			elif self.llm_type == FiscusLLMType.GEMINI:
				return self._execute_gemini(
					action=action,
					prompt=prompt,
					context=context,
					function_schema=function_schema,
					few_shot_examples=few_shot_examples,
					temperature=temperature,
					max_tokens=max_tokens,
					model=model,
					response_format=response_format,
					final_response=final_response,
					**kwargs,
				)
			elif self.llm_type == FiscusLLMType.LLAMA:
				return self._execute_llama(
					action=action,
					prompt=prompt,
					context=context,
					function_schema=function_schema,
					few_shot_examples=few_shot_examples,
					temperature=temperature,
					max_tokens=max_tokens,
					model=model,
					response_format=response_format,
					final_response=final_response,
					**kwargs,
				)
			elif self.llm_type == FiscusLLMType.COHERE:
				return self._execute_cohere(
					action=action,
					prompt=prompt,
					context=context,
					function_schema=function_schema,
					few_shot_examples=few_shot_examples,
					temperature=temperature,
					max_tokens=max_tokens,
					model=model,
					response_format=response_format,
					final_response=final_response,
					**kwargs,
				)
			else:
				raise ValueError(f"Unsupported LLM type: {self.llm_type}")
		except Exception as e:
			self.logger.error(f"Error during '{action}' execution: {e}")
			if self.error_callback:
				self.error_callback(e)
			return None

	# OpenAI Implementation
	def _execute_openai(
        self,
        action: str,
        prompt: str,
        context: Optional[str],
        function_schema: Optional[Dict[str, Any]],
        few_shot_examples: Optional[List[Dict[str, Any]]],
        temperature: Optional[float],
        max_tokens: Optional[int],
        model: Optional[str],
        response_format: Optional[FiscusResponseType],
        response_key: str,
		final_response: Optional[bool] = False,
        **kwargs
    ) -> Any:
    	# Prepare messages for the model
		self.logger.debug("Preparing messages for OpenAI request.")
		messages = self._prepare_messages(context, prompt, few_shot_examples)
		self.logger.debug(f"Messages prepared: {messages}")

		# Determine model and set default
		model = model or 'gpt-4o-2024-08-06'
		self.logger.info(f"Using model '{model}' for action '{action}'.")

		# Check if structured output is supported
		structured_output_supported_models = ['gpt-4o-2024-08-06', 'gpt-4o-mini-2024-07-18']
		use_structured_output = model in structured_output_supported_models and function_schema
		self.logger.debug(f"Structured output supported: {use_structured_output}")

		# Configure response format based on model and structured output support
		if use_structured_output:
			self.logger.info(f"Configuring structured output for model '{model}'.")
			parameters = function_schema.get("parameters", {})
			# Adjust schema construction based on parameters type
			if parameters.get('type') == 'object':
				# Ensure 'additionalProperties': False is present
				parameters.setdefault('additionalProperties', False)
				schema = parameters
			elif parameters.get('type') == 'array':
				items = parameters.get('items', {})
				if items.get('type') == 'object':
					# Ensure 'additionalProperties': False is present in items
					items.setdefault('additionalProperties', False)
				schema = {
					"type": "array",
					"items": items
				}
			else:
				schema = parameters  # Use parameters directly if it's neither object nor array

			response_format = {
				"type": "json_schema",
				"json_schema": {
					"name": function_schema.get("name", action),
					"description": function_schema.get("description", "Generated response"),
					"strict": True,
					"schema": schema
				}
			}
			self.logger.debug(f"Structured output response format: {response_format}")
		else:
			self.logger.info(f"Using JSON mode for model '{model}'.")
			response_format = {"type": "json_object"}
			self.logger.debug(f"JSON response format: {response_format}")

		# Log execution start
		self.logger.info(f"Executing OpenAI action '{action}' with model '{model}'.")

		try:
			if use_structured_output:
				# Structured Outputs - if 'parse' is supported
				if hasattr(self.llm.beta.chat.completions, 'parse'):
					self.logger.debug("Initiating structured output request via parse.")
					response = self.llm.beta.chat.completions.parse(
						model=model,
						messages=messages,
						response_format=response_format,
						temperature=temperature,
						max_tokens=max_tokens,
						**kwargs
					)
					self.logger.info(f"Response received from OpenAI for structured output: {response}")

					# Access parsed or refusal content
					message = response.choices[0].message
					if message.parsed:
						parsed_content = message.parsed
						self.logger.debug(f"Parsed content: {parsed_content}")
						# Handle both dict and list types
						if response_key and isinstance(parsed_content, dict):
							result = parsed_content.get(response_key) if parsed_content else None
						else:
							result = parsed_content  # For cases where parsed_content is a list or no response_key
						self.logger.info(f"Parsed content extracted with response key '{response_key}': {result}")
						return result
					elif message.refusal:
						self.logger.warning("OpenAI response refused due to content or safety filters.")
						return None
					else:
						# Handle parsing errors
						if hasattr(message, 'validation_errors') and message.validation_errors:
							self.logger.error(f"Validation errors during parsing: {message.validation_errors}")
						else:
							self.logger.warning("Parsing failed, no parsed content or refusal message.")
						# Attempt to parse the content manually as a fallback
						try:
							import json
							parsed_content = json.loads(message.content)
							self.logger.debug(f"Manually parsed content: {parsed_content}")
							if response_key and isinstance(parsed_content, dict):
								result = parsed_content.get(response_key) if parsed_content else None
							else:
								result = parsed_content  # For cases where parsed_content is a list or no response_key
							return result
						except json.JSONDecodeError as json_err:
							self.logger.error(f"Failed to parse message content as JSON: {json_err}")
							return None
				else:
					self.logger.error("Parse is not available for this model or client instance.")
					raise NotImplementedError("Parse is not available for this model or client instance.")
			else:
				# JSON Mode (Older models)
				self.logger.debug("Initiating request for JSON mode output.")
				response = self.llm.chat.completions.create(
					model=model,
					messages=messages,
					response_format=response_format,
					temperature=temperature,
					max_tokens=max_tokens,
					**kwargs
				)
				self.logger.info(f"Response received from OpenAI for JSON mode output: {response}")

				# Access content directly for older models
				content = response.choices[0].message.content
				self.logger.debug(f"Raw content received: {content}")
				parsed_result = self._parse_response_with_fallback(content, response_key, response_format, final_response)
				self.logger.info(f"Parsed result with fallback using response key '{response_key}': {parsed_result}")
				return parsed_result

		except Exception as e:
			self.logger.error(f"Error during OpenAI execution: {e}")
			if self.error_callback:
				self.logger.debug("Calling error callback due to execution error.")
				self.error_callback(e)
			return None

	# Anthropic Implementation
	def _execute_anthropic(
		self,
		action: str,
		prompt: str,
		context: Optional[str],
		function_schema: Optional[Dict[str, Any]],
		few_shot_examples: Optional[List[Dict[str, Any]]],
		temperature: Optional[float],
		max_tokens: Optional[int],
		model: Optional[str],
		response_format: Optional[FiscusResponseType],
		response_key: str,
		final_response: Optional[bool] = False,
		**kwargs
	) -> Any:
		messages = self._prepare_messages(context, prompt, few_shot_examples)
		model = model or 'claude-3-5-sonnet-20241022'
		self.logger.debug(f"Executing Anthropic action '{action}' with prompt: {prompt}")

		try:
			response = self.llm.messages.create(
				model=model,
				messages=messages,
				max_tokens=max_tokens,
				temperature=temperature,
				**kwargs
			)
			self.logger.debug(f"Received response from Anthropic: {response}")
			return self._parse_response_with_fallback(response.content[0].text if response.content else None, response_key, response_format, final_response)
		except Exception as e:
			self.logger.error(f"Error during Anthropic execution: {e}")
			if self.error_callback:
				self.error_callback(e)
			return None

	def _prepare_messages(
		self,
		context: Optional[str],
		prompt: str,
		few_shot_examples: Optional[List[Dict[str, Any]]]
	) -> List[Dict[str, str]]:
		"""
		Prepare the message payload for LLMs, including context and few-shot examples, with detailed logging.

		:param context: Optional context for the prompt.
		:param prompt: The main prompt.
		:param few_shot_examples: Few-shot examples to guide the model.
		:return: A list of messages formatted for the LLM.
		"""
		messages = []
		
		# Add system context if available
		if context:
			self.logger.debug(f"Adding context to messages: {context}")
			messages.append({"role": "system", "content": context})
		
		# Add few-shot examples if provided
		if few_shot_examples:
			self.logger.debug("Adding few-shot examples to messages.")
			for idx, example in enumerate(few_shot_examples):
				user_example = example.get("user")
				assistant_example = example.get("assistant")
				self.logger.debug(f"Example {idx + 1} - User: {user_example}, Assistant: {assistant_example}")
				messages.append({"role": "user", "content": user_example})
				messages.append({"role": "assistant", "content": assistant_example})
		
		# Add the main prompt
		self.logger.debug(f"Adding main prompt to messages: {prompt}")
		messages.append({"role": "user", "content": prompt})

		# Log final message structure for verification
		self.logger.debug(f"Final prepared messages: {messages}")
		
		return messages

	def _parse_response_with_fallback(self, response_content: Any, response_key: str, response_format: FiscusResponseType, final_response: bool) -> Any:
		"""
		Parse response content, handling cases where it's a list or non-JSON formatted string.
		Attempts direct JSON parsing first, then regex extraction, and falls back to array handling.
		"""

		# Directly return text content if response format is TEXT and for final response
		if response_format == FiscusResponseType.TEXT and final_response:
			self.logger.debug(f"Returning text response without parsing: {response_content}")
			return response_content

		# Step 1: If response is a list, take the first item assuming it's a TextBlock or similar
		if isinstance(response_content, list) and len(response_content) > 0:
			response_content = response_content[0] if isinstance(response_content[0], str) else response_content[0].text

		# Step 2: Attempt JSON parsing directly if it's a string
		try:
			parsed_json = json.loads(response_content) if isinstance(response_content, str) else response_content
			parsed_response = parsed_json.get(response_key, []) if isinstance(parsed_json, dict) else parsed_json
			self.logger.debug(f"Parsed JSON response: {parsed_response}")
			return parsed_response
		except (json.JSONDecodeError, KeyError, AttributeError) as e:
			self.logger.warning(f"Direct JSON parse failed, attempting regex extraction: {e}")

		# Step 3: Regex extraction if JSON parsing failed
		json_match = re.search(r'\{.*?\}|\[.*?\]', response_content, re.DOTALL)
		if json_match:
			try:
				parsed_json = json.loads(json_match.group(0))
				parsed_response = parsed_json.get(response_key, [])
				self.logger.debug(f"Parsed response after regex extraction: {parsed_response}")
				return parsed_response
			except json.JSONDecodeError as e:
				self.logger.error(f"Failed to parse JSON after regex extraction: {e}")

		# Fallback if all parsing attempts fail
		self.logger.error("No JSON object found in response after regex extraction.")
		if self.error_callback:
			self.error_callback(Exception("Failed to parse JSON from response"))
		return []

	# Gemini Implementation
	def _execute_gemini(
		self,
		action: str,
		prompt: str,
		context: Optional[str],
		function_schema: Optional[Dict[str, Any]],
		few_shot_examples: Optional[List[Dict[str, Any]]],
		temperature: Optional[float],
		max_tokens: Optional[int],
		model: Optional[str],
		response_format: Optional[FiscusResponseType],
		final_response: Optional[bool] = False,
		**kwargs,
	) -> Any:
		self.logger.debug(f"Executing action '{action}' using Gemini LLM.")
		# Prepare the prompt
		full_prompt = ""
		if context:
			full_prompt += f"{context}\n\n"
		if few_shot_examples:
			for example in few_shot_examples:
				full_prompt += f"{example['user']}\n{example['assistant']}\n\n"
		full_prompt += prompt

		# Define response schema for structured output
		response_schema = function_schema['parameters'] if function_schema else None

		# Set default parameters
		if temperature is None:
			temperature = 0.0 if action != 'generate_final_response' else 0.7
		if max_tokens is None:
			max_tokens = 256
		if model is None:
			model = 'gemini-1.5-pro'

		try:
			generation_config = {}
			if response_schema:
				generation_config['response_mime_type'] = 'application/json'
				generation_config['response_schema'] = response_schema

			response = self.llm.generate_content(
				prompt=full_prompt,
				model=model,
				temperature=temperature,
				max_output_tokens=max_tokens,
				generation_config=generation_config,
				**kwargs,
			)
			self.logger.debug(f"Gemini response: {response}")

			text = response.text.strip()
			if response_schema or response_format == FiscusResponseType.JSON:
				result = json.loads(text)
			else:
				result = text
			return result
		except Exception as e:
			self.logger.error(f"Error during Gemini execution: {e}")
			raise e

	# Llama Implementation
	def _execute_llama(
		self,
		action: str,
		prompt: str,
		context: Optional[str],
		function_schema: Optional[Dict[str, Any]],
		few_shot_examples: Optional[List[Dict[str, Any]]],
		temperature: Optional[float],
		max_tokens: Optional[int],
		model: Optional[str],
		response_format: Optional[FiscusResponseType],
		final_response: Optional[bool] = False,
		**kwargs,
	) -> Any:
		self.logger.debug(f"Executing action '{action}' using Llama LLM.")
		# Prepare messages
		messages = []
		if context:
			messages.append({"role": "system", "content": context})
		if few_shot_examples:
			for example in few_shot_examples:
				messages.append({"role": "user", "content": example['user']})
				messages.append({"role": "assistant", "content": example['assistant']})
		messages.append({"role": "user", "content": prompt})

		# Function calling
		functions = [function_schema] if function_schema else None
		function_call = {"name": function_schema['name']} if function_schema else None

		# Set default parameters
		if temperature is None:
			temperature = 0.0 if action != 'generate_final_response' else 0.7
		if max_tokens is None:
			max_tokens = 256
		if model is None:
			model = 'llama-2-70b-chat'

		try:
			api_request_json = {
				"model": model,
				"messages": messages,
				"temperature": temperature,
				"max_tokens": max_tokens,
				**kwargs,
			}
			if functions:
				api_request_json["functions"] = functions
				api_request_json["function_call"] = function_call

			response = self.llm.run(api_request_json)
			self.logger.debug(f"Llama response: {response}")

			if function_schema:
				# Extract function call arguments
				output = response['choices'][0]['message']['function_call']['arguments']
				result = json.loads(output)
			else:
				# Return the assistant's message content
				result = response['choices'][0]['message']['content']
				if response_format == FiscusResponseType.JSON:
					result = json.loads(result)
			return result
		except Exception as e:
			self.logger.error(f"Error during Llama execution: {e}")
			raise e

	# Cohere Implementation
	def _execute_cohere(
		self,
		action: str,
		prompt: str,
		context: Optional[str],
		function_schema: Optional[Dict[str, Any]],
		few_shot_examples: Optional[List[Dict[str, Any]]],
		temperature: Optional[float],
		max_tokens: Optional[int],
		model: Optional[str],
		response_format: Optional[FiscusResponseType],
		final_response: Optional[bool] = False,
		**kwargs,
	) -> Any:
		self.logger.debug(f"Executing action '{action}' using Cohere LLM.")
		# Prepare messages
		messages = []
		if context:
			messages.append({"role": "system", "content": context})
		if few_shot_examples:
			for example in few_shot_examples:
				messages.append({"role": "user", "content": example['user']})
				messages.append({"role": "assistant", "content": example['assistant']})
		messages.append({"role": "user", "content": prompt})

		# Define response format
		response_format_cohere = None
		if function_schema:
			response_format_cohere = {
				"type": "json_object",
				"json_schema": function_schema['parameters']
			}

		# Set default parameters
		if temperature is None:
			temperature = 0.0 if action != 'generate_final_response' else 0.7
		if max_tokens is None:
			max_tokens = 256
		if model is None:
			model = 'command-nightly'

		try:
			response = self.llm.chat(
				model=model,
				messages=messages,
				response_format=response_format_cohere,
				temperature=temperature,
				max_tokens=max_tokens,
				**kwargs,
			)
			self.logger.debug(f"Cohere response: {response}")

			text = response.reply.strip()
			if function_schema or response_format == FiscusResponseType.JSON:
				result = json.loads(text)
			else:
				result = text
			return result
		except Exception as e:
			self.logger.error(f"Error during Cohere execution: {e}")
			raise e
