# run_methods.py

import asyncio
from typing import Optional, Dict, Any
from .enums import FiscusConnectionType, FiscusResponseType, FiscusExecutionType
from .response import FiscusResponse, FiscusError, FiscusErrorCode
from .utility import _mask_sensitive_info
from .callbacks import FiscusCallback
from .enums import FiscusPlanningType

class _AIOrchestratorRunMethodsMixin:
	def run(
		self,
		input_text: str,
		callbacks: Optional[Dict[str, FiscusCallback]] = None,
		connection_type: Optional[FiscusConnectionType] = None,
		response_format: Optional[FiscusResponseType] = FiscusResponseType.JSON,
		execution_mode: FiscusExecutionType = FiscusExecutionType.SEQUENTIAL,
	) -> FiscusResponse:
		"""
		The main method to process input and execute tasks synchronously.
		"""
		self.logger.debug(f"Running AIOrchestrator with input: {input_text}")
		self.logger.debug(f"connection_type={connection_type}, response_format={response_format}")

		tasks = self.process_input(input_text)
		self.logger.debug(f"Processed tasks: {_mask_sensitive_info(tasks)}")

		if not tasks:
			self.logger.warning("No tasks could be planned based on the input.")
			return FiscusResponse(success=False, error=FiscusError(
				code=FiscusErrorCode.INVALID_REQUEST,
				message="No tasks could be planned based on the input."
			))

		# Execute tasks and receive response
		response = self.execute_tasks(
			tasks=tasks,
			callbacks=callbacks,
			connection_type=connection_type,
			response_format=response_format,
			execution_mode=execution_mode,
		)

		# Ensure we have a FiscusResponse instance
		if not isinstance(response, FiscusResponse):
			self.logger.warning("Received response is not a FiscusResponse instance; wrapping it now.")
			response = FiscusResponse(success=True, result=response)

		# Handle failure case
		if not response.success:
			self.logger.error(f"Task execution failed with error: {response.error}")
			return response  # Return the error-laden FiscusResponse as-is

		# Post-process response if necessary
		if self.postprocess_function:
			self.logger.debug("Applying postprocess_function to response.")
			response = self.postprocess_function(response)

		# Extract only the data contents
		if isinstance(response.data, list):
			response_result = [
				res.data if res.success else {'error': res.error.to_dict() if res.error else 'Unknown error'}
				for res in response.data if isinstance(res, FiscusResponse)
			]
		else:
			response_result = response.data

		# Add logging to inspect response_result
		self.logger.debug(f"Extracted response_result: {_mask_sensitive_info(response_result)}")

		# Create final response based on connection type and format
		final_response = FiscusResponse(success=True, result=response_result, message_id=response.message_id)

		if connection_type == FiscusConnectionType.WEBSOCKET and response_format == FiscusResponseType.TEXT:
			self.logger.debug("Generating final response as TEXT for WebSocket connection.")
			final_response_text = self.generate_final_response(input_text, response_result, response_format)
			return FiscusResponse(success=True, result=final_response_text, message_id=response.message_id)

		elif connection_type == FiscusConnectionType.REST and response_format == FiscusResponseType.JSON:
			self.logger.debug("Returning JSON response for REST connection.")
			return final_response

		elif connection_type == FiscusConnectionType.WEBSOCKET and response_format == FiscusResponseType.JSON:
			self.logger.debug("Returning JSON response for WebSocket connection.")
			return final_response

		elif connection_type == FiscusConnectionType.REST and response_format == FiscusResponseType.TEXT:
			self.logger.debug("Generating final response as TEXT for REST connection.")
			final_response_text = self.generate_final_response(input_text, response_result, response_format)
			return FiscusResponse(success=True, result=final_response_text, message_id=response.message_id)

		# Default case: return JSON format
		self.logger.debug("Defaulting to JSON response format.")
		return final_response

	async def run_async(
		self,
		input_text: str,
		callbacks: Optional[Dict[str, FiscusCallback]] = None,
		connection_type: Optional[FiscusConnectionType] = None,
		response_format: Optional[FiscusResponseType] = FiscusResponseType.JSON,
		execution_mode: FiscusExecutionType = FiscusExecutionType.SEQUENTIAL,
	) -> FiscusResponse:
		"""
		The main method to process input and execute tasks asynchronously.
		"""
		self.logger.debug(f"Running AIOrchestrator asynchronously with input: {input_text}")
		self.logger.debug(f"connection_type={connection_type}, response_format={response_format}")

		tasks = self.process_input(input_text)
		self.logger.debug(f"Processed tasks: {_mask_sensitive_info(tasks)}")

		if not tasks:
			self.logger.warning("No tasks could be planned based on the input.")
			return FiscusResponse(success=False, error=FiscusError(
				code=FiscusErrorCode.INVALID_REQUEST,
				message="No tasks could be planned based on the input."
			))

		# Execute tasks and receive response
		response = await self.execute_tasks_async(
			tasks=tasks,
			callbacks=callbacks,
			connection_type=connection_type,
			response_format=response_format,
			execution_mode=execution_mode,
		)

		# Ensure we have a FiscusResponse instance
		if not isinstance(response, FiscusResponse):
			self.logger.warning("Received response is not a FiscusResponse instance; wrapping it now.")
			response = FiscusResponse(success=True, result=response)

		# Handle failure case
		if not response.success:
			self.logger.error(f"Task execution failed with error: {response.error}")
			return response  # Return the error-laden FiscusResponse as-is

		# Post-process response if necessary
		if self.postprocess_function:
			self.logger.debug("Applying postprocess_function to response.")
			response = self.postprocess_function(response)

		# Extract only the data contents
		if isinstance(response.data, list):
			response_result = [
				res.data if res.success else {'error': res.error.to_dict() if res.error else 'Unknown error'}
				for res in response.data if isinstance(res, FiscusResponse)
			]
		else:
			response_result = response.data

		# Add logging to inspect response_result
		self.logger.debug(f"Extracted response_result: {_mask_sensitive_info(response_result)}")

		# Create final response based on connection type and format
		final_response = FiscusResponse(success=True, result=response_result, message_id=response.message_id)

		if connection_type == FiscusConnectionType.WEBSOCKET and response_format == FiscusResponseType.TEXT:
			self.logger.debug("Generating final response as TEXT for WebSocket connection.")
			final_response_text = await self.generate_final_response_async(input_text, response_result, response_format)
			return FiscusResponse(success=True, result=final_response_text, message_id=response.message_id)

		elif connection_type == FiscusConnectionType.REST and response_format == FiscusResponseType.JSON:
			self.logger.debug("Returning JSON response for REST connection.")
			return final_response

		elif connection_type == FiscusConnectionType.WEBSOCKET and response_format == FiscusResponseType.JSON:
			self.logger.debug("Returning JSON response for WebSocket connection.")
			return final_response

		elif connection_type == FiscusConnectionType.REST and response_format == FiscusResponseType.TEXT:
			self.logger.debug("Generating final response as TEXT for REST connection.")
			final_response_text = await self.generate_final_response_async(input_text, response_result, response_format)
			return FiscusResponse(success=True, result=final_response_text, message_id=response.message_id)

		# Default case: return JSON format
		self.logger.debug("Defaulting to JSON response format.")
		return final_response


	def plan(self, input_text: str, control_level: FiscusPlanningType):
		# Implement planning logic here
		pass

	def run_test(self, input_text: str, connection_type: Optional[FiscusConnectionType], response_format: Optional[FiscusResponseType]):
		# Implement testing logic here
		pass