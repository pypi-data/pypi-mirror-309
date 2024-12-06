# fiscus_sdk/user.py

import logging
import asyncio
from typing import Optional, Dict, Any, List, Callable, TYPE_CHECKING
from datetime import datetime, timedelta

from .connector import FiscusConnector
from .audit import FiscusAuditTrail
from .enums import FiscusActionType, FiscusLogLevel, FiscusRestType
from .response import FiscusResponse

if TYPE_CHECKING:
	from .client import FiscusClient  # Avoids circular import during runtime


class FiscusUser:
	"""
	Represents a user in the Fiscus SDK.

	This class provides methods for managing user-specific data, connectors,
	context, roles, and policies. It also facilitates user authentication,
	authorization, and interaction with the Fiscus platform.

	Attributes:
	- `user_id` (str): Unique identifier for the user.
	- `client` (Optional[FiscusClient]): Reference to the parent FiscusClient instance.
	- `context` (Dict[str, Any]): Stores user-specific context variables.
	- `connectors` (Dict[str, FiscusConnector]): Tracks connectors associated with the user.
	- `auth_callback` (Optional[Callable[[str], Dict[str, Any]]]): Callback for providing authentication parameters.
	- `dynamic_preferences` (Dict[str, str]): User preferences influencing connectors and workflows.
	- `roles` (List[str]): Roles assigned to the user.
	- `policies` (List[Dict[str, Any]]): Policies defining RBAC for the user.
	"""

	DEFAULT_CONTEXT_TTL_HOURS = 24  # Default TTL of 24 hours

	def __init__(self, user_id: str, client: Optional['FiscusClient'] = None):
		"""
		Initialize a FiscusUser.

		This method sets up a user instance with a unique identifier and an optional
		reference to the parent FiscusClient. It also initializes context, connectors,
		audit trails, and logging configurations for the user.

		Parameters:
		- `user_id` (str): Unique identifier for the user.
		- `client` (Optional[FiscusClient]): Reference to the parent FiscusClient instance.
		"""
		self.user_id = user_id
		self.client = client
		self.context: Dict[str, Any] = {}
		self.connectors: Dict[str, FiscusConnector] = {}
		self.auth_callback: Optional[Callable[[str], Dict[str, Any]]] = None
		self.dynamic_preferences: Dict[str, str] = {}
		self.roles: List[str] = []  # Use list of roles
		self.policies: List[Dict[str, Any]] = []  # Use policies for RBAC
		self.logger = logging.getLogger(f'.user.{self.user_id}')
		self.logger.setLevel(FiscusLogLevel.DEBUG.to_logging_level())
		self.logger.trace(f"Initializing FiscusUser with user_id: {self.user_id}")
		self.audit_trail = FiscusAuditTrail(
			f'FiscusUser-{self.user_id}', enable_logging=self.client.enable_audit_logging
		)
		self.logger.info("FiscusUser initialized successfully.")

	# Helper method to get the current time in UTC
	def _current_time(self) -> datetime:
		return datetime.utcnow()

	# Helper method to check if a context key has expired
	def _is_context_expired(self, key: str) -> bool:
		context_entry = self.context.get(key)
		if context_entry and 'endedAt' in context_entry:
			return self._current_time() > context_entry['endedAt']
		return False

	# Helper method to calculate the endedAt time
	def _calculate_ended_at(self, ttl_seconds: Optional[int] = None) -> datetime:
		ttl = ttl_seconds or self.DEFAULT_CONTEXT_TTL_HOURS * 3600  # Default to 24 hours in seconds
		return self._current_time() + timedelta(seconds=ttl)

	# Helper method to send user-related data
	def _send_user_data(
		self, 
		data: Dict[str, Any], 
		operation: str, 
		callbacks: Optional[Dict[str, Callable]] = None
	) -> FiscusResponse:
		"""
		Sends user-specific data synchronously to the backend using either WebSocket or REST.

		Parameters:
		- `data` (Dict[str, Any]): Data to be sent to the backend.
		- `operation` (str): Operation name to specify the backend action.
		- `callbacks` (Optional[Dict[str, Callable]]): Callbacks for handling success or error events.

		Returns:
		- `FiscusResponse`: Response object containing success status and result or error message.
		"""
		self.logger.trace("Entering _send_user_data method.")
		self.logger.debug(f"Sending user data for operation '{operation}' with data: [REDACTED]")
		self.audit_trail.record(f'send_{operation}', {'data': 'REDACTED'})

		# Check if WebSocket is connected, otherwise fallback to REST
		if self.client.connection_manager.websocket_sync_connected:
			self.logger.debug("Using WebSocket (synchronous) to send user data.")
			return self.client.orchestrator.send_user_data_via_websocket(
				user=self, 
				data=data, 
				callbacks=callbacks
			)
		else:
			self.logger.info("No live WebSocket connection, falling back to REST for sending user data.")
			# Since send_rest_request is asynchronous, run it synchronously using asyncio.run
			response = asyncio.run(
				self.client.connection_manager.send_rest_request(
					method=FiscusRestType.POST,
					action=FiscusActionType.USER,
					headers={},  # Add necessary headers if any
					data=data,
					user_id=self.user_id,
					operation=operation
				)
			)
			return response  # response is an instance of FiscusResponse

	# Helper method to send user-related data asynchronously
	async def _send_user_data_async(
		self, 
		data: Dict[str, Any], 
		operation: str, 
		callbacks: Optional[Dict[str, Callable]] = None
	) -> FiscusResponse:
		"""
		Sends user-specific data asynchronously to the backend using either WebSocket or REST.

		Parameters:
		- `data` (Dict[str, Any]): Data to be sent to the backend.
		- `operation` (str): Operation name to specify the backend action.
		- `callbacks` (Optional[Dict[str, Callable]]): Callbacks for handling success or error events.

		Returns:
		- `FiscusResponse`: Response object containing success status and result or error message.
		"""
		self.logger.trace("Entering _send_user_data_async method.")
		self.logger.debug(f"Sending user data asynchronously for operation '{operation}' with data: [REDACTED]")
		self.audit_trail.record(f'send_{operation}_async', {'data': 'REDACTED'})

		if self.client.connection_manager.websocket_connected:
			self.logger.debug("Using WebSocket (asynchronous) to send user data.")
			return await self.client.orchestrator.send_user_data_via_websocket(
				user=self, 
				data=data, 
				callbacks=callbacks
			)
		else:
			self.logger.info("No live WebSocket connection, falling back to REST for sending user data asynchronously.")
			response = await self.client.connection_manager.send_rest_request(
				method=FiscusRestType.POST,
				action=FiscusActionType.USER,
				headers={},  # Add necessary headers if any
				data=data,
				user_id=self.user_id,
				operation=operation
			)
			return response  # response is an instance of FiscusResponse

	# Connector Management

	def add_connector(self, connector: str) -> FiscusResponse:
		"""
		Synchronously add a connector to the user's list of connectors.

		Parameters:
		- `connector` (str): Name of the connector to be added (underscore).

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering add_connector method.")
		self.logger.debug(f"Adding connector '{connector}' for user '{self.user_id}'.")

		if connector in self.connectors:
			self.logger.warning(f"FiscusConnector '{connector}' is already added.")
			return FiscusResponse(success=False, error="Connector already exists.")

		connector_instance = FiscusConnector(name=connector, user=self)
		self.connectors[connector] = connector_instance
		self.audit_trail.record('add_connector', {'connector': connector})
		self.logger.info(f"Connector '{connector}' added successfully.")

		# Prepare data for REST request
		data = {
			'connector': connector,
			'data': connector_instance.data or {}
		}
		operation = 'addConnector'

		# Send connector addition event synchronously
		response = self._send_user_data(data, operation)

		# Handle response
		if response.success:
			if response.is_nested and response.nested_success:
				self.logger.debug(f"Connector '{connector}' addition confirmed: {response.nested_data}")
			else:
				self.logger.debug(f"Connector '{connector}' addition confirmed: {response.result}")
		else:
			if response.is_nested:
				self.logger.debug(f"Failed to add connector '{connector}': {response.nested_message}")
				return FiscusResponse(success=False, error=response.nested_message)
			else:
				self.logger.debug(f"Failed to add connector '{connector}': {response.error}")
				return FiscusResponse(success=False, error=response.error)

		return FiscusResponse(success=True, result=response)

	async def add_connector_async(self, connector: str) -> FiscusResponse:
		"""
		Asynchronously add a connector to the user's list of connectors.

		Parameters:
		- `connector` (str): Name of the connector to be added (underscore).

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering add_connector_async method.")
		self.logger.debug(f"Adding connector '{connector}' for user '{self.user_id}' asynchronously.")

		if connector in self.connectors:
			self.logger.warning(f"FiscusConnector '{connector}' is already added (async).")
			return FiscusResponse(success=False, result="Connector already exists.")

		connector_instance = FiscusConnector(name=connector, user=self)
		self.connectors[connector] = connector_instance
		self.audit_trail.record('add_connector', {'connector': connector})
		self.logger.info(f"Connector '{connector}' added successfully (async).")

		# Prepare data for REST request
		data = {
			'connector': connector,
			'data': connector_instance.data or {}
		}
		operation = 'addConnector'

		# Send connector addition event asynchronously
		response = await self._send_user_data_async(data, operation)

		# Handle response
		if response.success:
			if response.is_nested and response.nested_success:
				self.logger.debug(f"Connector '{connector}' addition confirmed asynchronously: {response.nested_data}")
			else:
				self.logger.debug(f"Connector '{connector}' addition confirmed asynchronously: {response.result}")
		else:
			if response.is_nested:
				self.logger.debug(f"Failed to add connector '{connector}' asynchronously: {response.nested_message}")
				return FiscusResponse(success=False, error=response.nested_message)
			else:
				self.logger.debug(f"Failed to add connector '{connector}' asynchronously: {response.error}")
				return FiscusResponse(success=False, error=response.error)

		return FiscusResponse(success=True, result=response)

	def authenticate_connector(self, connector: str, auth_params: Optional[Dict[str, Any]] = None) -> FiscusResponse:
		"""
		Synchronously authenticate a connector using the provided parameters.

		Parameters:
		- `connector` (str): Name (underscore) of the connector to authenticate.
		- `auth_params` (Optional[Dict[str, Any]]): Authentication parameters.

		Returns:
		- `FiscusResponse`: Response object with the user's current access token, an error object, or the authentication URL.
		"""
		self.logger.trace("Entering authenticate_connector method.")
		self.logger.debug(f"Authenticating connector '{connector}' for user '{self.user_id}'.")

		connector_instance = self.connectors.get(connector)

		if not auth_params and self.auth_callback:
			auth_params = self.auth_callback(connector_instance)
			self.logger.trace("Authentication parameters obtained via auth_callback.")

		self.logger.info(f"Connector '{connector}' authenticated successfully.")

		# Send authentication event synchronously
		data = {'connector': connector, 'auth_params': auth_params}
		operation = 'authenticateConnector'
		response = self._send_user_data(data, operation)

		# Check for successful authentication and handle empty result case
		if response.success:
			authorization_url = response.to_json().get("result", {}).get("data")
			
			# Handle empty result
			if not authorization_url:
				self.logger.info(f"No authentication needed for connector '{connector}' as the result is empty.")
				return FiscusResponse(success=True, result="No authentication needed for this connector")
			
			self.logger.debug(f"Authentication for connector '{connector}' confirmed with URL: {authorization_url}")
			return FiscusResponse(success=True, result=authorization_url)  # Only return the URL itself as result

		# If unsuccessful, handle error as before
		self.logger.debug(f"Failed to authenticate connector '{connector}': {response.error}")
		return FiscusResponse(success=False, error=response.error)

	async def authenticate_connector_async(self, connector: str, auth_params: Optional[Dict[str, Any]] = None) -> FiscusResponse:
		"""
		Asynchronously authenticate a connector using the provided parameters.

		Parameters:
		- `connector` (str): Name of the connector to authenticate.
		- `auth_params` (Optional[Dict[str, Any]]): Authentication parameters.

		Returns:
		- `FiscusResponse`: Response object with the user's current access token, an error object, or the authentication URL.
		"""
		self.logger.trace("Entering authenticate_connector_async method.")
		self.logger.debug(f"Authenticating connector '{connector}' for user '{self.user_id}' asynchronously.")

		connector_instance = self.connectors.get(connector)

		if not auth_params and self.auth_callback:
			auth_params = self.auth_callback(connector_instance)
			self.logger.trace("Authentication parameters obtained via auth_callback (async).")

		self.logger.info(f"Connector '{connector}' authenticated successfully (async).")

		# Send authentication event asynchronously
		data = {'connector': connector, 'auth_params': auth_params}
		operation = 'authenticateConnector'
		response = await self._send_user_data_async(data, operation)

		# Check for successful authentication and handle empty result case
		if response.success:
			authorization_url = response.to_json().get("result", {}).get("data")
			
			# Handle empty result
			if not authorization_url:
				self.logger.info(f"No authentication needed for connector '{connector}' as the result is empty (async).")
				return FiscusResponse(success=True, result="No authentication needed for this connector")
			
			self.logger.debug(f"Authentication for connector '{connector}' confirmed with URL (async): {authorization_url}")
			return FiscusResponse(success=True, result=authorization_url)  # Only return the URL itself as result

		# If unsuccessful, handle error as before
		self.logger.debug(f"Failed to authenticate connector '{connector}' asynchronously: {response.error}")
		return FiscusResponse(success=False, error=response.error)

	def deauthenticate_connector(self, connector: str) -> FiscusResponse:
		"""
		Synchronously deauthenticate a connector.

		Parameters:
		- `connector` (str): Name of the connector to deauthenticate.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering deauthenticate_connector method.")
		self.logger.debug(f"Deauthenticating connector '{connector}' for user '{self.user_id}'.")

		connector_instance = self.connectors.get(connector)

		# Send deauthentication event synchronously
		data = {'connector': connector}
		operation = 'deauthenticateConnector'
		response = self._send_user_data(data, operation)
		if response.success:
			self.logger.debug(f"Deauthentication for connector '{connector}' confirmed via response.")
			if connector_instance is not None:
				connector_instance.authenticated = False
				connector_instance.credentials = None
				self.logger.info(f"Connector '{connector}' deauthenticated in memory.")
		else:
			self.logger.debug(f"Failed to deauthenticate connector '{connector}': {response.error}")
			return FiscusResponse(success=False, error=response.error)
		
		return FiscusResponse(success=True, result=response.result)

	async def deauthenticate_connector_async(self, connector: str) -> FiscusResponse:
		"""
		Asynchronously deauthenticate a connector.

		Parameters:
		- `connector` (str): Name of the connector to deauthenticate.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering deauthenticate_connector_async method.")
		self.logger.debug(f"Deauthenticating connector '{connector}' for user '{self.user_id}' asynchronously.")

		connector_instance = self.connectors.get(connector)

		# Send deauthentication event asynchronously
		data = {'connector': connector}
		operation = 'deauthenticateConnector'
		response = await self._send_user_data_async(data, operation)

		if response.success:
			self.logger.debug(f"Deauthentication for connector '{connector}' confirmed via asynchronous response.")
			if connector_instance is not None:
				connector_instance.authenticated = False
				connector_instance.credentials = None
				self.logger.info(f"Connector '{connector}' deauthenticated in memory (async).")
		else:
			self.logger.debug(f"Failed to deauthenticate connector '{connector}' asynchronously: {response.error}")
			return FiscusResponse(success=False, error=response.error)
		
		return FiscusResponse(success=True, result=response.result)
	
	def list_connectors(self) -> FiscusResponse:
		"""
		Synchronously list all connected connectors & any user data associated by fetching data from the backend.

		Returns:
		- `FiscusResponse`: Response object containing a list of connector names or error details.
		"""
		self.logger.trace("Entering list_connected_connectors method.")
		
		# Define the operation name and empty body as per backend configuration
		operation = 'listConnectorsData'
		data = {}  # Empty body for GET-like operation
		
		# Fetch connected categories using _send_user_data
		response_categories = self._send_user_data(data, operation)
		
		if not response_categories.success:
			self.logger.debug(f"Error fetching connected categories: {response_categories.error}")
			self.audit_trail.record('list_connected_connectors', {'error': response_categories.error})
			return FiscusResponse(success=False, error=response_categories.error)
		
		# Get categories and use them to fetch connectors
		categories = response_categories.results
		data_connectors = {'categories': categories}
		response_connectors = self._send_user_data(data_connectors, operation)
		
		if not response_connectors.success:
			self.logger.debug(f"Error fetching connectors for categories {categories}: {response_connectors.error}")
			self.audit_trail.record('list_connected_connectors', {'error': response_connectors.error})
			return FiscusResponse(success=False, error=response_connectors.error)
		
		connectors = response_connectors.results
		self.audit_trail.record('list_connected_connectors', {'connectors': connectors})
		self.logger.debug(f"Listing connected connectors: {connectors}")
		# Wrap connectors list in a FiscusResponse before returning
		return FiscusResponse(success=True, result=connectors)

	async def list_connectors_async(self) -> FiscusResponse:
		"""
		Asynchronously list all connected connectors & any user data associated by fetching data from the backend.

		Returns:
		- `FiscusResponse`: Response object containing a list of connector names or error details.
		"""
		self.logger.trace("Entering list_connected_connectors_async method.")
		
		# Define the operation name and empty body as per backend configuration
		operation = 'listConnectorsData'
		data = {}  # Empty body for GET-like operation
		
		# Fetch connected categories using _send_user_data_async
		response_categories = await self._send_user_data_async(data, operation)
		
		if not response_categories.success:
			self.logger.debug(f"Error fetching connected categories asynchronously: {response_categories.error}")
			self.audit_trail.record('list_connected_connectors_async', {'error': response_categories.error})
			return FiscusResponse(success=False, error=response_categories.error)
		
		# Get categories and use them to fetch connectors
		categories = response_categories.results
		data_connectors = {'categories': categories}
		response_connectors = await self._send_user_data_async(data_connectors, operation)
		
		if not response_connectors.success:
			self.logger.debug(f"Error fetching connectors for categories {categories} asynchronously: {response_connectors.error}")
			self.audit_trail.record('list_connected_connectors_async', {'error': response_connectors.error})
			return FiscusResponse(success=False, error=response_connectors.error)
		
		connectors = response_connectors.results
		self.audit_trail.record('list_connected_connectors_async', {'connectors': connectors})
		self.logger.debug(f"Listing connected connectors asynchronously: {connectors}")
		return FiscusResponse(success=True, result=connectors)

	def list_connected_connectors(self) -> FiscusResponse:
		"""
		Synchronously list all connected connector names by fetching data from the backend.

		Returns:
		- `FiscusResponse`: Response object containing a list of connector names or error details.
		"""
		self.logger.trace("Entering list_connected_connectors method.")
		
		# Define the operation name and empty body as per backend configuration
		operation = 'listConnectedConnectors'
		data = {}  # Empty body for GET-like operation
		
		# Fetch connected categories using _send_user_data
		response_categories = self._send_user_data(data, operation)
		
		if not response_categories.success:
			self.logger.debug(f"Error fetching connected categories: {response_categories.error}")
			self.audit_trail.record('list_connected_connectors', {'error': response_categories.error})
			return FiscusResponse(success=False, error=response_categories.error)
		
		# Get categories and use them to fetch connectors
		categories = response_categories.result
		data_connectors = {'categories': categories}
		response_connectors = self._send_user_data(data_connectors, operation)
		
		if not response_connectors.success:
			self.logger.debug(f"Error fetching connectors for categories {categories}: {response_connectors.error}")
			self.audit_trail.record('list_connected_connectors', {'error': response_connectors.error})
			return FiscusResponse(success=False, error=response_connectors.error)
		
		connectors = response_connectors.result
		self.audit_trail.record('list_connected_connectors', {'connectors': connectors})
		self.logger.debug(f"Listing connected connectors: {connectors}")
		return FiscusResponse(success=True, result=connectors)

	async def list_connected_connectors_async(self) -> FiscusResponse:
		"""
		Asynchronously list all connected connector names by fetching data from the backend.

		Returns:
		- `FiscusResponse`: Response object containing a list of connector names or error details.
		"""
		self.logger.trace("Entering list_connected_connectors_async method.")
		
		# Define the operation name and empty body as per backend configuration
		operation = 'listConnectedConnectors'
		data = {}  # Empty body for GET-like operation
		
		# Fetch connected categories using _send_user_data_async
		response_categories = await self._send_user_data_async(data, operation)
		
		if not response_categories.success:
			self.logger.debug(f"Error fetching connected categories asynchronously: {response_categories.error}")
			self.audit_trail.record('list_connected_connectors_async', {'error': response_categories.error})
			return FiscusResponse(success=False, error=response_categories.error)
		
		# Get categories and use them to fetch connectors
		categories = response_categories.result
		data_connectors = {'categories': categories}
		response_connectors = await self._send_user_data_async(data_connectors, operation)
		
		if not response_connectors.success:
			self.logger.debug(f"Error fetching connectors for categories {categories} asynchronously: {response_connectors.error}")
			self.audit_trail.record('list_connected_connectors_async', {'error': response_connectors.error})
			return FiscusResponse(success=False, error=response_connectors.error)
		
		connectors = response_connectors.result
		self.audit_trail.record('list_connected_connectors_async', {'connectors': connectors})
		self.logger.debug(f"Listing connected connectors asynchronously: {connectors}")
		return FiscusResponse(success=True, result=connectors)

	def _get_connected_categories(self) -> List[str]:
		"""
		Private method to retrieve connected categories by calling the backend.
		
		:return: List of connected categories.
		"""
		self.logger.trace("Entering _get_connected_categories method.")

		operation = 'getConnectedCategories'
		data = {}  # Empty body for GET-like operation

		# Send the request synchronously
		response = self._send_user_data(data, operation)
		
		if response.success:
			categories = response.result  # Assuming the backend returns the array directly
			self.audit_trail.record('_get_connected_categories', {'categories': categories})
			self.logger.debug(f"Retrieved connected categories: {categories}")
			return categories
		else:
			self.logger.debug(f"Failed to retrieve connected categories: {response.error}")
			self.audit_trail.record('_get_connected_categories', {'error': response.error})
			return []

	async def _get_connected_categories_async(self) -> List[str]:
		"""
		Asynchronously retrieve connected categories by calling the backend.
		
		:return: List of connected categories.
		"""
		self.logger.trace("Entering _get_connected_categories_async method.")

		operation = 'getConnectedCategories'
		data = {}  # Empty body for GET-like operation

		# Send the request asynchronously
		response = await self._send_user_data_async(data, operation)
		
		if response.success:
			categories = response.result  # Assuming the backend returns the array directly
			self.audit_trail.record('_get_connected_categories_async', {'categories': categories})
			self.logger.debug(f"Retrieved connected categories asynchronously: {categories}")
			return categories
		else:
			self.logger.debug(f"Failed to retrieve connected categories asynchronously: {response.error}")
			self.audit_trail.record('_get_connected_categories_async', {'error': response.error})
			return []

	def _get_connected_connectors(self, categories: List[str]) -> List[str]:
		"""
		Private method to retrieve connectors associated with specified categories by calling the backend.
		
		:param categories: List of category names.
		:return: List of connector names within the specified categories.
		"""
		self.logger.trace("Entering _get_connected_connectors method.")

		operation = 'getConnectedCategoriesConnectors'
		data = {'categories': categories}

		# Send the request synchronously
		response = self._send_user_data(data, operation)
		
		if response.success:
			connectors = response.result  # Assuming the backend returns the array directly
			self.audit_trail.record('_get_connected_connectors', {'categories': categories, 'connectors': connectors})
			self.logger.debug(f"Retrieved connectors for categories {categories}: {connectors}")
			return connectors
		else:
			self.logger.debug(f"Failed to retrieve connectors for categories {categories}: {response.error}")
			self.audit_trail.record('_get_connected_connectors', {'error': response.error})
			return []

	async def _get_connected_connectors_async(self, categories: List[str]) -> List[str]:
		"""
		Asynchronously retrieve connectors associated with specified categories by calling the backend.
		
		:param categories: List of category names.
		:return: List of connector names within the specified categories.
		"""
		self.logger.trace("Entering _get_connected_connectors_async method.")

		operation = 'getConnectedCategoriesConnectors'
		data = {'categories': categories}

		# Send the request asynchronously
		response = await self._send_user_data_async(data, operation)
		
		if response.success:
			connectors = response.result  # Assuming the backend returns the array directly
			self.audit_trail.record('_get_connected_connectors_async', {'categories': categories, 'connectors': connectors})
			self.logger.debug(f"Retrieved connectors for categories {categories} asynchronously: {connectors}")
			return connectors
		else:
			self.logger.debug(f"Failed to retrieve connectors for categories {categories} asynchronously: {response.error}")
			self.audit_trail.record('_get_connected_connectors_async', {'error': response.error})
			return []

	from typing import List, Dict, Any

	def _get_connected_operations(self, connectors: List[str], expand: bool = False) -> Dict[str, Any]:
		"""
		Private method to retrieve operations associated with specified connectors by calling the backend.
		
		:param connectors: List of connector names.
		:param expand: Flag indicating whether to fetch expanded operations data. Defaults to False.
		:return: Dictionary mapping connector names to their respective operations or expanded operations.
		"""
		self.logger.trace("Entering _get_connected_operations method.")

		operation = 'getConnectedConnectorsOperations'
		data = {
			'connectors': connectors,
			'expand': expand  # Include the expand flag in the request payload
		}

		# Send the request synchronously
		response = self._send_user_data(data, operation)
		
		if response.success:
			operations_map = response.result  # Backend returns either operation names or expanded data based on the flag
			self.audit_trail.record('_get_connected_operations', {
				'connectors': connectors,
				'expand': expand,
				'operations': operations_map
			})
			self.logger.debug(
				f"Retrieved {'expanded ' if expand else ''}operations for connectors {connectors}: {operations_map}"
			)
			return operations_map
		else:
			self.logger.debug(
				f"Failed to retrieve {'expanded ' if expand else ''}operations for connectors {connectors}: {response.error}"
			)
			self.audit_trail.record('_get_connected_operations', {
				'expand': expand,
				'error': response.error
			})
			return {}

	async def _get_connected_operations_async(self, connectors: List[str], expand: bool = False) -> Dict[str, Any]:
		"""
		Asynchronously retrieve operations associated with specified connectors by calling the backend.
		
		:param connectors: List of connector names.
		:param expand: Flag indicating whether to fetch expanded operations data. Defaults to False.
		:return: Dictionary mapping connector names to their respective operations or expanded operations.
		"""
		self.logger.trace("Entering _get_connected_operations_async method.")

		operation = 'getConnectedConnectorsOperations'
		data = {
			'connectors': connectors,
			'expand': expand  # Include the expand flag in the request payload
		}

		# Send the request asynchronously
		response = await self._send_user_data_async(data, operation)
		
		if response.success:
			operations_map = response.result  # Backend returns either operation names or expanded data based on the flag
			self.audit_trail.record('_get_connected_operations_async', {
				'connectors': connectors,
				'expand': expand,
				'operations': operations_map
			})
			self.logger.debug(
				f"Retrieved {'expanded ' if expand else ''}operations for connectors {connectors} asynchronously: {operations_map}"
			)
			return operations_map
		else:
			self.logger.debug(
				f"Failed to retrieve {'expanded ' if expand else ''}operations for connectors {connectors} asynchronously: {response.error}"
			)
			self.audit_trail.record('_get_connected_operations_async', {
				'expand': expand,
				'error': response.error
			})
			return {}

	# Context Management

	def set_context(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> FiscusResponse:
		"""
		Synchronously set a context variable for the user with an optional TTL.

		Parameters:
		- `key` (str): Key of the context variable.
		- `value` (Any): Value to be assigned to the context variable.
		- `ttl_seconds` (Optional[int]): Time-to-live in seconds for the context variable.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering set_context method.")
		
		# Calculate TTL and set createdAt and endedAt timestamps
		created_at = self._current_time()
		ended_at = self._calculate_ended_at(ttl_seconds)

		# Store the context in a nested format directly under the key
		self.context[key] = {
			'value': value,
			'createdAt': created_at,
			'endedAt': ended_at
		}
		self.audit_trail.record('set_context', {'key': key, 'value': value, 'createdAt': created_at, 'endedAt': ended_at})
		self.logger.debug(f"Context variable set: {key} = {value}, TTL = {ttl_seconds} seconds")

		# Send the context update event synchronously with nested structure
		data = {
			key: {
				'value': value,
				'createdAt': created_at.isoformat(),
				'endedAt': ended_at.isoformat()
			}
		}
		operation = 'setContext'
		response = self._send_user_data(data, operation)
		if response.success:
			self.logger.debug(f"Context '{key}' updated successfully via response.")
		else:
			self.logger.debug(f"Failed to update context '{key}': {response.error}")
			return FiscusResponse(success=False, error=response.error)

		return FiscusResponse(success=True, result=response)

	async def set_context_async(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> FiscusResponse:
		"""
		Asynchronously set a context variable for the user with an optional TTL.

		Parameters:
		- `key` (str): Key of the context variable.
		- `value` (Any): Value to be assigned to the context variable.
		- `ttl_seconds` (Optional[int]): Time-to-live in seconds for the context variable.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering set_context_async method.")

		# Calculate TTL and set createdAt and endedAt timestamps
		created_at = self._current_time()
		ended_at = self._calculate_ended_at(ttl_seconds)

		# Store the context in a nested format directly under the key
		self.context[key] = {
			'value': value,
			'createdAt': created_at,
			'endedAt': ended_at
		}
		self.audit_trail.record('set_context', {'key': key, 'value': value, 'createdAt': created_at, 'endedAt': ended_at})
		self.logger.debug(f"Context variable set asynchronously: {key} = {value}, TTL = {ttl_seconds} seconds")

		# Send the context update event asynchronously with nested structure
		data = {
			key: {
				'value': value,
				'createdAt': created_at.isoformat(),
				'endedAt': ended_at.isoformat()
			}
		}
		operation = 'setContext'
		response = await self._send_user_data_async(data, operation)
		if response.success:
			self.logger.debug(f"Context '{key}' updated successfully via asynchronous response.")
		else:
			self.logger.debug(f"Failed to update context '{key}' asynchronously: {response.error}")
			return FiscusResponse(success=False, error=response.error)

		return FiscusResponse(success=True, result=response)

	def get_context(self, key: Optional[str] = None) -> FiscusResponse:
		"""
		Synchronously retrieve a context variable or all context if no key is specified.

		Parameters:
		- `key` (Optional[str]): Key of the context variable to retrieve. Defaults to `None`.

		Returns:
		- `FiscusResponse`: Response object containing the context value(s) or error details.
		"""
		self.logger.trace("Entering get_context method.")
		
		# Define operation and prepare data
		operation = 'getContext'
		data = {'key': key} if key else {}

		# Fetch context from backend
		response = self._send_user_data(data, operation)
		
		if response.success:
			context_entry = response.result
			result = context_entry.get('value') if key else context_entry
			self.audit_trail.record('get_context', {'key': key, 'value': result})
			self.logger.debug(f"Retrieved context variable: {key} = {result}")
			return FiscusResponse(success=True, result={'key': key, 'value': result} if key else result)
		else:
			error_message = f"Context key '{key}' not found or retrieval failed." if key else "Failed to retrieve context."
			self.logger.debug(error_message)
			self.audit_trail.record('get_context', {'key': key, 'error': error_message})
			return FiscusResponse(success=False, error=response.error)

	async def get_context_async(self, key: Optional[str] = None) -> FiscusResponse:
		"""
		Asynchronously retrieve a context variable or all context if no key is specified.

		Parameters:
		- `key` (Optional[str]): Key of the context variable to retrieve. Defaults to `None`.

		Returns:
		- `FiscusResponse`: Response object containing the context value(s) or error details.
		"""
		self.logger.trace("Entering get_context_async method.")
		
		# Define operation and prepare data
		operation = 'getContext'
		data = {'key': key} if key else {}

		# Fetch context from backend asynchronously
		response = await self._send_user_data_async(data, operation)
		
		if response.success:
			context_entry = response.result
			result = context_entry.get('value') if key else context_entry
			self.audit_trail.record('get_context_async', {'key': key, 'value': result})
			self.logger.debug(f"Retrieved context variable asynchronously: {key} = {result}")
			return FiscusResponse(success=True, result={'key': key, 'value': result} if key else result)
		else:
			error_message = f"Context key '{key}' not found or retrieval failed." if key else "Failed to retrieve context."
			self.logger.debug(error_message)
			self.audit_trail.record('get_context_async', {'key': key, 'error': error_message})
			return FiscusResponse(success=False, error=response.error)

	# Policy Management

	def has_permission(self, connector: str, operation: str) -> bool:
		"""
		Check if the user has permission for an operation.
		"""
		self.logger.trace("Entering has_permission method.")
		if not self.roles and not self.policies:
			self.logger.debug("No roles or policies defined. Granting permission by default.")
			self.audit_trail.record('has_permission', {'connector': connector, 'operation': operation, 'has_permission': True})
			return True

		for policy in self.policies:
			if self._evaluate_policy(policy, connector, operation):
				self.logger.debug(f"Permission granted by policy: {policy}")
				self.audit_trail.record('has_permission', {'connector': connector, 'operation': operation, 'has_permission': True})
				return True

		self.logger.info(f"Permission denied for operation '{operation}' on connector '{connector}'.")
		self.audit_trail.record('has_permission', {'connector': connector, 'operation': operation, 'has_permission': False})
		return False

	def _evaluate_policy(self, policy: Dict[str, Any], connector: str, operation: str) -> bool:
		"""
		Evaluate a policy to determine if it grants permission.
		"""
		self.logger.trace("Entering _evaluate_policy method.")
		if 'roles' in policy and not any(role in self.roles for role in policy['roles']):
			self.logger.debug("Policy roles do not match user's roles.")
			return False

		if 'connectors' in policy and '*' not in policy['connectors'] and connector not in policy['connectors']:
			self.logger.debug("Policy connectors do not include the specified connector.")
			return False

		if 'operations' in policy and '*' not in policy['operations'] and operation not in policy['operations']:
			self.logger.debug("Policy operations do not include the specified operation.")
			return False

		if 'conditions' in policy and not policy['conditions'](self, self.context):
			self.logger.debug("Policy conditions are not met.")
			return False

		self.logger.debug("Policy evaluation passed.")
		return True

	# Role Management

	def assign_role(self, role: str) -> FiscusResponse:
		"""
		Synchronously assign a role to the user.

		Parameters:
		- `role` (str): Role to be assigned to the user.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering assign_role method.")
		if role not in self.roles:
			self.roles.append(role)
			self.audit_trail.record('assign_role', {'role': role})
			self.logger.info(f"Role '{role}' assigned to user '{self.user_id}'.")

			# Send role assignment event synchronously
			data = {'role': role}
			operation = 'assignRole'
			response = self._send_user_data(data, operation)
			if response.success:
				self.logger.debug(f"Role '{role}' assignment confirmed via response.")
			else:
				self.logger.debug(f"Failed to assign role '{role}': {response.error}")
				return FiscusResponse(success=False, error=response.error)
		else:
			self.logger.warning(f"Role '{role}' is already assigned to user '{self.user_id}'.")
			return FiscusResponse(success=False, error="Role already assigned.")
		
		return FiscusResponse(success=True, result=response)

	async def assign_role_async(self, role: str) -> FiscusResponse:
		"""
		Asynchronously assign a role to the user.

		Parameters:
		- `role` (str): Role to be assigned to the user.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering assign_role_async method.")
		if role not in self.roles:
			self.roles.append(role)
			self.audit_trail.record('assign_role', {'role': role})
			self.logger.info(f"Role '{role}' assigned to user '{self.user_id}' asynchronously.")

			# Send role assignment event asynchronously
			data = {'role': role}
			operation = 'assignRole'
			response = await self._send_user_data_async(data, operation)
			if response.success:
				self.logger.debug(f"Role '{role}' assignment confirmed via asynchronous response.")
			else:
				self.logger.debug(f"Failed to assign role '{role}' asynchronously: {response.error}")
				return FiscusResponse(success=False, error=response.error)
		else:
			self.logger.warning(f"Role '{role}' is already assigned to user '{self.user_id}' (async).")
			return FiscusResponse(success=False, error="Role already assigned.")
		
		return FiscusResponse(success=True, result=response)

	def add_policy(self, policy: Dict[str, Any]) -> FiscusResponse:
		"""
		Synchronously add a policy for the user.

		Parameters:
		- `policy` (Dict[str, Any]): Policy definition to be added.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering add_policy method.")
		self.policies.append(policy)
		self.audit_trail.record('add_policy', {'policy': policy})
		self.logger.info(f"Policy added successfully for user '{self.user_id}'.")

		# Send policy addition event synchronously
		data = {'policy': policy}
		operation = 'addPolicy'
		response = self._send_user_data(data, operation)
		
		if response.success:
			self.logger.debug("Policy addition confirmed via response.")
			self.audit_trail.record('add_policy_async: User ID change confirmed via response')
		else:
			self.logger.debug(f"Failed to add policy: {response.error}")
			self.audit_trail.record('add_policy_async', {'error': response.error})
			return FiscusResponse(success=False, error=response.error)

		return FiscusResponse(success=True, result=response)

	async def add_policy_async(self, policy: Dict[str, Any]) -> FiscusResponse:
		"""
		Asynchronously add a policy for the user.

		Parameters:
		- `policy` (Dict[str, Any]): Policy definition to be added.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering add_policy_async method.")
		self.policies.append(policy)
		self.audit_trail.record('add_policy', {'policy': policy})
		self.logger.info(f"Policy added successfully for user '{self.user_id}' asynchronously.")

		# Send policy addition event asynchronously
		data = {'policy': policy}
		operation = 'addPolicy'
		response = await self._send_user_data_async(data, operation)

		if response.success:
			self.logger.debug("Policy addition confirmed via asynchronous response.")
			self.audit_trail.record('add_policy_async: User ID change confirmed via asynchronous response')
		else:
			self.logger.debug(f"Failed to add policy asynchronously: {response.error}")
			self.audit_trail.record('add_policy_async', {'error': response.error})
			return FiscusResponse(success=False, error=response.error)

		return FiscusResponse(success=True, result=response)

	# User ID Management

	def set_user_id(self, new_user_id: str) -> FiscusResponse:
		"""
		Synchronously set a new user ID.

		Parameters:
		- `new_user_id` (str): New user ID to be assigned.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering set_user_id method.")
		old_user_id = self.user_id
		self.logger.debug(f"Changing user ID from '{old_user_id}' to '{new_user_id}'.")
		self.audit_trail.record('set_user_id', {'old_user_id': old_user_id, 'new_user_id': new_user_id})
		self.user_id = new_user_id
		self.logger.info(f"User ID changed from '{old_user_id}' to '{new_user_id}'.")

		# Send user ID change event synchronously
		data = {'oldUserId': old_user_id, 'newUserId': new_user_id}
		operation = 'setUserId'
		response = self._send_user_data(data, operation)

		if response.success:
			self.logger.debug("User ID change confirmed via response.")
			self.audit_trail.record('set_user_id_async: User ID change confirmed via response')
		else:
			self.logger.debug(f"Failed to change user ID: {response.error}")
			self.audit_trail.record('set_user_id_async', {'error': response.error})
			return FiscusResponse(success=False, error=response.error)

		return FiscusResponse(success=True, result=response)

	async def set_user_id_async(self, new_user_id: str) -> FiscusResponse:
		"""
		Asynchronously set a new user ID.

		Parameters:
		- `new_user_id` (str): New user ID to be assigned.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering set_user_id_async method.")
		old_user_id = self.user_id
		self.logger.debug(f"Changing user ID from '{old_user_id}' to '{new_user_id}' asynchronously.")
		self.audit_trail.record('set_user_id', {'old_user_id': old_user_id, 'new_user_id': new_user_id})
		self.user_id = new_user_id
		self.logger.info(f"User ID changed from '{old_user_id}' to '{new_user_id}' asynchronously.")

		# Send user ID change event asynchronously
		data = {'oldUserId': old_user_id, 'newUserId': new_user_id}
		operation = 'setUserId'
		response = await self._send_user_data_async(data, operation)

		if response.success:
			self.logger.debug(f"User ID change confirmed via asynchronous response.")
			self.audit_trail.record('set_user_id_async: User ID change confirmed via asynchronous response')
		else:
			self.logger.debug(f"Failed to change user ID asynchronously: {response.error}")
			self.audit_trail.record('set_user_id_async', {'error': response.error})
			return FiscusResponse(success=False, error=response.error)

		return FiscusResponse(success=True, result=response)

	# Connectors Info

	# def get_connectors_info(self) -> Dict[str, Any]:
	# 	"""
	# 	Get information about available connectors by fetching from the backend.
		
	# 	:return: Dictionary of connector information.
	# 	"""
	# 	self.logger.trace("Entering get_connectors_info method.")

	# 	operation = 'listConnectorsData'
	# 	data = {}  # Empty body for GET-like operation

	# 	# Send the request synchronously
	# 	response = self._send_user_data(data, operation)

	# 	if response.success:
	# 		self.logger.debug(f"Retrieved connectors info: {response}")
	# 		self.audit_trail.record('get_connectors_info_async', {'info': response})
	# 	else:
	# 		self.logger.debug(f"Failed to retrieve connectors info: {response.error}")
	# 		self.audit_trail.record('get_connectors_info_async', {'error': response.error})
	# 		return FiscusResponse(success=False, error=response.error)
		
	# 	return FiscusResponse(success=True, result=response)

	# async def get_connectors_info_async(self) -> Dict[str, Any]:
	# 	"""
	# 	Asynchronously get information about available connectors by fetching from the backend.
		
	# 	:return: Dictionary of connector information.
	# 	"""
	# 	self.logger.trace("Entering get_connectors_info_async method.")

	# 	operation = 'listConnectorsData'
	# 	data = {}  # Empty body for GET-like operation

	# 	# Send the request asynchronously
	# 	response = await self._send_user_data_async(data, operation)

	# 	if response.success:
	# 		self.logger.debug(f"Retrieved connectors info asynchronously: {response}")
	# 		self.audit_trail.record('get_connectors_info_async', {'info': response})
	# 	else:
	# 		self.logger.debug(f"Failed to retrieve connectors info asynchronously: {response.error}")
	# 		self.audit_trail.record('get_connectors_info_async', {'error': response.error})
	# 		return FiscusResponse(success=False, error=response.error)

	# 	return FiscusResponse(success=True, result=response)

	# Dynamic Preferences

	def set_dynamic_preferences(self, preferences: Dict[str, str]) -> FiscusResponse:
		"""
		Synchronously set dynamic preferences for connectors and workflows.

		Parameters:
		- `preferences` (Dict[str, str]): Preferences to be set for the user.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering set_dynamic_preferences method.")
		self.dynamic_preferences = preferences
		self.audit_trail.record('set_dynamic_preferences', {'preferences': preferences})
		self.logger.debug("Dynamic preferences set successfully.")

		# Send dynamic preferences update event synchronously
		data = {'preferences': preferences}
		operation = 'setDynamicPreferences'
		response = self._send_user_data(data, operation)
		if response.success:
			self.logger.debug("Dynamic preferences update confirmed via response.")
		else:
			self.logger.debug(f"Failed to set dynamic preferences: {response.error}")
			return FiscusResponse(success=False, error=response.error)

		return FiscusResponse(success=True, result=response)

	async def set_dynamic_preferences_async(self, preferences: Dict[str, str]) -> FiscusResponse:
		"""
		Asynchronously set dynamic preferences for connectors and workflows.

		Parameters:
		- `preferences` (Dict[str, str]): Preferences to be set for the user.

		Returns:
		- `FiscusResponse`: Response object indicating success or error details.
		"""
		self.logger.trace("Entering set_dynamic_preferences_async method.")
		self.dynamic_preferences = preferences
		self.audit_trail.record('set_dynamic_preferences', {'preferences': preferences})
		self.logger.debug("Dynamic preferences set successfully (async).")

		# Send dynamic preferences update event asynchronously
		data = {'preferences': preferences}
		operation = 'setDynamicPreferences'
		response = await self._send_user_data_async(data, operation)
		if response.success:
			self.logger.debug("Dynamic preferences update confirmed via asynchronous response.")
		else:
			self.logger.debug(f"Failed to set dynamic preferences asynchronously: {response.error}")
			return FiscusResponse(success=False, error=response.error)

		return FiscusResponse(success=True, result=response)
