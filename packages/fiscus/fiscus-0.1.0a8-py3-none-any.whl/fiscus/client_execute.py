# fiscus_sdk/client_execute.py

from typing import Optional, Union, Dict, Any, List

from .user import FiscusUser
from .response import FiscusResponse
from .orchestrator import _Orchestrator
from .fiscus_file import FiscusFile
from .utility import _process_files
from .enums import (
    FiscusConnectionType,
    FiscusResponseType,
)
from .callbacks import (
    FiscusCallback
)

class _ClientExecuteMixin:
    def execute(
        self,
        connector_name: Optional[str] = None,
        operation: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        callbacks: Optional[Dict[str, FiscusCallback]] = None,
        custom_options: Optional[Dict[str, Any]] = None,
        tasks: Optional[List[Dict[str, Any]]] = None,
        connection_type: Optional[FiscusConnectionType] = None,
        response_format: Optional[FiscusResponseType] = None,
        user: Optional[FiscusUser] = None,
        files: Optional[List[FiscusFile]] = None
    ) -> FiscusResponse:
        """
        Execute one or more operations synchronously.

        This method provides a way to execute operations (or tasks) using a specified connector 
        and operation type. You can perform single operations or batch execution of tasks. 
        Supports passing parameters, files, and custom callbacks for response handling.

        Parameters:
            connector_name (Optional[str]): The connector name for the operation (e.g., "CRMSystem").
                Required for single operations.
            operation (Optional[str]): The operation to execute within the chosen connector (e.g., "send_email").
                Required for single operations.
            params (Optional[Dict[str, Any]]): A dictionary of parameters for the operation.
            callbacks (Optional[Dict[str, FiscusCallback]]): Optional callbacks for handling various stages
                of the operation, such as success or error.
            custom_options (Optional[Dict[str, Any]]): Additional options for configuring the execution.
            tasks (Optional[List[Dict[str, Any]]]): A list of tasks for batch execution. Each task must define
                its own `connector`, `operation`, and `params`.
            connection_type (Optional[FiscusConnectionType]): The connection type for execution (e.g., "ONLINE").
                Defaults to the client configured connection type.
            response_format (Optional[FiscusResponseType]): The desired response format ("JSON" or "TEXT").
                Defaults to the client configured response format.
            user (Optional[FiscusUser]): The FiscusUser instance performing the operation.
                If not provided, the client default user is used.
            files (Optional[List[FiscusFile]]): A list of files to include with the operation, either as 
                `FiscusFile` objects or file-like dictionaries.

        Returns:
            FiscusResponse: A response object containing execution results, success status, or error details.

        Example (Single Operation):
            ```python
            response = client.execute(
                connector_name="Gmail",
                operation="send_email",
                params={"to": "user@example.com", "subject": "Hello!", "body": "Welcome!"}
            )
            if response.success:
                print("Email sent successfully!")
            else:
                print(f"Error: {response.error_message}")
            ```

        Example (Batch Execution):
            ```python
            tasks = [
                {
                    "connector": "CRMSystem",
                    "operation": "create_contact",
                    "params": {"name": "Jane Doe", "email": "jane.doe@example.com"}
                },
                {
                    "connector": "Gmail",
                    "operation": "send_email",
                    "params": {
                        "to": "jane.doe@example.com",
                        "subject": "Welcome!",
                        "body": "Welcome to our service, Jane!"
                    }
                }
            ]
            response = client.execute(tasks=tasks)
            if response.success:
                print("Tasks executed successfully!")
            else:
                print(f"Error: {response.error_message}")
            ```

        Notes:
        - For batch tasks, each task is executed independently, and aggregated results are returned.
        - Files can be attached to operations via the `files` parameter or included in individual tasks.

        Exceptions:
        - Raises `ValueError` if required parameters are missing or invalid.
        - Logs critical issues when execution fails and raises underlying exceptions.
        """
        self.logger.debug("Executing synchronous operation.")

        if connection_type is None:
            connection_type = self.connection_type
        if response_format is None:
            response_format = self.response_format
        if params is None:
            params = {}

        if not user and not self.user:
            self.logger.error("User instance must be provided for execution.")
            raise ValueError("A FiscusUser instance must be provided.")
        current_user = user or self.user

        if not current_user.user_id:
            self.logger.critical("User instance with a user_id must be provided.")
            raise ValueError("A FiscusUser instance with a user_id must be provided.")

        if not self.orchestrator:
            self.logger.debug("Creating orchestrator.")
            self.orchestrator = _Orchestrator(
                user=current_user, connection_manager=self.connection_manager, client=self
            )
            self.logger.debug("Orchestrator created successfully.")

        # Process files for single operation
        if files:
            try:
                files = _process_files(files)  # This will raise an error if the size limit is exceeded
            except ValueError as e:
                self.logger.error(str(e))
                raise ValueError(str(e))

        if tasks and isinstance(tasks, list):
            self.logger.info("Executing multiple synchronous tasks.")
            responses = []
            for task in tasks:
                # Merge files into each task's params if files are provided in task-specific format
                task_params = task.get("params", {})
                # Process task-specific files
                if "files" in task:
                    task_files = _process_files(task["files"])
                    task["files"] = task_files  # Update task's files with processed files
                response = self.orchestrator._execute_operation(
                    connector_name=task.get("connector"),
                    operation=task.get("operation"),
                    params=task_params,
                    callbacks=task.get("callbacks", callbacks),
                    custom_options=custom_options,
                    connection_type=connection_type,
                    response_format=response_format,
                    user=current_user,
                    files=task.get("files")
                )
                responses.append(response)

                if task.get("callbacks"):
                    self._handle_response(response, task.get("callbacks"))

            return FiscusResponse(success=True, result=responses)

        elif connector_name and operation:
            self.logger.info(f"Executing synchronous operation: Connector='{connector_name}', Operation='{operation}'.")
            response = self.orchestrator._execute_operation(
                connector_name=connector_name,
                operation=operation,
                params=params,
                callbacks=callbacks,
                custom_options=custom_options,
                connection_type=connection_type,
                response_format=response_format,
                user=current_user,
                files=files
            )
            self._handle_response(response, callbacks)
            return response
        else:
            self.logger.error("Invalid parameters provided for execution.")
            raise ValueError("Either 'tasks' or both 'connector_name' and 'operation' must be provided.")

    # Similarly update execute_async to support dict conversion for files
    async def execute_async(
        self,
        connector_name: Optional[str] = None,
        operation: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        callbacks: Optional[Dict[str, FiscusCallback]] = None,
        custom_options: Optional[Dict[str, Any]] = None,
        tasks: Optional[List[Dict[str, Any]]] = None,
        connection_type: Optional[FiscusConnectionType] = None,
        response_format: Optional[FiscusResponseType] = None,
        user: Optional[FiscusUser] = None,
        files: Optional[List[FiscusFile]] = None
    ) -> FiscusResponse:
        """
        Execute one or more operations asynchronously.

        This method allows asynchronous execution of single or batch operations, enabling
        non-blocking workflows in environments where responsiveness is crucial.

        Differences from `execute`:
        - Operations are performed asynchronously.
        - Can be awaited for completion, enabling seamless integration into async workflows.

        Parameters:
            connector_name (Optional[str]): The connector name for the operation (e.g., "CRMSystem").
                Required for single operations.
            operation (Optional[str]): The operation to execute within the chosen connector (e.g., "send_email").
                Required for single operations.
            params (Optional[Dict[str, Any]]): A dictionary of parameters for the operation.
            callbacks (Optional[Dict[str, FiscusCallback]]): Optional callbacks for handling various stages
                of the operation, such as success or error.
            custom_options (Optional[Dict[str, Any]]): Additional options for configuring the execution.
            tasks (Optional[List[Dict[str, Any]]]): A list of tasks for batch execution. Each task must define
                its own `connector`, `operation`, and `params`.
            connection_type (Optional[FiscusConnectionType]): The connection type for execution (e.g., "ONLINE").
                Defaults to the client’s configured connection type.
            response_format (Optional[FiscusResponseType]): The desired response format ("JSON" or "TEXT").
                Defaults to the client’s configured response format.
            user (Optional[FiscusUser]): The FiscusUser instance performing the operation.
                If not provided, the client’s default user is used.
            files (Optional[List[FiscusFile]]): A list of files to include with the operation, either as 
                `FiscusFile` objects or file-like dictionaries.

        Returns:
            FiscusResponse: A response object containing execution results, success status, or error details.

        Example (Async Single Operation):
            ```python
            response = await client.execute_async(
                connector_name="CRMSystem",
                operation="create_contact",
                params={"name": "John Doe", "email": "john.doe@example.com"}
            )
            if response.success:
                print("Contact created successfully!")
            else:
                print(f"Error: {response.error_message}")
            ```

        Example (Async Batch Execution):
            ```python
            tasks = [
                {
                    "connector": "Gmail",
                    "operation": "send_email",
                    "params": {
                        "to": "example@example.com",
                        "subject": "Test Email",
                        "body": "This is a test email."
                    }
                },
                {
                    "connector": "CRMSystem",
                    "operation": "update_contact",
                    "params": {"contact_id": "1234", "status": "active"}
                }
            ]
            response = await client.execute_async(tasks=tasks)
            if response.success:
                print("Batch executed successfully!")
            else:
                print(f"Error: {response.error_message}")
            ```

        Notes:
        - For batch tasks, each task is executed independently, and aggregated results are returned.
        - Files can be attached to operations via the `files` parameter or included in individual tasks.

        Exceptions:
        - Raises `ValueError` if required parameters are missing or invalid.
        - Logs critical issues when execution fails and raises underlying exceptions.
        """
        self.logger.debug("Executing asynchronous operation.")

        if connection_type is None:
            connection_type = self.connection_type
        if response_format is None:
            response_format = self.response_format
        if params is None:
            params = {}

        if not user and not self.user:
            self.logger.error("User instance must be provided for asynchronous execution.")
            raise ValueError("A FiscusUser instance must be provided.")
        current_user = user or self.user

        if not current_user.user_id:
            self.logger.critical("User instance with a user_id must be provided.")
            raise ValueError("A FiscusUser instance with a user_id must be provided.")

        if not self.orchestrator:
            self.logger.debug("Creating orchestrator for asynchronous execution.")
            self.orchestrator = _Orchestrator(
                user=current_user, connection_manager=self.connection_manager, client=self
            )
            self.logger.debug("Orchestrator created successfully.")

        # Process files for single operation
        if files:
            try:
                files = _process_files(files)  # This will raise an error if the size limit is exceeded
            except ValueError as e:
                self.logger.error(str(e))
                raise ValueError(str(e))

        if tasks and isinstance(tasks, list):
            self.logger.info("Executing multiple asynchronous tasks.")
            responses = []
            for task in tasks:
                task_params = task.get("params", {})
                # Process task-specific files
                if "files" in task:
                    task_files = _process_files(task["files"])
                    task["files"] = task_files  # Update task's files with processed files
                response = self.orchestrator._execute_operation(
                    connector_name=task.get("connector"),
                    operation=task.get("operation"),
                    params=task_params,
                    callbacks=task.get("callbacks", callbacks),
                    custom_options=custom_options,
                    connection_type=connection_type,
                    response_format=response_format,
                    user=current_user,
                    files=task.get("files")
                )
                responses.append(response)

                # Handle task-specific callbacks if provided
                if task.get("callbacks"):
                    self._handle_response(response, task.get("callbacks"))

            # Return aggregated results as a single FiscusResponse
            return FiscusResponse(success=True, result=responses)

        elif connector_name and operation:
            self.logger.info(f"Executing asynchronous operation: Connector='{connector_name}', Operation='{operation}'.")
            # Execute a single operation asynchronously and handle responses
            response = await self.orchestrator._execute_operation_async(
                connector_name=connector_name,
                operation=operation,
                params=params,
                callbacks=callbacks,
                custom_options=custom_options,
                connection_type=connection_type,
                response_format=response_format,
                user=current_user,
                files=files
            )
            self._handle_response(response, callbacks)
            return response
        else:
            self.logger.error("Invalid parameters provided for asynchronous execution.")
            raise ValueError("Either 'tasks' or both 'connector_name' and 'operation' must be provided.")
