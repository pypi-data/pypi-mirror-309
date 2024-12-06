# fiscus_sdk/connection.py

import aiohttp  # type: ignore
import asyncio
import threading
import logging
import time
import uuid
from typing import Any, Dict, Optional, Callable
import json
from queue import Queue, Empty
import websocket  # type: ignore
import websockets  # type: ignore
from .fiscus_token import generate_token
from .response import FiscusResponse, FiscusError, FiscusErrorCode
from .callbacks import (
	FiscusCallback,
	FiscusOnResponse,
	FiscusOnSuccess,
	FiscusOnError,
	FiscusOnAuth,
	FiscusOnStream,
	FiscusOnLog,
)
from .enums import (
	FiscusActionType,
	FiscusLogLevel,
	FiscusActionTypeEncoder,
	FiscusRestType,
)

# ============================
# Connection Manager Class
# ============================

class _ConnectionManager:
	"""
	Manages REST and WebSocket connections for the Fiscus SDK.
	Provides both synchronous and asynchronous WebSocket operations.
	"""

	def __init__(self, api_key: str):
		"""
		Initializes the ConnectionManager with the provided API key.

		:param api_key: API key for authenticating connections.
		"""
		self.logger = logging.getLogger('.connection')
		self.logger.setLevel(FiscusLogLevel.DEBUG.to_logging_level())
		self.logger.trace("Initializing ConnectionManager with provided API key.")

		# Initialize REST and WebSocket endpoints
		# ##### DEV ######
		# self.rest_endpoint = 'https://86ktfzke6h.execute-api.us-east-1.amazonaws.com/'  # REST API endpoint for dev
		# self.websocket_endpoint = 'wss://b8ych02pwi.execute-api.us-east-1.amazonaws.com/dev/'  # WebSocket API endpoint dev

		##### PROD #####
		self.rest_endpoint = 'https://5qva06rx59.execute-api.us-east-1.amazonaws.com/'  # REST API endpoint for prod
		self.websocket_endpoint = 'wss://6qnsbv19b9.execute-api.us-east-1.amazonaws.com/prod/'  # WebSocket API endpoint prod
		self.logger.debug(f"REST endpoint set to: {self.rest_endpoint}")
		self.logger.debug(f"WebSocket endpoint set to: {self.websocket_endpoint}")

		# Synchronous WebSocket attributes
		self.websocket_sync = None
		self.websocket_sync_connected = False
		self.websocket_sync_thread = None
		self.websocket_sync_connected_event = threading.Event()
		self.response_queue = Queue()

		# Tracking pending responses for synchronous WebSocket
		self.pending_responses = {}  # Maps message_id to Queue
		self.callback_sync = {}      # Maps message_id to FiscusCallback

		# Asynchronous WebSocket attributes
		self.websocket = None
		self.websocket_connected = False
		self.pending_responses_async = {}  # Maps message_id to asyncio.Future
		self.callback_async = {}           # Maps message_id to FiscusCallback

		# General callback for all responses
		self.general_callback = FiscusOnResponse

		# Initialize an optional on_error attribute, setting it to FiscusOnError by default
		self.on_error = FiscusOnError

		# Initialize the dynamic REST endpoint map (relative paths)
		self.rest_endpoint_map = {
			FiscusActionType.ACTION: 'prod/execute',
			FiscusActionType.USER: 'prod/user/',
			# FiscusActionType.ACTION: 'dev/execute',
			# FiscusActionType.USER: 'dev/user/',
			# Add more mappings here as needed
		}

		self.api_key = api_key
		self.logger.info("ConnectionManager initialized successfully.")

	# ============================
	# Synchronous WebSocket Methods
	# ============================

	def start_websocket_connection_sync(self, user_id: str) -> None:
		"""
		Establishes a synchronous WebSocket connection using WebSocketApp.

		:param user_id: The user ID for authenticating the connection.
		"""
		self.logger.trace("Entering start_websocket_connection_sync method.")
		if self.websocket_sync_connected:
			self.logger.info("Synchronous WebSocket is already connected.")
			return

		self.logger.debug(f"Attempting to start synchronous WebSocket connection for user_id: {user_id}")

		# Generate authentication token
		token = generate_token(self.api_key)
		self.logger.debug("Authentication token generated for synchronous WebSocket.")

		# Prepare headers for the WebSocket connection
		headers = {
			'Authorization': f"Bearer {token}",
			'X-User-Id': user_id,
			'X-Api-Key': self.api_key,
		}
		self.logger.trace(f"WebSocket headers prepared: { {k: '***' if k == 'Authorization' else v for k, v in headers.items()} }")

		# Define callback functions for WebSocket events
		def on_open(ws):
			connection_time = time.time()
			self.logger.info("Synchronous WebSocket connection established.")
			self.websocket_sync_connected = True
			self.websocket_sync_connected_event.set()
			self.connection_start_time = connection_time
			self.logger.trace(f"Connection opened at {connection_time}.")

		def on_message(ws, message):
			receive_time = time.time()
			self.logger.debug(f"Received message at {receive_time}: {message}")
			try:
				message_data = json.loads(message)
				self.logger.trace("Parsed JSON message from WebSocket.")
				message_id = message_data.get('messageId')
				self.logger.trace(f"Extracted message_id: {message_id}")

				# Trigger general callback if it's defined
				if callable(self.general_callback):
					self.general_callback({'response': message_data})

				if message_id and message_id in self.pending_responses:
					self.logger.debug(f"Message ID {message_id} matches a pending response.")
					self.pending_responses[message_id].put(message_data)

					# Trigger the associated callback if exists
					if message_id in self.callback_sync:
						callback = self.callback_sync.pop(message_id)
						response = FiscusResponse(
							success=message_data.get('success', False),
							result=message_data.get('data'),
							error=FiscusResponse.map_error(message_data.get('error', 'Unknown error')) if not message_data.get('success', False) else None,
							message_id=message_id
						)
						self.logger.debug(f"Invoking synchronous callback for message_id: {message_id}.")
						if callable(callback):
							callback({'response': response})
						# Trigger FiscusOnSuccess or FiscusOnError based on response
						if response.success and callable(FiscusOnSuccess):
							FiscusOnSuccess({'response': response})
						elif not response.success and callable(FiscusOnError):
							FiscusOnError({'error': response.error, 'message_id': message_id})
				else:
					self.logger.info("Unsolicited message received; adding to response queue.")
					self.response_queue.put(message_data)

			except json.JSONDecodeError as e:
				self.logger.debug(f"JSON decoding error: {e}")
				if callable(self.on_error):
					self.on_error({'error': str(e)})

		def on_error(ws, error):
			self.logger.debug(f"Synchronous WebSocket error: {error}")
			self.logger.critical("Critical error encountered in synchronous WebSocket connection.")

			# Invoke on_error callback if defined
			if callable(self.on_error):
				self.on_error({"error": error})

		def on_close(ws, close_status_code, close_msg):
			close_time = time.time()
			self.logger.warning(f"Synchronous WebSocket closed at {close_time} with status {close_status_code}: {close_msg}")
			self.websocket_sync_connected = False
			self.websocket_sync_connected_event.clear()
			self.logger.info("Attempting to reconnect synchronous WebSocket in 5 seconds.")
			time.sleep(5)
			self.start_websocket_connection_sync(user_id)

		# Initialize WebSocketApp with the specified callbacks and headers
		self.websocket_sync = websocket.WebSocketApp(
			self.websocket_endpoint,
			header=[f"{k}: {v}" for k, v in headers.items()],
			on_open=on_open,
			on_message=on_message,
			on_error=on_error,
			on_close=on_close,
		)

		# Function to run the WebSocketApp in a separate thread
		def run():
			self.logger.trace("Launching synchronous WebSocket in a new thread.")
			self.websocket_sync.run_forever(ping_interval=60, ping_timeout=30)

		# Start the WebSocketApp thread
		self.websocket_sync_thread = threading.Thread(target=run, name="SyncWebSocketThread", daemon=True)
		self.websocket_sync_thread.start()

		# Wait for the connection to be established or timeout after 30 seconds
		self.logger.debug("Waiting for synchronous WebSocket connection to establish.")
		if not self.websocket_sync_connected_event.wait(timeout=30):
			self.logger.fatal("Synchronous WebSocket connection timed out after 30 seconds.")
			if callable(self.on_error):
				self.on_error({"error": "Synchronous WebSocket connection timeout"})
			raise Exception("Synchronous WebSocket connection timeout")
		else:
			connection_duration = time.time() - self.connection_start_time
			self.logger.info(f"Synchronous WebSocket connected in {connection_duration:.2f} seconds.")
			self.logger.trace(f"Connection established duration: {connection_duration:.2f} seconds.")

	def send_websocket_message_sync(
		self,
		message: Any,
		message_id: str,
		callback: Optional[FiscusCallback] = None,
		expected_responses: int = None
	) -> FiscusResponse:
		"""
		Sends a message over the synchronous WebSocket connection and awaits responses.

		:param message: The message payload to send.
		:param message_id: Unique identifier for correlating responses.
		:param callback: Optional callback to handle the response.
		:param expected_responses: Number of expected responses.
		:return: FiscusResponse object containing the result.
		"""
		self.logger.trace("Entering send_websocket_message_sync method.")
		if not self.websocket_sync_connected or not self.websocket_sync:
			self.logger.debug("Cannot send message: Synchronous WebSocket is not connected.")
			fiscus_error = FiscusError(code=FiscusErrorCode.INTERNAL_ERROR, message='WebSocket not connected')
			if callable(FiscusOnError):
				FiscusOnError({'error': fiscus_error, 'message_id': message_id})
			return FiscusResponse(success=False, error=fiscus_error)

		if 'userId' in message and message['action'] == 'user':
			self.logger.debug("Sending user-related data via WebSocket.")
		else:
			self.logger.debug("Sending action-related data via WebSocket.")

		self.logger.debug(f"Sending synchronous WebSocket message with message_id: {message_id}")
		try:
			# Use custom encoder to handle FiscusActionType serialization
			message_str = json.dumps(message, cls=FiscusActionTypeEncoder)
			response_queue = Queue()
			self.pending_responses[message_id] = response_queue

			# Register the callback if provided
			if callback:
				self.callback_sync[message_id] = callback
				self.logger.debug(f"Registered callback for message_id: {message_id}")

			send_time = time.time()
			self.logger.trace(f"Message prepared to send at {send_time}: {message_str}")
			self.websocket_sync.send(message_str)
			self.logger.debug(f"Message sent at {send_time}: [REDACTED]")  # Avoid logging sensitive message content

			# Collect responses with matching message_id
			responses = []
			start_time = time.time()
			timeout = 30  # Total timeout of 30 seconds
			self.logger.trace(f"Awaiting responses for message_id: {message_id} with timeout: {timeout} seconds.")
			while True:
				elapsed_time = time.time() - start_time
				remaining_time = timeout - elapsed_time
				if remaining_time <= 0:
					self.logger.debug("Synchronous WebSocket response timeout.")
					break
				try:
					response_data = response_queue.get(timeout=remaining_time)
					response_time = time.time()
					self.logger.debug(f"Received response at {response_time}: [REDACTED]")  # Avoid logging sensitive data
					responses.append(response_data)
					if expected_responses and len(responses) >= expected_responses:
						self.logger.debug(f"Received expected number of responses: {len(responses)}")
						break
					if expected_responses is None and len(responses) >= 1:
						self.logger.debug("Received single synchronous response as expected.")
						break
				except Empty:
					self.logger.info("No more responses received within the timeout period.")
					break

			# Clean up the pending responses
			del self.pending_responses[message_id]
			if message_id in self.callback_sync:
				del self.callback_sync[message_id]

			if responses:
				# Assuming single response for simplicity; adjust as needed
				first_response = responses[0]
				self.logger.debug(f"Response from the WebSocket is: {first_response}")

				if first_response.get('success'):
					fiscus_response = FiscusResponse(
						success=True,
						result=first_response.get('data'),
						message_id=message_id
					)
					self.logger.info(f"Received successful response for message_id: {message_id}.")
					self.logger.trace(f"Response data: {first_response.get('data')}")
					if callable(FiscusOnSuccess):
						FiscusOnSuccess({'response': fiscus_response})
					return fiscus_response
				else:
					# Extract authorization URL and error message directly from the response
					authorization_url = first_response.get('authorizationUrl')
					error_message = first_response.get('error', 'Unknown WebSocket error occurred')

					# Create a FiscusError with AUTH_FAILURE if authorization URL is present
					fiscus_error = FiscusError(
						code=FiscusErrorCode.AUTH_FAILURE if authorization_url else FiscusErrorCode.UNKNOWN_ERROR,
						message=error_message,
						details={'authorizationUrl': authorization_url} if authorization_url else None
					)

					# Log the error for clarity
					self.logger.debug(f"WebSocket operation failed with error: {error_message}")
					if callable(FiscusOnError):
						FiscusOnError({'error': fiscus_error, 'message_id': message_id})
					return FiscusResponse(
						success=False,
						error=fiscus_error,
						message_id=message_id
					)
			else:
				# Handle case where no responses were received
				self.logger.debug(f"No responses received for message_id: {message_id}.")
				fiscus_error = FiscusError(code=FiscusErrorCode.TIMEOUT, message='No responses received from WebSocket')
				if callable(FiscusOnError):
					FiscusOnError({'error': fiscus_error, 'message_id': message_id})
				return FiscusResponse(
					success=False,
					error=fiscus_error,
					message_id=message_id
				)
		except Exception as e:
			self.logger.debug(f"Exception while sending synchronous WebSocket message: {e}")
			self.logger.critical("Critical exception encountered in send_websocket_message_sync.")
			if message_id in self.pending_responses:
				del self.pending_responses[message_id]  # Clean up
			if message_id in self.callback_sync:
				self.callback_sync.pop(message_id)
			fiscus_error = FiscusError(code=FiscusErrorCode.INTERNAL_ERROR, message=str(e))
			if callable(FiscusOnError):
				FiscusOnError({'error': fiscus_error, 'message_id': message_id})
			return FiscusResponse(
				success=False,
				error=fiscus_error,
				message_id=message_id
			)

	def stop_websocket_connection_sync(self) -> None:
		"""
		Terminates the synchronous WebSocket connection gracefully.
		"""
		self.logger.trace("Entering stop_websocket_connection_sync method.")
		if self.websocket_sync_connected and self.websocket_sync:
			self.logger.info("Stopping synchronous WebSocket connection.")
			try:
				self.websocket_sync.close()
				self.logger.debug("WebSocket close signal sent.")
			except Exception as e:
				self.logger.debug(f"Error while closing WebSocket: {e}")
			self.websocket_sync_connected = False
			self.websocket_sync_connected_event.clear()
			if self.websocket_sync_thread and self.websocket_sync_thread.is_alive():
				self.logger.debug("Waiting for synchronous WebSocket thread to terminate.")
				self.websocket_sync_thread.join()
				self.logger.trace("Synchronous WebSocket thread has terminated.")
			self.logger.info("Synchronous WebSocket connection stopped successfully.")
		else:
			self.logger.warning("Synchronous WebSocket is not connected; nothing to stop.")

	def restart_websocket_connection_sync(self, user_id: str) -> None:
		"""
		Restarts the synchronous WebSocket connection by stopping and then starting it.

		:param user_id: The user ID for authenticating the connection.
		"""
		self.logger.trace("Entering restart_websocket_connection_sync method.")
		self.logger.info("Restarting synchronous WebSocket connection.")
		self.stop_websocket_connection_sync()
		self.start_websocket_connection_sync(user_id)

	# ============================
	# Asynchronous WebSocket Methods
	# ============================

	async def start_websocket_connection(self, user_id: str) -> None:
		"""
		Establishes an asynchronous WebSocket connection.

		:param user_id: The user ID for authenticating the connection.
		"""
		self.logger.trace("Entering start_websocket_connection method.")
		if self.websocket_connected:
			self.logger.info("Asynchronous WebSocket is already connected.")
			return

		self.logger.debug(f"Attempting to start asynchronous WebSocket connection for user_id: {user_id}")

		# Generate authentication token
		token = generate_token(self.api_key)
		self.logger.debug("Authentication token generated for asynchronous WebSocket.")

		# Prepare headers for the WebSocket connection
		headers = {
			'Authorization': f"Bearer {token}",
			'X-User-Id': user_id,
			'X-Api-Key': self.api_key,
		}
		self.logger.trace(f"WebSocket headers prepared: { {k: '***' if k == 'Authorization' else v for k, v in headers.items()} }")

		try:
			# Establish the asynchronous WebSocket connection with specified headers
			connection_start_time = time.time()
			self.logger.trace(f"Initiating asynchronous WebSocket connection at {connection_start_time}.")
			self.websocket = await websockets.connect(
				self.websocket_endpoint,
				extra_headers={k: v for k, v in headers.items()},
				ping_interval=60,
				ping_timeout=30,
			)
			self.websocket_connected = True
			connection_duration = time.time() - connection_start_time
			self.logger.info(f"Asynchronous WebSocket connection established in {connection_duration:.2f} seconds.")
			self.logger.trace(f"Connection established duration: {connection_duration:.2f} seconds.")

			# Start the message receiving loop
			asyncio.create_task(self._receive_messages())
		except Exception as e:
			self.logger.debug(f"Failed to establish asynchronous WebSocket connection: {e}")
			self.logger.critical("Critical failure in establishing asynchronous WebSocket connection.")
			if callable(FiscusOnError):
				FiscusOnError({'error': FiscusError(code=FiscusErrorCode.INTERNAL_ERROR, message=str(e)), 'message_id': str(uuid.uuid4())})
			self.websocket_connected = False

	async def _receive_messages(self):
		"""
		Continuously listens for incoming messages on the asynchronous WebSocket.
		"""
		self.logger.trace("Entering _receive_messages method.")
		self.logger.debug("Starting asynchronous WebSocket message receiver loop.")
		try:
			async for message in self.websocket:
				receive_time = time.time()
				self.logger.debug(f"Received asynchronous message at {receive_time}: [REDACTED]")  # Avoid logging sensitive data
				try:
					message_data = json.loads(message)
					message_id = message_data.get('messageId')
					self.logger.trace(f"Extracted message_id: {message_id} from asynchronous message.")

					# Trigger general callback for every response
					if callable(self.general_callback):
						self.general_callback({'response': message_data})

					if message_id and message_id in self.pending_responses_async:
						future = self.pending_responses_async.pop(message_id)
						if not future.done():
							future.set_result(message_data)

						# Trigger the associated callback if exists
						if message_id in self.callback_async:
							callback = self.callback_async.pop(message_id)
							response = FiscusResponse(
								success=message_data.get('success', False),
								result=message_data.get('data'),
								error=FiscusResponse.map_error(message_data.get('error', 'Unknown error')) if not message_data.get('success', False) else None,
								message_id=message_id
							)
							self.logger.debug(f"Invoking asynchronous callback for message_id: {message_id}.")
							if callable(callback):
								callback({'response': response})
							# Trigger FiscusOnSuccess or FiscusOnError based on response
							if response.success and callable(FiscusOnSuccess):
								FiscusOnSuccess({'response': response})
							elif not response.success and callable(FiscusOnError):
								FiscusOnError({'error': response.error, 'message_id': message_id})
					else:
						self.logger.info("Unsolicited asynchronous message received.")
						# Optionally, trigger a general callback for unsolicited messages
						if callable(self.general_callback):
							self.general_callback({'response': message_data})
				except json.JSONDecodeError as e:
					self.logger.debug(f"JSON decoding error in asynchronous message: {e}")
					if callable(self.on_error):
						self.on_error({'error': str(e)})
		except Exception as e:
			self.logger.debug(f"Error in asynchronous WebSocket receive loop: {e}")
			self.logger.critical("Critical error encountered in asynchronous WebSocket receive loop.")
			if callable(FiscusOnError):
				FiscusOnError({'error': FiscusError(code=FiscusErrorCode.INTERNAL_ERROR, message=str(e)), 'message_id': str(uuid.uuid4())})
			self.websocket_connected = False

	async def send_websocket_message(
		self,
		message: Any,
		message_id: str,
		callback: Optional[FiscusCallback] = None,
		expected_responses: int = None
	) -> FiscusResponse:
		"""
		Sends a message over the asynchronous WebSocket connection and awaits responses.

		:param message: The message payload to send.
		:param message_id: Unique identifier for correlating responses.
		:param callback: Optional callback to handle the response.
		:param expected_responses: Number of expected responses.
		:return: FiscusResponse object containing the result.
		"""
		self.logger.trace("Entering send_websocket_message method.")
		if not self.websocket_connected or not self.websocket:
			self.logger.debug("Cannot send message: Asynchronous WebSocket is not connected.")
			fiscus_error = FiscusError(code=FiscusErrorCode.INTERNAL_ERROR, message='Asynchronous WebSocket not connected')
			if callable(FiscusOnError):
				FiscusOnError({'error': fiscus_error, 'message_id': message_id})
			return FiscusResponse(success=False, error=fiscus_error)

		self.logger.debug(f"Sending asynchronous WebSocket message with message_id: {message_id}")
		try:
			message_str = json.dumps(message)

			# Register the callback if provided
			if callback:
				self.callback_async[message_id] = callback
				self.logger.debug(f"Registered callback for message_id: {message_id}")

			future = asyncio.get_event_loop().create_future()
			self.pending_responses_async[message_id] = future

			send_time = time.time()
			self.logger.trace(f"Message prepared to send at {send_time}: {message_str}")
			await self.websocket.send(message_str)
			self.logger.debug(f"Message sent at {send_time}: [REDACTED]")  # Avoid logging sensitive message content

			# Await the expected number of responses
			try:
				self.logger.trace(f"Awaiting response for message_id: {message_id} with timeout: 30 seconds.")
				response_data = await asyncio.wait_for(future, timeout=30)
				response_receive_time = time.time()
				self.logger.debug(f"Received asynchronous response at {response_receive_time}: [REDACTED]")  # Avoid sensitive data

				if response_data.get('success'):
					fiscus_response = FiscusResponse(
						success=True,
						result=response_data.get('data'),
						message_id=message_id
					)
					self.logger.info(f"Received successful asynchronous response for message_id: {message_id}.")
					self.logger.trace(f"Response data: {response_data.get('data')}")
					if callable(FiscusOnSuccess):
						FiscusOnSuccess({'response': fiscus_response})
					return fiscus_response
				else:
					error_msg = response_data.get('error', 'Unknown asynchronous WebSocket error occurred')
					authorization_url = response_data.get('authorizationUrl')
					fiscus_error = FiscusError(
						code=FiscusErrorCode.AUTH_FAILURE if authorization_url else FiscusErrorCode.UNKNOWN_ERROR,
						message=error_msg,
						details={'authorizationUrl': authorization_url} if authorization_url else None
					)
					self.logger.debug(f"Asynchronous WebSocket operation failed with error: {error_msg}")
					if callable(FiscusOnError):
						FiscusOnError({'error': fiscus_error, 'message_id': message_id})
					return FiscusResponse(
						success=False,
						error=fiscus_error,
						message_id=message_id
					)

			except asyncio.TimeoutError:
				self.logger.debug("Asynchronous WebSocket response timed out.")
				fiscus_error = FiscusError(code=FiscusErrorCode.TIMEOUT, message='No response received from asynchronous WebSocket')
				if callable(FiscusOnError):
					FiscusOnError({'error': fiscus_error, 'message_id': message_id})
				return FiscusResponse(
					success=False,
					error=fiscus_error,
					message_id=message_id
				)

		except Exception as e:
			self.logger.debug(f"Exception while sending asynchronous WebSocket message: {e}")
			self.logger.critical("Critical exception encountered in send_websocket_message.")
			if message_id in self.pending_responses_async:
				del self.pending_responses_async[message_id]
			if message_id in self.callback_async:
				self.callback_async.pop(message_id)
			fiscus_error = FiscusError(code=FiscusErrorCode.INTERNAL_ERROR, message=str(e))
			if callable(FiscusOnError):
				FiscusOnError({'error': fiscus_error, 'message_id': message_id})
			return FiscusResponse(
				success=False,
				error=fiscus_error,
				message_id=message_id
			)

	async def stop_websocket_connection(self) -> None:
		"""
		Terminates the asynchronous WebSocket connection gracefully.
		"""
		self.logger.trace("Entering stop_websocket_connection method.")
		if self.websocket_connected and self.websocket:
			self.logger.info("Stopping asynchronous WebSocket connection.")
			try:
				await self.websocket.close()
				self.logger.debug("Asynchronous WebSocket connection closed.")
				if callable(FiscusOnLog):
					FiscusOnLog({'message': 'Asynchronous WebSocket connection closed.'})
			except Exception as e:
				self.logger.debug(f"Error closing asynchronous WebSocket: {e}")
				if callable(FiscusOnError):
					FiscusOnError({'error': FiscusError(code=FiscusErrorCode.INTERNAL_ERROR, message=str(e)), 'message_id': str(uuid.uuid4())})
			self.websocket_connected = False
			self.logger.info("Asynchronous WebSocket connection stopped successfully.")
		else:
			self.logger.warning("Asynchronous WebSocket is not connected; nothing to stop.")

	async def restart_websocket_connection(self, user_id: str) -> None:
		"""
		Restarts the asynchronous WebSocket connection by stopping and then starting it.

		:param user_id: The user ID for authenticating the connection.
		"""
		self.logger.trace("Entering restart_websocket_connection method.")
		self.logger.info("Restarting asynchronous WebSocket connection.")
		await self.stop_websocket_connection()
		await self.start_websocket_connection(user_id)

	async def send_rest_request(
		self, 
		method: FiscusRestType, 
		action: FiscusActionType, 
		headers: Dict[str, Any], 
		data: Any = None, 
		user_id: str = None, 
		operation: str = None
	) -> FiscusResponse:
		"""
		Sends a REST HTTP request based on the action type, adding 'operation' as a path parameter when necessary.
		Returns FiscusResponse instances that handle both standard and user-specific responses.

		:param method: The HTTP method to use (GET, POST, etc.).
		:param action: The action type for determining the endpoint.
		:param headers: The headers to include in the request.
		:param data: The payload for POST requests or query parameters for GET requests.
		:param user_id: The user ID for authenticating the request.
		:param operation: Optional operation parameter for specific actions.
		:return: FiscusResponse object containing the result.
		"""
		self.logger.trace("Entering send_rest_request method.")
		# Force logging level to debug
		self.logger.setLevel(FiscusLogLevel.DEBUG.to_logging_level())

		# Raise error if no user_id is provided
		if not user_id:
			error_message = "User ID is required but was not provided."
			self.logger.debug(error_message)
			if callable(FiscusOnError):
				FiscusOnError({'error': FiscusError(code=FiscusErrorCode.INVALID_REQUEST, message=error_message), 'message_id': str(uuid.uuid4())})
			raise ValueError(error_message)

		# Generate authentication token and prepare headers
		token = generate_token(self.api_key)
		self.logger.debug("Authentication token generated for REST request.")

		# Prepare headers for the REST request
		headers.update({
			'Authorization': f"Bearer {token}",
			'X-User-Id': user_id,
			'X-Api-Key': self.api_key,
		})
		self.logger.trace(
			f"REST request headers updated: { {k: '***' if k == 'Authorization' else v for k, v in headers.items()} }"
		)

		# Get the base URL from the action
		url = self._get_rest_endpoint(action)

		# If the action is USER and an operation is provided, append it as a path parameter
		if action == FiscusActionType.USER and operation:
			url = f"{url}{operation}"
			self.logger.trace(f"Operation '{operation}' appended to URL for USER action.")

		# Log URL and full request details explicitly
		self.logger.debug(
			f"Sending {method.value.upper()} request to URL: {url} with headers: [REDACTED] and data: [REDACTED]"
		)

		try:
			start_time = time.time()
			self.logger.trace(f"REST request initiated at {start_time}.")

			async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
				if method == FiscusRestType.POST:
					self.logger.debug(f"Executing POST request to {url}.")
					async with session.post(url, json=data, headers=headers) as response:
						response_data = await response.json()
						return self._handle_response(response, response_data, action, start_time)

				elif method == FiscusRestType.GET:
					self.logger.debug(f"Executing GET request to {url}.")
					async with session.get(url, headers=headers, params=data) as response:
						response_data = await response.json()
						return self._handle_response(response, response_data, action, start_time)

				else:
					error_message = f"Unsupported HTTP method: {method}"
					self.logger.debug(error_message)
					if callable(FiscusOnError):
						FiscusOnError({'error': FiscusError(code=FiscusErrorCode.INVALID_REQUEST, message=error_message), 'message_id': str(uuid.uuid4())})
					raise ValueError(error_message)

		except Exception as e:
			self.logger.debug(f"Error sending REST request: {e}")
			fiscus_error = FiscusError(
				code=FiscusErrorCode.INTERNAL_ERROR, 
				message=str(e)
			)
			if callable(FiscusOnError):
				FiscusOnError({'error': fiscus_error, 'message_id': str(uuid.uuid4())})
			return FiscusResponse(
				success=False,
				error=fiscus_error,
				message_id=str(uuid.uuid4())
			)

	def _handle_response(self, response, response_data, action, start_time) -> FiscusResponse:
		"""
		Processes HTTP response data into a FiscusResponse, handling both success and error cases.

		:param response: The aiohttp.ClientResponse object.
		:param response_data: The JSON-decoded response data.
		:param action: The action type for determining response handling.
		:param start_time: The timestamp when the request was initiated.
		:return: FiscusResponse object containing the result.
		"""
		response_time = time.time()
		duration = response_time - start_time
		self.logger.trace(f"Request completed in {duration:.2f} seconds with status {response.status}.")

		# Handle authorization errors if present
		if response.status == 403 and "authorizationUrl" in response_data.get("metadata", {}):
			auth_url = response_data["metadata"]["authorizationUrl"]
			self.logger.warning(f"Authorization error encountered. Redirect user to: {auth_url}")
			fiscus_error = FiscusError(
				code=FiscusErrorCode.AUTH_FAILURE,
				message=response_data.get("message", "Authorization required"),
				details={"authorizationUrl": auth_url}
			)
			if callable(FiscusOnAuth):
				FiscusOnAuth({'authorization_url': auth_url, 'message_id': response_data.get("message_id", str(uuid.uuid4()))})
			return FiscusResponse(
				success=False,
				error=fiscus_error,
				message_id=response_data.get("message_id", str(uuid.uuid4()))
			)

		# General error handling for non-200 statuses
		elif response.status != 200:
			error_message = response_data.get('message', f"Non-200 status code: {response.status}")
			self.logger.debug(f"Received {response.status} for URL: {response.url}")
			self.logger.debug(f"Response Data: {response_data}")
			# Check if 'code' exists in response_data, else use UNKNOWN_ERROR
			error_code = response_data.get("code", FiscusErrorCode.UNKNOWN_ERROR.value)
			fiscus_error = FiscusError(
				code=FiscusErrorCode(error_code) if error_code in FiscusErrorCode._value2member_map_ else FiscusErrorCode.UNKNOWN_ERROR,
				message=error_message
			)
			if callable(FiscusOnError):
				FiscusOnError({'error': fiscus_error, 'message_id': response_data.get("message_id", str(uuid.uuid4()))})
			return FiscusResponse(
				success=False,
				error=fiscus_error,
				message_id=response_data.get("message_id", str(uuid.uuid4()))
			)

		# Success handling for USER action type
		elif action == FiscusActionType.USER:
			if response_data.get("success", False):
				self.logger.info("REST USER request successful.")
				result = response_data.get("result") or {"data": response_data.get("data")}
				fiscus_response = FiscusResponse(
					success=True,
					result=result,
					message_id=response_data.get("message_id")
				)
				if callable(FiscusOnSuccess):
					FiscusOnSuccess({'response': fiscus_response})
				return fiscus_response
			else:
				error_message = response_data.get("message", "Unknown error in USER response")
				self.logger.debug(f"REST USER operation failed with error: {error_message}")
				# Extract code from response_data if available, else use UNKNOWN_ERROR
				error_code = response_data.get("code", FiscusErrorCode.UNKNOWN_ERROR.value)
				fiscus_error = FiscusError(
					code=FiscusErrorCode(error_code) if error_code in FiscusErrorCode._value2member_map_ else FiscusErrorCode.UNKNOWN_ERROR,
					message=error_message
				)
				if callable(FiscusOnError):
					FiscusOnError({'error': fiscus_error, 'message_id': response_data.get("message_id", str(uuid.uuid4()))})
				return FiscusResponse(
					success=False,
					error=fiscus_error,
					message_id=response_data.get("message_id")
				)

		# General success handling for other action types
		elif response_data.get("success", False):
			self.logger.info("REST request successful.")
			fiscus_response = FiscusResponse(
				success=True,
				result=response_data,
				message_id=response_data.get("message_id")
			)
			if callable(FiscusOnSuccess):
				FiscusOnSuccess({'response': fiscus_response})
			return fiscus_response

		else:
			error_message = response_data.get("message", "Unknown REST error occurred")
			self.logger.debug(f"REST operation failed with error: {error_message}")
			# Extract code from response_data if available, else use UNKNOWN_ERROR
			error_code = response_data.get("code", FiscusErrorCode.UNKNOWN_ERROR.value)
			fiscus_error = FiscusError(
				code=FiscusErrorCode(error_code) if error_code in FiscusErrorCode._value2member_map_ else FiscusErrorCode.UNKNOWN_ERROR,
				message=error_message
			)
			if callable(FiscusOnError):
				FiscusOnError({'error': fiscus_error, 'message_id': response_data.get("message_id", str(uuid.uuid4()))})
			return FiscusResponse(
				success=False,
				error=fiscus_error,
				message_id=response_data.get("message_id", str(uuid.uuid4()))
			)

	def _get_rest_endpoint(self, action: FiscusActionType) -> str:
		"""
		Retrieves the appropriate REST endpoint URL based on the action.
		This method accepts a FiscusActionType enum.

		:param action: The action type to determine the endpoint.
		:return: The full REST endpoint URL.
		"""
		# Log the action mapping to help debug issues with the rest_endpoint_map
		self.logger.debug(f"Fetching REST endpoint for action: {action}")

		if action not in self.rest_endpoint_map:
			error_message = f"Endpoint for action '{action}' not found in the configuration"
			self.logger.debug(error_message)
			if callable(FiscusOnError):
				FiscusOnError({'error': FiscusError(code=FiscusErrorCode.INVALID_REQUEST, message=error_message), 'message_id': str(uuid.uuid4())})
			raise ValueError(error_message)

		endpoint = self.rest_endpoint_map[action]
		self.logger.debug(f"Selected REST endpoint for '{action}': {endpoint}")
		return f"{self.rest_endpoint}{endpoint}"
