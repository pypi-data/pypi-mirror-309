# logging_config.py

class _AIOrchestratorLoggingConfigMixin:
    def _configure_logging(self) -> None:
        """
        Configure the logging for the AIOrchestrator.

        Sets up the logger with appropriate handlers and formatters based on the client's configuration.
        Ensures that logs are consistent with other SDK components.
        """
        # Inherit logging level and handlers from the client's logger
        self.logger.setLevel(self.client.logger.level)

        # Prevent adding multiple handlers if they already exist
        if not self.logger.hasHandlers():
            for handler in self.client.logger.handlers:
                self.logger.addHandler(handler)

        self.logger.debug("Logging configured for AIOrchestrator.")
