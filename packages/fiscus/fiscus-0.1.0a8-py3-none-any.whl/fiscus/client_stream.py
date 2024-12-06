# fiscus_sdk/client_stream.py

import asyncio


class _ClientStreamMixin:
    def stop_stream(self) -> None:
        """
        Stop the WebSocket stream.

        This method stops the WebSocket stream, which is used to maintain a live connection
        with the server for real-time updates. It checks whether the initialization is 
        asynchronous or synchronous and calls the appropriate method to stop the WebSocket
        connection.

        If the stream is no longer needed, calling this method ensures resources are 
        properly released. Users should handle any exceptions that might occur, especially 
        in environments with unreliable network connections.

        Example usage:
        ```python
        client.stop_stream()
        ```

        Logs:
        - Logs information about the stopping process at various stages.
        - Logs any errors encountered during the operation.

        Notes:
        - For asynchronous environments, the method uses `asyncio.run`.
        - For synchronous environments, the method directly calls the synchronous stop method.
        """
        self.logger.info("Stopping WebSocket stream.")
        if self.initialization_async:
            try:
                asyncio.run(self.connection_manager.stop_websocket_connection())
                self.logger.debug("WebSocket connection stopped asynchronously.")
            except Exception as e:
                self.logger.error(f"Failed to stop asynchronous WebSocket connection: {e}", exc_info=True)
        else:
            try:
                self.connection_manager.stop_websocket_connection_sync()
                self.logger.debug("WebSocket connection stopped synchronously.")
            except Exception as e:
                self.logger.error(f"Failed to stop synchronous WebSocket connection: {e}", exc_info=True)
        self.logger.info("WebSocket stream stopped.")

    def restart_stream(self) -> None:
        """
        Restart the WebSocket stream.

        This method restarts the WebSocket stream, allowing users to re-establish a live 
        connection with the server. This is useful in scenarios where the stream might 
        have been interrupted or explicitly stopped and needs to be resumed.

        The method determines whether the initialization is asynchronous or synchronous 
        and calls the corresponding restart method. It requires the `user_id` to ensure 
        the reconnection is tied to the correct user session.

        Example usage:
        ```python
        client.restart_stream()
        ```

        Logs:
        - Logs information about the restart process at various stages.
        - Logs any errors encountered during the operation.

        Notes:
        - Users should handle potential exceptions during the restart process.
        - For asynchronous environments, the method uses `asyncio.run`.
        - For synchronous environments, the method directly calls the synchronous restart method.
        """
        self.logger.info("Restarting WebSocket stream.")
        if self.initialization_async:
            try:
                asyncio.run(
                    self.connection_manager.restart_websocket_connection(self.user_id)
                )
                self.logger.debug("WebSocket connection restarted asynchronously.")
            except Exception as e:
                self.logger.error(f"Failed to restart asynchronous WebSocket connection: {e}", exc_info=True)
        else:
            try:
                self.connection_manager.restart_websocket_connection_sync(self.user_id)
                self.logger.debug("WebSocket connection restarted synchronously.")
            except Exception as e:
                self.logger.error(f"Failed to restart synchronous WebSocket connection: {e}", exc_info=True)
        self.logger.info("WebSocket stream restarted.")
