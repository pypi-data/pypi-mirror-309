# fiscus_sdk/client_configure_logging.py

import logging
from typing import Optional

from .enums import (
	FiscusLogLevel
)

class _ClientConfiguringLoggingMixin:
	def _configure_logging(
			self, level: Optional[FiscusLogLevel], log_to_file: bool, log_file_path: Optional[str]
		) -> None:
			"""
			Configure the logging for the FiscusClient.
			"""
			# Initialize root logger for 'fiscus_sdk'
			logger_name = 'fiscus_sdk'
			self.logger = logging.getLogger(logger_name)

			if level is None:
				# Explicitly disable the logger to prevent any logging activity
				self.logger.disabled = True
				return  # Exit early if logging is not desired

			# If a level is provided, proceed with configuring the logger
			numeric_level = level.to_logging_level()
			self.logger.setLevel(numeric_level)

			# Remove any existing handlers to prevent duplicate logs
			if self.logger.hasHandlers():
				self.logger.handlers.clear()

			# Set up handler
			if log_to_file and log_file_path:
				handler = logging.FileHandler(log_file_path)
				self.logger.debug(f"Logging to file: {log_file_path}")
			else:
				handler = logging.StreamHandler()
				self.logger.debug("Logging to console.")

			handler.setLevel(numeric_level)
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
										datefmt='%Y-%m-%d %H:%M:%S')
			handler.setFormatter(formatter)
			self.logger.addHandler(handler)

			# Set 'websocket' logger level to prevent unwanted logs
			websocket_logger = logging.getLogger('.websocket')
			websocket_logger.setLevel(logging.CRITICAL + 1)
			self.logger.debug("'websocket' module logging level set to CRITICAL+1 to suppress logs.")
