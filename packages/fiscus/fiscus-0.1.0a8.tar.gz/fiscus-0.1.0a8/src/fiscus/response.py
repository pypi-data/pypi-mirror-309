# fiscus_sdk/response.py

import json
import logging
from typing import Any, Dict, List, Optional, Union, Callable
from enum import Enum

from .enums import FiscusCallbackType
from .callbacks import (
	FiscusOnSuccess,
	FiscusOnError,
	FiscusOnLog,
	FiscusOnResponse,
	FiscusOnStream,
	FiscusOnAuth
)

class FiscusErrorCode(Enum):
	"""
	Enumeration of standardized error codes for Fiscus SDK.
	"""
	AUTH_FAILURE = 1001
	INVALID_REQUEST = 1002
	NOT_FOUND = 1003
	INTERNAL_ERROR = 1004
	TIMEOUT = 1005
	USER_OPERATION_ERROR = 1006
	EXECUTION_FAILURE = 1007
	EXECUTION_HALTED = 1008
	PLANNING_FAILURE = 1009
	TESTING_FAILURE = 1010
	HALT_REQUESTED = 1011
	UNKNOWN_ERROR = 9999
	# Add more as needed


class FiscusError:
	"""
	Represents a structured error with a code, message, and optional details.
	"""

	def __init__(self, code: Union[FiscusErrorCode, int, None], message: str, details: Optional[Any] = None):
		"""
		Initialize a FiscusError.

		:param code: A FiscusErrorCode enumeration value, an integer, or None.
		:param message: Descriptive error message.
		:param details: Optional additional error details.
		"""
		# Attempt to interpret the error code correctly
		if isinstance(code, FiscusErrorCode):
			self.code = code
		elif isinstance(code, int) and code in FiscusErrorCode._value2member_map_:
			self.code = FiscusErrorCode(code)
		else:
			self.code = FiscusErrorCode.UNKNOWN_ERROR  # Default if code is missing or unrecognized

		self.message = message
		self.details = details

	def __repr__(self):
		return f"<FiscusError code={self.code.value} message='{self.message}'>"
	
	def __str__(self):
		return json.dumps(self.to_dict())  # Provides a JSON-compatible string for logging

	def to_dict(self) -> Dict[str, Any]:
		"""
		Serialize the FiscusError to a dictionary.

		:return: Dictionary representation of the error.
		"""
		return {
			'code': self.code.value,
			'message': self.message,
			'details': self.details
		}
	
	def to_json(self) -> Dict[str, Any]:
		"""
		Serialize the FiscusResponse to a JSON-compatible dictionary.

		:return: Dictionary representation of the response.
		"""
		return {
			'success': self.success,
			'message_id': self.message_id,
			'error': self.error.to_dict() if isinstance(self.error, FiscusError) else self.error,
			'result': self._result
		}

class FiscusResponse:
	"""
	Represents a unified response from Fiscus SDK operations, abstracting REST and WebSocket responses.
	Handles both standard and user-specific responses.
	Provides intuitive accessors and robust error handling.
	"""

	def __init__(
		self,
		success: bool,
		result: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
		error: Optional[Union[FiscusError, str, dict]] = None,
		message_id: Optional[str] = None,

		# Default callbacks assigned here, can be overridden if needed
		callbacks: Optional[Dict[FiscusCallbackType, Callable]] = None
	):
		"""
		Initialize a FiscusResponse.

		:param success: Indicates if the operation was successful.
		:param result: The result data, can be a dict for single responses or a list of dicts for batch responses.
		:param error: Error information which can be a FiscusError, string, or dictionary.
		:param message_id: Identifier for the message or operation.
		:param callbacks: Optional dictionary of user-defined callbacks to override SDK-defined defaults.
		"""
		self.logger = logging.getLogger(f'.response.{self.__class__.__name__}')

		self.success = success
		self.message_id = message_id
		self._result = result
		self._is_batch = isinstance(result, list) and success
		self.authorization_url = None

		# Assign callbacks with optional user overrides, falling back to defaults if necessary
		self.on_success = callbacks.get(FiscusCallbackType.ON_SUCCESS, FiscusOnSuccess) if callbacks else FiscusOnSuccess
		self.on_error = callbacks.get(FiscusCallbackType.ON_ERROR, FiscusOnError) if callbacks else FiscusOnError
		self.on_response = callbacks.get(FiscusCallbackType.ON_RESPONSE, FiscusOnResponse) if callbacks else FiscusOnResponse
		self.on_stream = callbacks.get(FiscusCallbackType.ON_STREAM, FiscusOnStream) if callbacks else FiscusOnStream
		self.on_log = callbacks.get(FiscusCallbackType.ON_LOG, FiscusOnLog) if callbacks else FiscusOnLog
		self.on_auth = callbacks.get(FiscusCallbackType.ON_AUTH, FiscusOnAuth) if callbacks else FiscusOnAuth

		# Check for AUTH_FAILURE and trigger on_auth callback immediately if applicable
		if isinstance(error, dict) and error.get("code") == FiscusErrorCode.AUTH_FAILURE.value:
			auth_url = error.get("details", {}).get("authorizationUrl")
			if auth_url:
				# Log to confirm the callback setup and invocation
				self.logger.debug(f"Attempting to invoke on_auth with URL: {auth_url}")
				if callable(self.on_auth):
					self.on_auth({"authorization_url": auth_url, "message_id": self.message_id})
					self.logger.debug("on_auth callback successfully triggered.")
				else:
					self.logger.warning("on_auth callback is not callable.")
				return  # Skip further processing if on_auth is handled

		# Process and set up the error object if needed
		if isinstance(error, FiscusError):
			self.error = error
		elif isinstance(error, str):
			self.error = FiscusError(code=FiscusErrorCode.UNKNOWN_ERROR, message=error)
		elif isinstance(error, dict):
			# Extract and interpret the code from the dictionary, if present
			code_value = error.get('code', FiscusErrorCode.UNKNOWN_ERROR.value)
			# Convert code to FiscusErrorCode or default to UNKNOWN_ERROR
			code = FiscusErrorCode(code_value) if code_value in FiscusErrorCode._value2member_map_ else FiscusErrorCode.UNKNOWN_ERROR
			self.error = FiscusError(
				code=code,
				message=error.get('message', 'An error occurred.'),
				details=error.get('details')
			)
		else:
			self.error = None  # Handle unexpected types gracefully

		# Trigger appropriate callbacks
		if self.success and self.on_success:
			self.on_success({"result": self._result, "message_id": self.message_id})
		elif not self.success and self.on_error:
			self.on_error({"error": self.error.to_dict() if self.error else None, "message_id": self.message_id})

		# Always call the general response callback if defined
		if self.on_response:
			self.on_response({"success": self.success, "result": self._result, "error": self.error, "message_id": self.message_id})

		# Process nested response if result contains 'success', 'message', and 'data'
		self._nested_success: Optional[bool] = None
		self._nested_message: Optional[str] = None
		self._nested_data: Optional[Any] = None

		if self.success and isinstance(self._result, dict):
			# Check if the result contains nested 'success', 'message', and 'data'
			if all(k in self._result for k in ('success', 'message', 'data')):
				self._nested_success = self._result.get('success')
				self._nested_message = self._result.get('message')
				self._nested_data = self._result.get('data')

	@property
	def has_error(self) -> bool:
		"""Indicates if the response contains an error."""
		return not self.success

	@property
	def operation(self) -> Optional[str]:
		"""
		Retrieve the operation name from the response data.

		:return: Operation name string or None.
		"""
		if self.success and self._result:
			if self._is_batch and isinstance(self._result, list) and len(self._result) > 0:
				return self._result[0].get('operation')
			elif isinstance(self._result, dict):
				return self._result.get('operation')
		return None

	@property
	def result(self) -> Optional[Dict[str, Any]]:
		"""
		Retrieve a single response result.
		
		If the response contains a 'data' field, return its contents.
		
		:return: Dictionary of the single result or None.
		"""
		if self.success and not self._is_batch:
			# Check if the result contains a 'data' field, return it if exists
			if isinstance(self._result, dict) and 'data' in self._result:
				return self._result['data']
			return self._result  # Return the result directly if it's not batched
		return None

	@property
	def results(self) -> List[Dict[str, Any]]:
		"""
		Retrieve all response results for batch operations.
		
		If the response contains a 'data' field and it's a list, return its contents.
		
		:return: List of response dictionaries.
		"""
		if self.success and self._is_batch and isinstance(self._result, list):
			return self._result  # Return the list of results directly for batch operations
		
		# Handle cases where 'data' is a list inside a dictionary result
		if self.success and isinstance(self._result, dict) and 'data' in self._result:
			if isinstance(self._result['data'], list):
				return self._result['data']
		
		return []  # Return an empty list if no valid results are found
	
	@property
	def data(self) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
		"""
		Retrieve the entire response data.

		:return: The complete result data or None.
		"""
		return self._result if self.success else None

	@property
	def error_code(self) -> Optional[int]:
		"""
		Retrieve the error code if an error exists.

		:return: Error code integer or None.
		"""
		return self.error.code.value if self.error else None

	@property
	def error_message(self) -> Optional[str]:
		"""
		Retrieve the error message if an error exists.

		:return: Error message string or None.
		"""
		return self.error.message if self.error else None

	@property
	def error_details(self) -> Optional[Any]:
		"""
		Retrieve the error details if available.

		:return: Error details or None.
		"""
		return self.error.details if self.error else None

	@property
	def nested_success(self) -> Optional[bool]:
		"""Indicates if the nested operation was successful."""
		return self._nested_success

	@property
	def nested_message(self) -> Optional[str]:
		"""Retrieve the nested operation's message."""
		return self._nested_message

	@property
	def nested_data(self) -> Optional[Any]:
		"""Retrieve the nested operation's data."""
		return self._nested_data

	@property
	def is_nested(self) -> bool:
		"""Indicates if the response contains nested result data."""
		return self._nested_success is not None
	
	@staticmethod
	def map_error(error_message: str) -> 'FiscusError':
		"""
		Maps an error message to a FiscusError with appropriate ErrorCode.

		:param error_message: The error message string from the backend.
		:return: FiscusError instance with mapped ErrorCode.
		"""
		# Define your error mapping logic here
		error_mapping = {
			"connector already exists": FiscusErrorCode.INVALID_REQUEST,
			"API configuration not found": FiscusErrorCode.NOT_FOUND,
			"Invalid API key": FiscusErrorCode.AUTH_FAILURE,
			"Invalid parameters": FiscusErrorCode.INVALID_REQUEST,
			"Timeout occurred": FiscusErrorCode.TIMEOUT,
			"User operation error": FiscusErrorCode.USER_OPERATION_ERROR
			# Add more mappings as needed
		}

		for msg, code in error_mapping.items():
			if msg.lower() in error_message.lower():
				return FiscusError(code=code, message=error_message)

		# Default to UNKNOWN_ERROR if no match found
		return FiscusError(code=FiscusErrorCode.UNKNOWN_ERROR, message=error_message)

	def get_field(self, *keys: str, default: Any = None) -> Any:
		"""
		Safely retrieve nested fields from the result data.

		Usage:
			response.get_field('data', 'time', 'updated')

		:param keys: Sequence of keys to traverse the nested data.
		:param default: Default value to return if any key is missing.
		:return: The retrieved value or the default.
		"""
		if not self.success or not self._result:
			return default

		target = self._nested_data if self.is_nested else self._result

		for key in keys:
			if isinstance(target, dict) and key in target:
				target = target[key]
			else:
				return default
		return target

	def get_value(self, key: str, default: Any = None) -> Any:
		"""
		Retrieve a top-level key value from the result data.

		:param key: The key to retrieve.
		:param default: Default value if key is missing.
		:return: The value associated with the key or default.
		"""
		if not self.success or not self._result:
			return default

		target = self._nested_data if self.is_nested else self._result

		return target.get(key, default) if isinstance(target, dict) else default

	def get_nested_value(self, keys: List[str], default: Any = None) -> Any:
		"""
		Retrieve a nested value from the result data using a list of keys.

		:param keys: List of keys representing the path to the desired value.
		:param default: Default value if any key in the path is missing.
		:return: The nested value or default.
		"""
		return self.get_field(*keys, default=default)
	
	def trigger_stream_callback(self, data: Any):
		"""Utility to trigger the stream callback when streaming data is available."""
		if self.on_stream:
			self.on_stream(data)

	def to_json(self) -> Dict[str, Any]:
		"""
		Serialize the FiscusResponse to a JSON-compatible dictionary.

		:return: Dictionary representation of the response.
		"""
		return {
			'success': self.success,
			'message_id': self.message_id,
			'error': self.error.to_dict() if self.error else None,
			'result': self._result
		}

	def _get_nested_value(self, data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
		"""
		Helper method to retrieve nested value from a single data item.

		:param data: Dictionary to retrieve the value from.
		:param keys: List of keys representing the path.
		:param default: Default value if any key is missing.
		:return: The nested value or default.
		"""
		value = data
		for key in keys:
			if isinstance(value, dict) and key in value:
				value = value[key]
			else:
				return default
		return value

	def __repr__(self):
		if self.success:
			if self._is_batch:
				return f"<FiscusResponse success=True results={self._result}>"
			elif self.is_nested:
				return f"<FiscusResponse success=True nested_success={self.nested_success} message='{self.nested_message}' data={self.nested_data}>"
			elif self._result:
				return f"<FiscusResponse success=True result={self._result}>"
			else:
				return f"<FiscusResponse success=True>"
		else:
			return f"<FiscusResponse success=False error={self.error}>"

	def __str__(self):
		return json.dumps(self.to_json(), indent=4)

	def __getitem__(self, key: str) -> Any:
		"""
		Allows dict-like access to the response data.

		:param key: The key to access.
		:return: The value associated with the key.
		"""
		if key in self.to_json():
			return self.to_json()[key]
		raise KeyError(f"Key '{key}' not found in FiscusResponse.")

	def __iter__(self):
		"""
		Allows iteration over the response keys.

		:return: An iterator over the keys.
		"""
		return iter(self.to_json())

	def __contains__(self, key: str) -> bool:
		"""
		Allows the use of the 'in' keyword to check for keys in the response.

		:param key: The key to check.
		:return: True if the key exists, False otherwise.
		"""
		return key in self.to_json()
