# fiscus_sdk/client_base.py

from typing import Optional, Dict, Any, Callable

from .user import FiscusUser
from .response import FiscusResponse
from .audit import FiscusAuditTrail
from .connection import _ConnectionManager
from .orchestrator import _Orchestrator
from .enums import (
	FiscusConnectionType,
	FiscusResponseType,
	FiscusInitType,
	FiscusLogLevel,
)

from .client_ai_execute import _ClientAIExecuteMixin
from .client_logging_config import _ClientConfiguringLoggingMixin
from .client_execute import _ClientExecuteMixin
from .client_user_action import _ClientUserActionMixin


class FiscusClient(
	_ClientAIExecuteMixin,
	_ClientConfiguringLoggingMixin,
	_ClientExecuteMixin,
	_ClientUserActionMixin
):
	"""
	The `FiscusClient` class is the primary interface for interacting with the Fiscus SDK.

	This class enables developers to initialize and manage resources, execute workflows, and perform
	user-specific operations seamlessly. Designed with flexibility in mind, it supports both
	synchronous and asynchronous methods, allowing integration into diverse environments such
	as event-driven systems, web servers, or command-line tools.

	### Key Features:
	- **Connection Management**: Automatically handles WebSocket or REST connections based on configuration.
	- **User Actions**: Provides methods to manage users, roles, policies, and dynamic preferences.
	- **Logging and Auditing**: Built-in logging support, including optional audit trails.
	- **Workflow Execution**: Facilitates task execution through connectors, categories, or AI-driven workflows.
	- **Asynchronous Support**: Supports asynchronous operations for non-blocking workflows.

	### Usage:
	To use the `FiscusClient`, instantiate it with the required parameters such as `api_key` and
	any additional configuration options. The client can be initialized in `LAZY` or `EAGER` mode,
	depending on whether resources should be loaded on demand or upfront.

	Example:
	```python
	from fiscus_sdk import FiscusClient, FiscusLogLevel

	client = FiscusClient(
		api_key="your_api_key",
		logging_level=FiscusLogLevel.INFO,
		connection_type=FiscusConnectionType.REST
	)

	# Perform operations with the client
	await client.execute()
	"""

	def __init__(
		self,
		api_key: str,
		user_id: Optional[str] = None,
		logging_level: Optional[FiscusLogLevel] = None,
		log_to_file: bool = False,
		log_file_path: Optional[str] = None,
		enable_audit_logging: bool = False,
		connection_type: FiscusConnectionType = FiscusConnectionType.WEBSOCKET,
		response_format: FiscusResponseType = FiscusResponseType.JSON,
		retries: int = 3,
		backoff_factor: float = 0.5,
		context_loader: Optional[Callable[[], Dict[str, Any]]] = None,
		context_saver: Optional[Callable[[Dict[str, Any]], None]] = None,
		initialization_mode: FiscusInitType = FiscusInitType.LAZY,
		initialization_async: bool = False,
		llm: Any = None,
		memory: Any = None,
		**kwargs,
	):
		"""
		Initialize the FiscusClient with the provided configuration.

		:param api_key: API key for authenticating requests.
		:param user_id: Optional user ID for user-specific operations.
		:param logging_level: Optional logging level from FiscusLogLevel enum.
		:param log_to_file: Whether to log to a file instead of the console.
		:param log_file_path: Path to the log file if log_to_file is True.
		:param enable_audit_logging: Enable or disable audit trail logging.
		:param connection_type: Type of connection to use (e.g., WEBSOCKET).
		:param response_format: Format of the responses (e.g., TEXT).
		:param retries: Number of retries for failed operations.
		:param backoff_factor: Factor for exponential backoff between retries.
		:param context_loader: Optional callable to load user context.
		:param context_saver: Optional callable to save user context.
		:param initialization_mode: Mode of initialization (LAZY or EAGER).
		:param initialization_async: Whether to initialize asynchronously.
		:param kwargs: Additional custom options.
		"""
		# Store initialization parameters
		self.api_key = api_key
		self.user_id = user_id
		self.enable_audit_logging = enable_audit_logging

		# Initialize audit trail for logging actions
		self.audit_trail = FiscusAuditTrail(
			'FiscusClient', enable_logging=self.enable_audit_logging
		)

		# Configure logging based on provided parameters
		self._configure_logging(logging_level, log_to_file, log_file_path)

		# Store connection and response configurations
		self.connection_type = connection_type
		self.response_format = response_format
		self.retries = retries
		self.backoff_factor = backoff_factor
		self.context_loader = context_loader
		self.context_saver = context_saver
		self.custom_options: Dict[str, Any] = kwargs.get('custom_options', {})
		self.initialization_mode = initialization_mode
		self.initialization_async = initialization_async

		# Initialize default LLM and memory
		self.llm = llm
		self.memory = memory

		# Log client initialization
		self.logger.info("FiscusClient initialized with provided configuration.")

		# Initialize the connection manager with the API key
		self.connection_manager = _ConnectionManager(api_key=self.api_key)
		self.logger.debug("Connection manager initialized successfully.")

		# Initialize orchestrator to manage operations, whether user_id is provided or not
		self.orchestrator = _Orchestrator(
			user=None,  # Initialize without a user initially
			connection_manager=self.connection_manager,
			client=self,
		)
		self.logger.debug("Orchestrator initialized without user context.")

		# If a user_id is provided, initialize the user context and update the orchestrator
		if self.user_id is not None:
			self.logger.debug("User ID provided; initializing user context.")
			self.user = FiscusUser(user_id=self.user_id, client=self)
			if self.context_loader:
				self.user.context = self.context_loader()
				self.logger.debug("User context loaded successfully.")
			# Update the orchestrator with the new user context
			self.orchestrator.user = self.user
			self.logger.debug("Orchestrator updated with user context.")
		else:
			self.logger.warning("User ID not provided; some features may be limited.")
			self.user = None

		# Handle eager initialization based on the initialization mode
		if self.initialization_mode == FiscusInitType.EAGER:
			if self.initialization_async:
				self.logger.debug(
					"Eager asynchronous initialization selected. Please call 'await initialize_async()' after creating the client."
				)
			else:
				self.logger.debug(
					"Eager synchronous initialization selected. Initializing now."
				)
				self.initialize()

	def initialize(self) -> None:
		"""
		Initialize the FiscusClient with the provided configuration.

		This method sets up the FiscusClient, allowing developers to configure connection 
		settings, logging, and user-specific contexts. It serves as the entry point for 
		managing AI-driven workflows and API integrations, providing flexibility and control.

		Parameters:
		- `api_key` (str): The API key used for authenticating requests to the Fiscus platform.
		- `user_id` (Optional[str]): The user ID for user-specific operations. If provided, 
		the client initializes the user context automatically.
		- `logging_level` (Optional[FiscusLogLevel]): The logging level to control verbosity. 
		Defaults to the SDK's standard level.
		- `log_to_file` (bool): Whether to log to a file. Defaults to `False` (logs to console).
		- `log_file_path` (Optional[str]): The path to the log file if `log_to_file` is enabled.
		- `enable_audit_logging` (bool): Enables or disables audit trail logging. Defaults to `False`.
		- `connection_type` (FiscusConnectionType): The type of connection to use 
		(e.g., `WEBSOCKET` or `REST`). Defaults to `WEBSOCKET`.
		- `response_format` (FiscusResponseType): The format of responses from the Fiscus platform 
		(`JSON` or `TEXT`). Defaults to `JSON`.
		- `retries` (int): The number of retries for failed operations. Defaults to `3`.
		- `backoff_factor` (float): The factor for exponential backoff between retries. Defaults to `0.5`.
		- `context_loader` (Optional[Callable[[], Dict[str, Any]]]): A callable to load user context. 
		Useful for initializing stateful workflows. Defaults to `None`.
		- `context_saver` (Optional[Callable[[Dict[str, Any]], None]]): A callable to save user context 
		after execution. Defaults to `None`.
		- `initialization_mode` (FiscusInitType): Controls whether initialization is `LAZY` or `EAGER`. 
		Defaults to `LAZY`.
		- `initialization_async` (bool): Indicates if initialization should be asynchronous. Defaults to `False`.
		- `llm` (Any): Optional LLM instance to be used for AI-driven workflows. Defaults to `None`.
		- `memory` (Any): Optional memory configuration for managing state across executions. Defaults to `None`.
		- `**kwargs`: Additional custom options.

		Example:
		```python
		client = FiscusClient(
			api_key="your_api_key",
			user_id="user_123",
			logging_level=FiscusLogLevel.INFO,
			connection_type=FiscusConnectionType.REST,
			retries=5,
			backoff_factor=1.0
		)
		Notes:

		- If user_id is provided, the client initializes the user context automatically.
		- Use context_loader and context_saver for managing user state in long-running workflows.
		- For eager initialization, set initialization_mode to EAGER and call initialize or initialize_async.
		"""
		self.logger.debug("Starting synchronous initialization.")
		if self.connection_type == FiscusConnectionType.WEBSOCKET:
			if not self.user_id:
				self.logger.debug(
					"User ID not provided; WebSocket initialization deferred until execution."
				)
			else:
				self.logger.info("Starting synchronous WebSocket connection.")
				try:
					self.connection_manager.start_websocket_connection_sync(self.user_id)
					self.logger.info("Synchronous WebSocket connection established successfully.")
				except Exception as e:
					self.logger.critical(f"Failed to establish synchronous WebSocket connection: {e}", exc_info=True)
		self.logger.debug("Synchronous initialization complete.")

	async def initialize_async(self) -> None:
		"""
		Initialize the FiscusClient with the provided configuration.

		This method sets up resources and establishes connections asynchronously. It is
		recommended for applications where non-blocking operations are necessary, such
		as web servers or event-driven workflows.

		Parameters:
		- `api_key` (str): The API key used for authenticating requests to the Fiscus platform.
		- `user_id` (Optional[str]): The user ID for user-specific operations. If provided, 
		the client initializes the user context automatically.
		- `logging_level` (Optional[FiscusLogLevel]): The logging level to control verbosity. 
		Defaults to the SDK's standard level.
		- `log_to_file` (bool): Whether to log to a file. Defaults to `False` (logs to console).
		- `log_file_path` (Optional[str]): The path to the log file if `log_to_file` is enabled.
		- `enable_audit_logging` (bool): Enables or disables audit trail logging. Defaults to `False`.
		- `connection_type` (FiscusConnectionType): The type of connection to use 
		(e.g., `WEBSOCKET` or `REST`). Defaults to `WEBSOCKET`.
		- `response_format` (FiscusResponseType): The format of responses from the Fiscus platform 
		(`JSON` or `TEXT`). Defaults to `JSON`.
		- `retries` (int): The number of retries for failed operations. Defaults to `3`.
		- `backoff_factor` (float): The factor for exponential backoff between retries. Defaults to `0.5`.
		- `context_loader` (Optional[Callable[[], Dict[str, Any]]]): A callable to load user context. 
		Useful for initializing stateful workflows. Defaults to `None`.
		- `context_saver` (Optional[Callable[[Dict[str, Any]], None]]): A callable to save user context 
		after execution. Defaults to `None`.
		- `initialization_mode` (FiscusInitType): Controls whether initialization is `LAZY` or `EAGER`. 
		Defaults to `LAZY`.
		- `initialization_async` (bool): Indicates if initialization should be asynchronous. Defaults to `False`.
		- `llm` (Any): Optional LLM instance to be used for AI-driven workflows. Defaults to `None`.
		- `memory` (Any): Optional memory configuration for managing state across executions. Defaults to `None`.
		- `**kwargs`: Additional custom options.

		Example:
		```python
		client = FiscusClient(
			api_key="your_api_key",
			user_id="user_123",
			logging_level=FiscusLogLevel.INFO,
			connection_type=FiscusConnectionType.REST,
			retries=5,
			backoff_factor=1.0
		)
		Notes:
		- This method must be awaited to complete initialization.
		- If user_id is provided, the client initializes the user context automatically.
		- Use context_loader and context_saver for managing user state in long-running workflows.
		"""
		self.logger.debug("Starting asynchronous initialization.")
		if self.connection_type == FiscusConnectionType.WEBSOCKET:
			if not self.user_id:
				self.logger.debug(
					"User ID not provided; WebSocket initialization deferred until execution."
				)
			else:
				self.logger.info("Starting asynchronous WebSocket connection.")
				try:
					await self.connection_manager.start_websocket_connection(self.user_id)
					self.logger.info("Asynchronous WebSocket connection established successfully.")
				except Exception as e:
					self.logger.critical(f"Failed to establish asynchronous WebSocket connection: {e}", exc_info=True)
		self.logger.debug("Asynchronous initialization complete.")
		
	def _invoke_callback(self, callback: Callable, response: FiscusResponse) -> None:
		"""
		Simplified callback invocation: passes result data or error message.
		"""
		if response.success:
			# If it's a single result, pass that; otherwise, pass the entire batch of results
			result_data = response.result if not response._is_batch else response.results
			callback(result_data)  # Pass only the result data
		else:
			callback({'error': response.error_message})  # Pass error message


	def _handle_response(self, response: FiscusResponse, callbacks: Optional[Dict[str, Callable]] = None):
		"""
		Handles response by invoking the appropriate callbacks.
		If no callbacks are provided, simply return or log the result.
		"""
		# Check if callbacks are provided before proceeding
		if callbacks:
			if response.success:
				success_callback = callbacks.get('fiscus_on_success')
				if success_callback:
					self._invoke_callback(success_callback, response)
			else:
				error_callback = callbacks.get('fiscus_on_error')
				if error_callback:
					self._invoke_callback(error_callback, response)
		else:
			# If no callbacks are provided, you can log or handle the response as needed
			if response.success:
				self.logger.debug(f"Operation successful, result: {response.result or response.results}")
			else:
				self.logger.error(f"Operation failed with error: {response.error_message}")

	def _mask_sensitive_info(self, info: str) -> str:
		"""
		Masks sensitive information in logs to prevent exposure.

		:param info: The sensitive information string.
		:return: Masked string.
		"""
		if not info:
			return ""
		return f"{info[:4]}****{info[-4:]}"
