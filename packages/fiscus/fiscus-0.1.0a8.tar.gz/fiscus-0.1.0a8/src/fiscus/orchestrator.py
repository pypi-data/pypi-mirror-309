# fiscus_sdk/orchestrator.py

import logging
import asyncio
import time
import uuid
from typing import Dict, Any, List, Optional, Callable, TYPE_CHECKING

from .enums import FiscusConnectionType, FiscusResponseType, FiscusActionType, FiscusRestType, FiscusCallbackType
from .user import FiscusUser
from .connection import _ConnectionManager
from .response import FiscusResponse, FiscusError, FiscusErrorCode
from .exceptions import FiscusValidationError
from .callbacks import (
	FiscusCallback,
	FiscusOnSuccess,
	FiscusOnError,
	FiscusOnAuth,
	FiscusOnStream,
	FiscusOnLog,
)
from .audit import FiscusAuditTrail
from .fiscus_file import FiscusFile
from .utility import validate_params

if TYPE_CHECKING:
	from .client import FiscusClient


class _Orchestrator:
	"""
	Manages and executes workflows, both manually defined and dynamically routed.
	This class is intended for internal use and is not exposed publicly.
	Provides comprehensive logging for internal debugging and auditing.
	"""

	def __init__(
		self,
		user: Optional[FiscusUser],
		connection_manager: _ConnectionManager,
		client: 'FiscusClient',
	):
		"""
		Initialize an Orchestrator with the provided user, connection manager, and client.

		:param user: Reference to the FiscusUser instance, can be None.
		:param connection_manager: Connection manager instance for handling network connections.
		:param client: Reference to the FiscusClient instance.
		"""
		self.user = user
		self.client = client
		self.connection_manager = connection_manager
		self.context: Dict[str, Any] = {}

		# Conditionally set the logger based on user_id availability
		if self.user and self.user.user_id:
			logger_name = f".orchestrator.{self.user.user_id}"
		else:
			logger_name = ".orchestrator.unknown"
		self.logger = logging.getLogger(logger_name)

		# Initialize audit trail for logging actions
		self.audit_trail = FiscusAuditTrail(
			logger_name,
			enable_logging=self.client.enable_audit_logging if self.user else False,
		)

		# Configure logger based on client's logging settings
		self._configure_logging()

		self.logger.info("Orchestrator initialized successfully.")

		self.custom_prompt_template: Optional[str] = None
		self.preprocess_function: Optional[Callable[[str], str]] = None
		self.postprocess_function: Optional[Callable[[FiscusResponse], Any]] = None
		self.error_callback: Optional[FiscusCallback] = None
		self.success_callback: Optional[FiscusCallback] = None

		# Use settings from the client
		self.connection_type = self.client.connection_type
		self.response_format = self.client.response_format
		self.retries = self.client.retries
		self.backoff_factor = self.client.backoff_factor

	def _configure_logging(self) -> None:
		"""
		Configure the logging for the Orchestrator.

		Sets up the logger with appropriate handlers and formatters based on the client's configuration.
		Ensures that logs are consistent with other SDK components.
		"""
		# Inherit logging level and handlers from the client's logger
		self.logger.setLevel(self.client.logger.level)

		# Prevent adding multiple handlers if they already exist
		if not self.logger.hasHandlers():
			for handler in self.client.logger.handlers:
				self.logger.addHandler(handler)

		self.logger.debug("Logging configured for Orchestrator.")

	def _execute_tasks(
		self,
		tasks: List[Dict[str, Any]],
		callbacks: Optional[Dict[str, FiscusCallback]] = None,
		custom_options: Optional[Dict[str, Any]] = None,
		connection_type: Optional[FiscusConnectionType] = None,
		response_format: Optional[FiscusResponseType] = None,
		user: Optional[FiscusUser] = None,
	) -> FiscusResponse:
		"""
		Execute a list of tasks synchronously.

		:param tasks: List of task dictionaries to execute.
		:param callbacks: Optional callbacks to handle responses.
		:param custom_options: Optional custom options for execution.
		:param connection_type: Optional type of connection to use.
		:param response_format: Optional format of the response.
		:param user: Optional FiscusUser instance to perform the tasks.
		:return: FiscusResponse object containing the result.
		"""
		self.logger.debug("Starting synchronous execution of tasks.")

		# Set default connection type and response format if not provided
		if connection_type is None:
			connection_type = self.connection_type
		if response_format is None:
			response_format = self.response_format

		# Ensure each task has a 'params' key
		for task in tasks:
			if 'params' not in task or task['params'] is None:
				task['params'] = {}
				self.logger.debug(f"Task {task.get('operation', 'unknown')} missing 'params'; defaulting to empty dict.")

		# Validate user presence
		if not user and not self.user:
			self.logger.error("No FiscusUser instance provided for task execution.")
			raise ValueError("A FiscusUser instance must be provided.")
		current_user = user or self.user

		self.logger.debug(f"Executing tasks for user '{current_user.user_id}'.")

		# Prepare data to send to backend
		data = {
			'tasks': tasks,
			# 'callbacks': callbacks,  # Callbacks are handled internally
		}
		self.logger.debug(f"Prepared data for server: {self._mask_sensitive_info(data)}")

		# Send operation to server and capture response
		response = self._send_operation_to_server(
			action=FiscusActionType.ACTION,
			data=data,
			response_format=response_format,
			connection_type=connection_type,
			custom_options=custom_options,
			user=current_user,
			expected_responses=len(tasks),
		)

		self.logger.info(f"Synchronous task execution completed for user '{current_user.user_id}'.")
		self.audit_trail.record('execute_tasks', {'number_of_tasks': len(tasks)})

		return response

	async def _execute_tasks_async(
		self,
		tasks: List[Dict[str, Any]],
		callbacks: Optional[Dict[str, FiscusCallback]] = None,
		custom_options: Optional[Dict[str, Any]] = None,
		connection_type: Optional[FiscusConnectionType] = None,
		response_format: Optional[FiscusResponseType] = None,
		user: Optional[FiscusUser] = None,
	) -> FiscusResponse:
		"""
		Execute a list of tasks asynchronously.

		:param tasks: List of task dictionaries to execute.
		:param callbacks: Optional callbacks to handle responses.
		:param custom_options: Optional custom options for execution.
		:param connection_type: Optional type of connection to use.
		:param response_format: Optional format of the response.
		:param user: Optional FiscusUser instance to perform the tasks.
		:return: FiscusResponse object containing the result.
		"""
		self.logger.debug("Starting asynchronous execution of tasks.")

		# Set default connection type and response format if not provided
		if connection_type is None:
			connection_type = self.connection_type
		if response_format is None:
			response_format = self.response_format

		# Ensure each task has a 'params' key
		for task in tasks:
			if 'params' not in task or task['params'] is None:
				task['params'] = {}
				self.logger.debug(f"Task {task.get('operation', 'unknown')} missing 'params'; defaulting to empty dict.")

		# Validate user presence
		if not user and not self.user:
			self.logger.error("No FiscusUser instance provided for asynchronous task execution.")
			raise ValueError("A FiscusUser instance must be provided.")
		current_user = user or self.user

		self.logger.debug(f"Asynchronously executing tasks for user '{current_user.user_id}'.")

		# Prepare data to send to backend
		data = {
			'tasks': tasks,
			'callbacks': callbacks,
		}
		self.logger.debug(f"Prepared data for asynchronous server call: {self._mask_sensitive_info(data)}")

		# Send operation to server asynchronously and capture response
		response = await self._send_operation_to_server_async(
			action=FiscusActionType.ACTION,
			data=data,
			response_format=response_format,
			connection_type=connection_type,
			custom_options=custom_options,
			user=current_user,
			expected_responses=len(tasks),
		)

		self.logger.info(f"Asynchronous task execution completed for user '{current_user.user_id}'.")
		self.audit_trail.record('execute_tasks_async', {'number_of_tasks': len(tasks)})

		return response

	def _execute_operation(
		self,
		connector_name: str,
		operation: str,
		params: Dict[str, Any],
		callbacks: Optional[Dict[str, FiscusCallback]] = None,
		custom_options: Optional[Dict[str, Any]] = None,
		connection_type: Optional[FiscusConnectionType] = None,
		response_format: Optional[FiscusResponseType] = None,
		user: Optional[FiscusUser] = None,
		files: Optional[List[FiscusFile]] = None,
	) -> FiscusResponse:
		"""
		Execute a single operation synchronously with retry logic.

		:param connector_name: Name of the connector to use.
		:param operation: Operation name to execute.
		:param params: Parameters for the operation.
		:param callbacks: Optional callbacks to handle responses.
		:param custom_options: Optional custom options for execution.
		:param connection_type: Optional type of connection to use.
		:param response_format: Optional format of the response.
		:param user: Optional FiscusUser instance to perform the operation.
		:return: FiscusResponse object containing the result.
		"""
		self.logger.debug(f"Starting synchronous execution of operation '{operation}' on connector '{connector_name}'.")

		# Set default connection type and response format if not provided
		connection_type = connection_type or self.connection_type
		response_format = response_format or self.response_format
		params = params or {}

		# Validate user presence
		if not user and not self.user:
			self.logger.error("No FiscusUser instance provided for operation execution.")
			raise ValueError("A FiscusUser instance must be provided.")
		current_user = user or self.user

		# Establish WebSocket connection if required
		if connection_type == FiscusConnectionType.WEBSOCKET:
			if not self.connection_manager.websocket_sync_connected:
				self.logger.debug("Synchronous WebSocket not connected. Initiating connection.")
				if not current_user or not current_user.user_id:
					self.logger.error("User ID missing for WebSocket connection.")
					raise ValueError("User ID must be provided to establish WebSocket connection.")
				self.connection_manager.start_websocket_connection_sync(current_user.user_id)
				self.logger.info("Synchronous WebSocket connection established.")
			else:
				self.logger.debug("Synchronous WebSocket already connected.")

		self.logger.debug(
			f"Executing operation '{operation}' with params: {self._mask_sensitive_info(params)} using {connection_type.value} connection."
		)
		self.audit_trail.record(
			'execute_operation',
			{
				'connector_name': connector_name,
				'operation': operation,
				'params': self._mask_sensitive_info(params),
				'connection_type': connection_type.value,
			},
		)

		# Validate parameters
		if not validate_params(params) and params:
			self.logger.error(f"Validation failed for operation '{operation}' on connector '{connector_name}'.")
			self.audit_trail.record(
				'validation_error', {'connector_name': connector_name, 'operation': operation}
			)
			raise FiscusValidationError(
				f"Invalid parameters for operation '{operation}' on connector '{connector_name}'."
			)

		# Merge default and provided callbacks
		merged_callbacks = self._merge_callbacks(callbacks)

		# Retry logic for executing the operation
		for attempt in range(self.retries):
			try:
				data = {
					"connector": connector_name,
					"operation": operation,
					"params": params,
				}
				if files:
					data['files'] = [dict(file) for file in files]
				self.logger.debug(f"Attempt {attempt + 1} to execute operation '{operation}'.")

				# Fetch raw response data from the server and wrap in FiscusResponse immediately
				response = self._send_operation_to_server(
					action=FiscusActionType.ACTION,
					data=data,
					response_format=response_format,
					connection_type=connection_type,
					custom_options=custom_options,
					user=current_user,
				)

				# Check response success status and handle callbacks accordingly
				if response.success:
					if merged_callbacks['fiscus_on_success']:
						merged_callbacks['fiscus_on_success'](
							{'message': 'Operation succeeded', 'response': response}
						)
						self.logger.debug(f"Success callback executed for operation '{operation}'.")

					self.audit_trail.record(
						'operation_success',
						{
							'connector_name': connector_name,
							'operation': operation,
							'response': response.to_json(),
						},
					)
					self.logger.info(f"Operation '{operation}' executed successfully on connector '{connector_name}'.")
					return response
				else:
					# Handle specific error types and trigger appropriate callbacks
					error_code = response.error_code
					authorization_url = response.error_details.get("authorizationUrl") if response.error_details else None

					# Use FiscusCallbackType.ON_AUTH for consistency
					if error_code == FiscusErrorCode.AUTH_FAILURE.value and authorization_url:
						if FiscusCallbackType.ON_AUTH in merged_callbacks and callable(merged_callbacks[FiscusCallbackType.ON_AUTH]):
							# Log to confirm the callback setup and invocation
							self.logger.debug(f"Attempting to trigger ON_AUTH with URL: {authorization_url}")
							merged_callbacks[FiscusCallbackType.ON_AUTH]({
								'message': 'Authorization required',
								'authorization_url': authorization_url,
								'response': response
							})
							self.logger.debug(f"Auth callback executed for operation '{operation}' with authorization URL.")
						else:
							self.logger.warning("ON_AUTH callback is not set or is not callable.")
					else:
						if FiscusCallbackType.ON_ERROR in merged_callbacks and callable(merged_callbacks[FiscusCallbackType.ON_ERROR]):
							merged_callbacks[FiscusCallbackType.ON_ERROR](
								{'message': response.error_message or 'Unknown error', 'response': response}
							)
							self.logger.debug(f"Error callback executed for operation '{operation}'.")

					self.logger.error(f"Operation '{operation}' failed with error: {response.error_message or 'Unknown error'}")
					return response

			except Exception as e:
				self.logger.error(
					f"Error executing operation '{operation}' on connector '{connector_name}': {e}",
					exc_info=True
				)
				self.audit_trail.record(
					'operation_error',
					{
						'connector_name': connector_name,
						'operation': operation,
						'error': str(e),
						'attempt': attempt + 1,
					},
				)
				if attempt < self.retries - 1:
					sleep_time = self.backoff_factor * (2 ** attempt)
					self.logger.debug(f"Retrying operation '{operation}' after {sleep_time} seconds.")
					time.sleep(sleep_time)
				else:
					if merged_callbacks['fiscus_on_error']:
						fiscus_error = FiscusResponse.map_error(str(e))
						error_response = FiscusResponse(success=False, error=fiscus_error)
						merged_callbacks['fiscus_on_error']({'message': str(e), 'response': error_response})
						self.logger.debug(f"Error callback executed for operation '{operation}'.")
					self.logger.critical(f"Operation '{operation}' failed after {self.retries} attempts.")
					raise

	async def _execute_operation_async(
		self,
		connector_name: str,
		operation: str,
		params: Dict[str, Any],
		callbacks: Optional[Dict[str, FiscusCallback]] = None,
		custom_options: Optional[Dict[str, Any]] = None,
		connection_type: Optional[FiscusConnectionType] = None,
		response_format: Optional[FiscusResponseType] = None,
		user: Optional[FiscusUser] = None,
		files: Optional[List[FiscusFile]] = None,
	) -> FiscusResponse:
		"""
		Execute a single operation asynchronously with retry logic.
		
		:param connector_name: Name of the connector to use.
		:param operation: Operation name to execute.
		:param params: Parameters for the operation.
		:param callbacks: Optional callbacks to handle responses.
		:param custom_options: Optional custom options for execution.
		:param connection_type: Optional type of connection to use.
		:param response_format: Optional format of the response.
		:param user: Optional FiscusUser instance to perform the operation.
		:return: FiscusResponse object containing the result.
		"""
		self.logger.debug(f"Starting asynchronous execution of operation '{operation}' on connector '{connector_name}'.")

		# Set default connection type and response format if not provided
		if connection_type is None:
			connection_type = self.connection_type
		if response_format is None:
			response_format = self.response_format
		if params is None:
			params = {}

		# Validate user presence
		if not user and not self.user:
			self.logger.error("No FiscusUser instance provided for asynchronous operation execution.")
			raise ValueError("A FiscusUser instance must be provided.")
		current_user = user or self.user

		# Establish WebSocket connection if required
		if connection_type == FiscusConnectionType.WEBSOCKET:
			if not self.connection_manager.websocket_connected:
				self.logger.debug("Asynchronous WebSocket not connected. Initiating connection.")
				if not current_user or not current_user.user_id:
					self.logger.error("User ID missing for WebSocket connection.")
					raise ValueError("User ID must be provided to establish WebSocket connection.")
				await self.connection_manager.start_websocket_connection(current_user.user_id)
				self.logger.info("Asynchronous WebSocket connection established.")
		else:
			self.logger.debug("Using REST connection for asynchronous operation.")

		self.logger.debug(
			f"Asynchronously executing operation '{operation}' with params: {self._mask_sensitive_info(params)} using {connection_type.value} connection."
		)
		self.audit_trail.record(
			'execute_operation_async',
			{
				'connector_name': connector_name,
				'operation': operation,
				'params': self._mask_sensitive_info(params),
				'connection_type': connection_type.value,
			},
		)

		# Validate parameters
		if not validate_params(params):
			self.logger.error(f"Validation failed for asynchronous operation '{operation}' on connector '{connector_name}'.")
			self.audit_trail.record(
				'validation_error_async', {'connector_name': connector_name, 'operation': operation}
			)
			raise FiscusValidationError(
				f"Invalid parameters for operation '{operation}' on connector '{connector_name}'."
			)

		# Merge default and provided callbacks
		merged_callbacks = self._merge_callbacks(callbacks)

		# Retry logic for executing the operation asynchronously
		for attempt in range(self.retries):
			try:
				data = {
					"connector": connector_name,
					"operation": operation,
					"params": params,
					# "callbacks": []  # Callbacks are handled separately
				}
				if files:
					data['files'] = [dict(file) for file in files]
				self.logger.debug(f"Attempt {attempt + 1} to asynchronously execute operation '{operation}'.")
				response = await self._send_operation_to_server_async(
					action=FiscusActionType.ACTION,
					data=data,
					response_format=response_format,
					connection_type=connection_type,
					custom_options=custom_options,
					user=current_user,
				)

				# Execute success callback if provided
				if merged_callbacks['fiscus_on_success']:
					merged_callbacks['fiscus_on_success'](
						{'message': 'Operation succeeded', 'response': response}
					)
					self.logger.debug(f"Success callback executed for asynchronous operation '{operation}'.")

				self.audit_trail.record(
					'operation_success_async',
					{
						'connector_name': connector_name,
						'operation': operation,
						'response': response.to_json(),
					},
				)
				self.logger.info(f"Asynchronous operation '{operation}' executed successfully on connector '{connector_name}'.")
				return response

			except Exception as e:
				self.logger.error(
					f"Error executing asynchronous operation '{operation}' on connector '{connector_name}': {e}",
					exc_info=True
				)
				self.audit_trail.record(
					'operation_error_async',
					{
						'connector_name': connector_name,
						'operation': operation,
						'error': str(e),
						'attempt': attempt + 1,
					},
				)
				if attempt < self.retries - 1:
					sleep_time = self.backoff_factor * (2 ** attempt)
					self.logger.debug(f"Retrying asynchronous operation '{operation}' after {sleep_time} seconds.")
					await asyncio.sleep(sleep_time)
				else:
					if merged_callbacks['fiscus_on_error']:
						merged_callbacks['fiscus_on_error']({'message': str(e)})
						self.logger.debug(f"Error callback executed for asynchronous operation '{operation}'.")
					self.logger.critical(f"Asynchronous operation '{operation}' failed after {self.retries} attempts.")
					raise

	def _send_operation_to_server(
		self,
		action: FiscusActionType,
		data: Dict[str, Any],
		response_format: FiscusResponseType,
		connection_type: FiscusConnectionType,
		custom_options: Optional[Dict[str, Any]],
		user: FiscusUser,
		expected_responses: Optional[int] = None,
	) -> FiscusResponse:
		"""
		Send an operation to the server synchronously.

		:param action: Action name.
		:param data: Data payload to send.
		:param response_format: Format of the response.
		:param connection_type: Type of connection to use.
		:param custom_options: Optional custom options.
		:param user: FiscusUser instance performing the operation.
		:param expected_responses: Number of expected responses.
		:return: FiscusResponse object containing the result.
		"""
		self.logger.debug(f"Sending action '{action}' to server with data: {self._mask_sensitive_info(data)}")
		response = self._make_server_call(
			action,
			data,
			connection_type,
			response_format,
			custom_options,
			user,
			expected_responses,
		)
		self.logger.debug(f"Received response from server for action '{action}': {response.to_json()}")
		return response

	async def _send_operation_to_server_async(
		self,
		action: FiscusActionType,
		data: Dict[str, Any],
		response_format: FiscusResponseType,
		connection_type: FiscusConnectionType,
		custom_options: Optional[Dict[str, Any]],
		user: FiscusUser,
		expected_responses: Optional[int] = None,
	) -> FiscusResponse:
		"""
		Send an operation to the server asynchronously.

		:param action: Action name.
		:param data: Data payload to send.
		:param response_format: Format of the response.
		:param connection_type: Type of connection to use.
		:param custom_options: Optional custom options.
		:param user: FiscusUser instance performing the operation.
		:param expected_responses: Number of expected responses.
		:return: FiscusResponse object containing the result.
		"""
		self.logger.debug(f"Asynchronously sending action '{action}' to server with data: {self._mask_sensitive_info(data)}")
		response = await self._make_server_call_async(
			action,
			data,
			connection_type,
			response_format,
			custom_options,
			user,
			expected_responses,
		)
		self.logger.debug(f"Received asynchronous response from server for action '{action}': {response.to_json()}")
		return response

	def _make_server_call(
		self,
		action: FiscusActionType,
		data: Dict[str, Any],
		connection_type: FiscusConnectionType,
		response_format: FiscusResponseType,
		custom_options: Optional[Dict[str, Any]],
		user: FiscusUser,
		expected_responses: Optional[int] = None,
	) -> FiscusResponse:
		"""
		Make a synchronous server call based on the connection type.
		"""
		message_id = str(uuid.uuid4())
		data['messageId'] = message_id
		self.logger.debug(f"Generated message ID '{message_id}' for action '{action}'.")

		try:
			if connection_type == FiscusConnectionType.REST:
				url = self.connection_manager._get_rest_endpoint(action)
				headers = {'Authorization': f'Bearer {self.client.api_key}'}
				self.logger.debug(f"Sending REST request to URL '{url}' with payload: {self._mask_sensitive_info(data)}")

				# REST call execution
				response_data = asyncio.run(
					self.connection_manager.send_rest_request(
						method=FiscusRestType.POST,
						action=action,
						headers=headers,
						data=data,
						user_id=user.user_id,
					)
				)
				self.logger.debug(f"Received REST response: {response_data}")
				return self._create_fiscus_response(response_data, message_id)

			elif connection_type == FiscusConnectionType.WEBSOCKET:
				if not self.connection_manager.websocket_sync_connected:
					self.logger.debug("Synchronous WebSocket not connected. Initiating connection.")
					if not user or not user.user_id:
						self.logger.error("User ID missing for WebSocket connection.")
						raise ValueError("User ID must be provided to establish WebSocket connection.")
					self.connection_manager.start_websocket_connection_sync(user.user_id)
					self.logger.info("Synchronous WebSocket connection established.")

				self.logger.debug(f"Sending WebSocket message: {self._mask_sensitive_info(data)}")
				message = {'action': action, 'data': data}

				# WebSocket call execution
				response_data = self.connection_manager.send_websocket_message_sync(
					message, message_id, expected_responses=expected_responses
				)
				self.logger.debug(f"Received WebSocket response: {response_data}")
				return self._create_fiscus_response(response_data, message_id)

			else:
				self.logger.error(f"Unknown connection_type '{connection_type}' for server call.")
				raise ValueError(f"Unknown connection_type: {connection_type}")

		except Exception as e:
			self.logger.critical(f"Server call failed for action '{action}': {e}", exc_info=True)
			self.audit_trail.record('make_server_call_failure', {'action': action, 'error': str(e)})
			fiscus_error = FiscusError(code=FiscusErrorCode.INTERNAL_ERROR, message=str(e))
			return FiscusResponse(success=False, error=fiscus_error, message_id=message_id)

	def _create_fiscus_response(self, response_data, message_id):
		"""
		Centralized function to convert response data into FiscusResponse,
		handling error extraction without triggering callbacks.
		"""
		if response_data.success:
			return FiscusResponse(success=True, result=response_data.result, message_id=message_id)

		# Extract error details directly from the response_data, regardless of connection type
		error_message = response_data.error.message if response_data.error else "Unknown error occurred"
		error_code = response_data.error.code if response_data.error else FiscusErrorCode.UNKNOWN_ERROR.value
		authorization_url = (
			response_data.error.details.get('authorizationUrl')
			if response_data.error and response_data.error.details else None
		)

		# Construct a FiscusError based on available details
		fiscus_error = FiscusError(
			code=FiscusErrorCode.AUTH_FAILURE if authorization_url else FiscusErrorCode.UNKNOWN_ERROR,
			message=error_message,
			details={'authorizationUrl': authorization_url} if authorization_url else None
		)

		return FiscusResponse(success=False, error=fiscus_error, message_id=message_id)


	async def _make_server_call_async(
		self,
		action: FiscusActionType,
		data: Dict[str, Any],
		connection_type: FiscusConnectionType,
		response_format: FiscusResponseType,
		custom_options: Optional[Dict[str, Any]],
		user: FiscusUser,
		expected_responses: Optional[int] = None,
	) -> FiscusResponse:
		"""
		Make an asynchronous server call based on the connection type.

		:param action: Action name.
		:param data: Data payload to send.
		:param connection_type: Type of connection to use.
		:param response_format: Format of the response.
		:param custom_options: Optional custom options.
		:param user: FiscusUser instance performing the operation.
		:param expected_responses: Number of expected responses.
		:return: FiscusResponse object containing the result.
		"""
		message_id = str(uuid.uuid4())  # Generate a unique message ID
		data['messageId'] = message_id  # Include message ID in the data
		self.logger.debug(f"Generated message ID '{message_id}' for asynchronous action '{action}'.")

		try:
			if connection_type == FiscusConnectionType.REST:
				url = self.connection_manager._get_rest_endpoint(action)
				headers = {'Authorization': f'Bearer {self.client.api_key}'}
				payload = {
					'action': action,
					'data': data,
					'user_id': user.user_id,
				}
				self.logger.debug(f"Sending asynchronous REST request to URL '{url}' with payload: {self._mask_sensitive_info(payload)}")
				response_data = await self.connection_manager.send_rest_request(
					'POST', url, headers, payload, user_id=user.user_id, action=FiscusActionType.ACTION
				)
				self.logger.debug(f"Received asynchronous REST response: {response_data}")

				if response_data.success:
					return FiscusResponse(success=True, result=response_data.data, message_id=message_id)
				else:
					error_message = response_data.error_message or 'Unknown error occurred'
					fiscus_error = FiscusResponse.map_error(error_message)
					return FiscusResponse(success=False, error=fiscus_error, message_id=message_id)

			elif connection_type == FiscusConnectionType.WEBSOCKET:
				if not self.connection_manager.websocket_connected:
					self.logger.debug("Asynchronous WebSocket not connected. Initiating connection.")
					if not user or not user.user_id:
						self.logger.error("User ID missing for asynchronous WebSocket connection.")
						raise ValueError("User ID must be provided to establish WebSocket connection.")
					await self.connection_manager.start_websocket_connection(user.user_id)
					self.logger.info("Asynchronous WebSocket connection established.")

				self.logger.debug(f"Sending asynchronous WebSocket message: {self._mask_sensitive_info(data)}")
				message = {'action': action, 'data': data}
				response_data = await self.connection_manager.send_websocket_message(
					message, message_id, expected_responses=expected_responses
				)
				self.logger.debug(f"Received asynchronous WebSocket response: {response_data}")

				if response_data.success:
					return FiscusResponse(success=True, result=response_data.data, message_id=message_id)
				else:
					error_msg = response_data.error_message or 'Unknown asynchronous WebSocket error occurred'
					fiscus_error = FiscusResponse.map_error(error_msg)
					return FiscusResponse(success=False, error=fiscus_error, message_id=message_id)

			else:
				self.logger.error(f"Unknown connection_type '{connection_type}' for asynchronous server call.")
				raise ValueError(f"Unknown connection_type: {connection_type}")

		except Exception as e:
			self.logger.critical(f"Asynchronous server call failed for action '{action}': {e}", exc_info=True)
			self.audit_trail.record('make_server_call_async_failure', {'action': action, 'error': str(e)})
			fiscus_error = FiscusError(code=FiscusErrorCode.INTERNAL_ERROR, message=str(e))
			return FiscusResponse(success=False, error=fiscus_error, message_id=message_id)

	def _merge_callbacks(
		self, callbacks: Optional[Dict[str, FiscusCallback]]
	) -> Dict[str, FiscusCallback]:
		"""
		Merge provided callbacks with default callbacks.

		:param callbacks: Optional dictionary of callbacks to override defaults.
		:return: Dictionary containing merged callbacks.
		"""
		default_callbacks = {
			'fiscus_on_success': FiscusOnSuccess,
			'fiscus_on_error': FiscusOnError,
			'fiscus_on_auth': FiscusOnAuth,
			'fiscus_on_stream': FiscusOnStream,
			'fiscus_on_log': FiscusOnLog,
		}
		if callbacks:
			self.logger.debug(f"Merging provided callbacks with defaults: {callbacks.keys()}")
			default_callbacks.update(callbacks)
		else:
			self.logger.debug("No custom callbacks provided; using default callbacks.")
		return default_callbacks
	
	def send_user_data_via_websocket(
		self,
		user: FiscusUser,
		data: Dict[str, Any],
		callbacks: Optional[Dict[str, FiscusCallback]] = None,
	) -> FiscusResponse:
		"""
		Send user-related data via WebSocket connection.

		:param user: The FiscusUser instance.
		:param data: Data to send.
		:param callbacks: Optional callbacks for handling response.
		:return: FiscusResponse containing the result.
		"""
		self.logger.debug(f"Sending user data for user '{user.user_id}' via WebSocket.")
		message_id = str(uuid.uuid4())  # Generate unique message ID
		message_data = {
			'messageId': message_id,
			'action': FiscusActionType.USER,  # Specify that this is a user-related action
			'userId': user.user_id,
			'data': data
		}

		# Sending the message through the WebSocket
		response = self.connection_manager.send_websocket_message_sync(
			message=message_data,
			message_id=message_id,
			callback=callbacks.get('fiscus_on_success') if callbacks else None,
		)
		return response

	def send_user_data_via_rest(
		self,
		user_id: str,
		data: Dict[str, Any],
		callbacks: Optional[Dict[str, FiscusCallback]] = None,
	) -> FiscusResponse:
		"""
		Send user-related data via REST connection.

		:param user: The FiscusUser instance.
		:param data: Data to send.
		:param callbacks: Optional callbacks for handling response.
		:return: FiscusResponse containing the result.
		"""
		self.logger.debug(f"Sending user data for user '{user_id}' via REST.")
		message_id = str(uuid.uuid4())  # Generate unique message ID
		data['messageId'] = message_id

		# Sending the REST request by passing action instead of url
		return self.connection_manager.send_rest_request(
			method=FiscusRestType,
			action=FiscusActionType.USER,  # Pass the action, not the URL
			headers={'Authorization': f'Bearer {self.client.api_key}'},
			data=data,
			user_id=user_id
		)
	
	async def send_user_data_via_rest_async(
		self,
		user_id: str,
		data: Dict[str, Any],
		operation: str,
		callbacks: Optional[Dict[str, Callable]] = None,
	) -> FiscusResponse:
		"""
		Asynchronously send user-related data via REST connection.

		:param user: The FiscusUser instance.
		:param data: Data to send.
		:param callbacks: Optional callbacks for handling response.
		:return: FiscusResponse containing the result.
		"""
		self.logger.debug(f"Sending user data for user '{user_id}' via REST (async).")
		message_id = str(uuid.uuid4())  # Generate unique message ID
		data['messageId'] = message_id
		# Sending the REST request asynchronously
		return await self.connection_manager.send_rest_request(
			method=FiscusRestType.POST,
			action=FiscusActionType.USER,
			headers={'Authorization': f'Bearer {self.client.api_key}'},
			operation=operation,
			data=data,
			user_id=user_id
		)

	def _mask_sensitive_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Masks sensitive information in the provided data to prevent exposure in logs.

		:param data: Dictionary containing sensitive information.
		:return: Dictionary with sensitive information masked.
		"""
		masked_data = {}
		for key, value in data.items():
			if isinstance(value, dict):
				masked_data[key] = self._mask_sensitive_info(value)
			elif key.lower() in {'password', 'secret', 'api_key', 'token'}:
				masked_data[key] = self._mask_value(str(value))
			else:
				masked_data[key] = value
		self.logger.debug(f"Masked sensitive information: {masked_data}")
		return masked_data

	def _mask_value(self, value: str) -> str:
		"""
		Masks a given string value, showing only the first and last four characters.

		:param value: The string value to mask.
		:return: Masked string.
		"""
		if len(value) <= 8:
			return '*' * len(value)
		return f"{value[:4]}****{value[-4:]}"