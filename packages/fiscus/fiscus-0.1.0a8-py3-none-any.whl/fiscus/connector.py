# fiscus_sdk/connector.py

import logging
from typing import Dict, Any, Optional, TYPE_CHECKING
from .enums import FiscusConnectionType
from .response import FiscusResponse
from .exceptions import FiscusAuthenticationError
from .audit import FiscusAuditTrail

if TYPE_CHECKING:
    from .user import FiscusUser  # Avoids circular import during runtime


class FiscusConnector:
    """
    Represents an integration with an external API or service.
    
    Provides methods to authenticate, manage data, and retrieve information.
    """

    def __init__(self, name: str, user: 'FiscusUser'):
        """
        Initialize a FiscusConnector with the specified name and user context.

        :param name: Name of the connector.
        :param user: Reference to the FiscusUser instance.
        """
        self.name = name
        self.user = user  # Type hint as 'FiscusUser' to avoid circular import
        self.category: Optional[str] = None  # E.g., Email, CRM
        self.authenticated = False
        self.data: Dict[str, Any] = {}
        self.credentials: Dict[str, Any] = {}

        # Initialize audit trail for logging actions
        self.audit_trail = FiscusAuditTrail(
            f'FiscusConnector-{self.name}',
            enable_logging=self.user.client.enable_audit_logging
        )

        # Configure logger based on the user's client logging settings
        self._configure_logging()

        self.logger.info(f"FiscusConnector '{self.name}' initialized successfully.")

    def _configure_logging(self) -> None:
        """
        Configure the logging for the FiscusConnector.
        Sets up the logger with appropriate handlers and formatters based on the client's data.
        """
        logger_name = f'.connector.{self.name}'
        self.logger = logging.getLogger(logger_name)

        # Inherit logging level and handlers from the user's client logger
        self.logger.setLevel(self.user.client.logger.level)

        # Prevent adding multiple handlers if they already exist
        if not self.logger.hasHandlers():
            for handler in self.user.client.logger.handlers:
                self.logger.addHandler(handler)

        self.logger.debug(f"Logging configured for FiscusConnector '{self.name}'.")

    def authenticate(self, auth_params: Dict[str, Any]) -> None:
        """
        Authenticate with the external service.

        :param auth_params: Authentication parameters.
        """
        self.logger.debug(f"Attempting to authenticate with parameters: {self._mask_sensitive_info(auth_params)}")
        try:
            # Implement authentication logic here
            # For example, send auth_params to the external service and verify response
            self.authenticated = True  # Set to True upon successful authentication
            self.logger.info(f"Authentication successful for connector '{self.name}'.")
            self.audit_trail.record('authenticate', {'auth_params': self._mask_sensitive_info(auth_params)})
        except Exception as e:
            self.logger.critical(f"Authentication failed for connector '{self.name}': {e}", exc_info=True)
            self.audit_trail.record('authenticate_failure', {'error': str(e)})
            raise FiscusAuthenticationError(f"Authentication failed for connector '{self.name}'.") from e

    def deauthenticate(self) -> None:
        """
        Deauthenticate from the external service.
        """
        self.logger.debug("Attempting to deauthenticate.")
        try:
            # Implement deauthentication logic here
            self.authenticated = False
            self.logger.info(f"Deauthentication successful for connector '{self.name}'.")
            self.audit_trail.record('deauthenticate', {})
        except Exception as e:
            self.logger.error(f"Deauthentication failed for connector '{self.name}': {e}", exc_info=True)
            self.audit_trail.record('deauthenticate_failure', {'error': str(e)})
            raise e

    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the connector.

        :return: Dictionary containing connector information.
        """
        self.logger.debug("Retrieving connector information.")
        try:
            info = {
                'name': self.name,
                'category': self.category,
                'authenticated': self.authenticated,
                'data': self.data
            }
            self.logger.info(f"Retrieved information for connector '{self.name}'.")
            self.audit_trail.record('get_info', {'info': info})
            return info
        except Exception as e:
            self.logger.error(f"Failed to retrieve information for connector '{self.name}': {e}", exc_info=True)
            self.audit_trail.record('get_info_failure', {'error': str(e)})
            raise e

    def update_data(self, data: Dict[str, Any]) -> None:
        """
        Update connector data.

        :param data: Data options to update.
        """
        self.logger.debug(f"Updating data with options: {self._mask_sensitive_info(data)}")
        try:
            self.data.update(data)
            self.logger.info(f"Data updated successfully for connector '{self.name}'.")
            self.audit_trail.record('update_data', {'config_options': self._mask_sensitive_info(data)})
        except Exception as e:
            self.logger.error(f"Failed to update data for connector '{self.name}': {e}", exc_info=True)
            self.audit_trail.record('update_data_failure', {'error': str(e)})
            raise e

    def _mask_sensitive_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Masks sensitive information in the provided data to prevent exposure in logs.

        :param data: Dictionary containing sensitive information.
        :return: Dictionary with sensitive information masked.
        """
        masked_data = {}
        for key, value in data.items():
            if key.lower() in {'password', 'secret', 'api_key', 'token'}:
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
