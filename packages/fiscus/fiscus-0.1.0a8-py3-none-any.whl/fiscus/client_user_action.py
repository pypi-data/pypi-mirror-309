# fiscus_sdk/client_user_action.py

from typing import Optional, Dict, Any

from .user import FiscusUser
from .response import FiscusResponse
from .orchestrator import _Orchestrator
from .enums import (
	FiscusConnectionType,
	FiscusResponseType,
	FiscusActionType,
)


class _ClientUserActionMixin:	
	def user_action(
		self,
		action: FiscusActionType,
		params: Optional[Dict[str, Any]] = None,
		user: Optional[FiscusUser] = None,
		connection_type: Optional[FiscusConnectionType] = None,
		response_format: Optional[FiscusResponseType] = None,
	) -> FiscusResponse:
		"""
		Execute a user action synchronously.

		:param action: The action to perform.
		:param params: Parameters for the action.
		:param user: FiscusUser instance to perform the action.
		:param connection_type: Type of connection to use.
		:param response_format: Format of the response.
		:return: FiscusResponse object containing the result.
		"""
		self.logger.debug(f"Executing synchronous user action: {action}")

		if connection_type is None:
			connection_type = self.connection_type
		if response_format is None:
			response_format = self.response_format
		if params is None:
			params = {}

		if not user and not self.user:
			self.logger.error("User instance must be provided for user action.")
			raise ValueError("A FiscusUser instance must be provided.")
		current_user = user or self.user

		if not current_user.user_id:
			self.logger.critical("User instance with a user_id must be provided for user action.")
			raise ValueError("A FiscusUser instance with a user_id must be provided.")

		data = {'action': action, 'params': params or {}}
		self.logger.debug("User action payload prepared.")

		if not self.orchestrator:
			self.logger.debug("Creating orchestrator for user action.")
			self.orchestrator = _Orchestrator(
				user=current_user, connection_manager=self.connection_manager, client=self
			)
			self.logger.debug("Orchestrator created successfully.")

		try:
			response = self.orchestrator._send_operation_to_server(
				action=FiscusActionType.USER,
				data=data,
				response_format=response_format,
				connection_type=connection_type,
				custom_options=None,
				user=current_user,
			)
			self.logger.info(f"User action '{action}' executed successfully.")
		except Exception as e:
			self.logger.critical(f"User action '{action}' failed: {e}", exc_info=True)
			raise e

		return response

	async def user_action_async(
		self,
		action: FiscusActionType,
		params: Optional[Dict[str, Any]] = None,
		user: Optional[FiscusUser] = None,
		connection_type: Optional[FiscusConnectionType] = None,
		response_format: Optional[FiscusResponseType] = None,
	) -> FiscusResponse:
		"""
		Execute a user action asynchronously.

		:param action: The action to perform.
		:param params: Parameters for the action.
		:param user: FiscusUser instance to perform the action.
		:param connection_type: Type of connection to use.
		:param response_format: Format of the response.
		:return: FiscusResponse object containing the result.
		"""
		self.logger.debug(f"Asynchronously executing user action: {action}")

		if connection_type is None:
			connection_type = self.connection_type
		if response_format is None:
			response_format = self.response_format
		if params is None:
			params = {}

		if not user and not self.user:
			self.logger.error("User instance must be provided for asynchronous user action.")
			raise ValueError("A FiscusUser instance must be provided.")
		current_user = user or self.user

		if not current_user.user_id:
			self.logger.critical("User instance with a user_id must be provided for asynchronous user action.")
			raise ValueError("A FiscusUser instance with a user_id must be provided.")

		data = {'action': action, 'params': params or {}}
		self.logger.debug("Asynchronous user action payload prepared.")

		if not self.orchestrator:
			self.logger.debug("Creating orchestrator for asynchronous user action.")
			self.orchestrator = _Orchestrator(
				user=current_user, connection_manager=self.connection_manager, client=self
			)
			self.logger.debug("Orchestrator created successfully.")

		try:
			response = await self.orchestrator._send_operation_to_server_async(
				action=FiscusActionType.USER,
				data=data,
				response_format=response_format,
				connection_type=connection_type,
				custom_options=None,
				user=current_user,
			)
			self.logger.info(f"Asynchronous user action '{action}' executed successfully.")
		except Exception as e:
			self.logger.critical(f"Asynchronous user action '{action}' failed: {e}", exc_info=True)
			raise e

		return response

