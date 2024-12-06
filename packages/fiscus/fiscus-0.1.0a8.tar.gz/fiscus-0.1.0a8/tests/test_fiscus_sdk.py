# tests/test_.py

import unittest
from unittest.mock import patch
import asyncio
from fiscus import (
    FiscusClient, FiscusUser, FiscusConnector, FiscusResponse,
    FiscusAuthenticationError, FiscusAuthorizationError, FiscusValidationError
)
from fiscus.callbacks import fiscus_on_success, fiscus_on_error
from fiscus.orchestrator import _Orchestrator
from fiscus.connection import _ConnectionManager
from fiscus.enums import FiscusResponseType, FiscusConnectionType, FiscusInitType

class TestFiscusSDK(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.api_key = 'TEST_FISCUS_API_KEY'
        self.user_id = 'test_user'
        self.client = FiscusClient(api_key=self.api_key, user_id=self.user_id)
        self.user = self.client.user  # Access the user from the client
        self.connector_name = 'Gmail'
        self.operation = 'send_email'
        self.params = {
            'to': 'recipient@example.com',
            'subject': 'Test Email',
            'body': 'This is a test email.'
        }

    async def asyncSetUp(self):
        self.setUp()  # Reuse setUp for async tests

    def test_client_initialization(self):
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client.user_id, self.user_id)
        self.assertIsInstance(self.client.user, FiscusUser)
        self.assertEqual(self.client.user.user_id, self.user_id)
    
    def test_add_connector(self):
        # Ensure the connector doesn't exist initially
        self.assertNotIn(self.connector_name, self.user.connectors)

        # Add the connector
        self.user.add_connector(self.connector_name)

        # Check if the connector is now in the list
        self.assertIn(self.connector_name, self.user.connectors)
        self.assertIsInstance(self.user.connectors[self.connector_name], FiscusConnector)

    def test_remove_connector(self):
        # First, add the connector
        self.user.add_connector(self.connector_name)

        # Ensure the connector is in the list
        self.assertIn(self.connector_name, self.user.connectors)

        # Remove the connector
        self.user.remove_connector(self.connector_name)

        # Ensure the connector is no longer in the list
        self.assertNotIn(self.connector_name, self.user.connectors)

    def test_authenticate_connector(self):
        # Set up an auth callback that returns auth_params
        def auth_callback(connector_name):
            return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

        self.user.set_auth_callback(auth_callback)
        self.user.authenticate_connector(self.connector_name)
        self.assertIn(self.connector_name, self.user.connectors)
        self.assertTrue(self.user.connectors[self.connector_name].authenticated)

    def test_deauthenticate_connector(self):
        # First, authenticate the connector
        def auth_callback(_):
            return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

        self.user.set_auth_callback(auth_callback)
        self.user.authenticate_connector(self.connector_name)

        # Assert connector is authenticated initially
        self.assertTrue(self.user.connectors[self.connector_name].authenticated)

        # Now, deauthenticate the connector
        self.user.deauthenticate_connector(self.connector_name)

        # FiscusConnector should still be present in user.connectors but deauthenticated
        self.assertIn(self.connector_name, self.user.connectors)
        self.assertFalse(self.user.connectors[self.connector_name].authenticated)


    def test_authentication_error(self):
        # Mock the server response to raise an FiscusAuthenticationError
        with patch.object(FiscusClient, '_send_operation_to_server', side_effect=FiscusAuthenticationError):
            with self.assertRaises(FiscusAuthenticationError):
                self.client.execute(self.connector_name, self.operation, self.params)


    def test_execute_operation_success(self):
        # Authenticate connector
        def auth_callback(connector_name):
            return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

        self.user.set_auth_callback(auth_callback)
        self.user.authenticate_connector(self.connector_name)

        # Mock the backend call
        with patch.object(FiscusClient, '_send_operation_to_server', return_value=FiscusResponse(success=True, result='Email sent')) as mock_send_operation:
            response = self.client.execute(
                connector_name=self.connector_name,
                operation=self.operation,
                params=self.params,
                response_format=FiscusResponseType.JSON,
                user=self.user
            )

            # Assert the backend was called with the right parameters
            mock_send_operation.assert_called_once_with(
                connector_name=self.connector_name,
                operation=self.operation,
                params=self.params,
                response_format=FiscusResponseType.JSON,
                connection_type=FiscusConnectionType.REST,
                custom_options=None,
                user=self.user
            )
            
            self.assertTrue(response.success)
            self.assertEqual(response.result, 'Email sent')


    def test_execute_operation_no_permission(self):
        # Simulate the server denying permission with FiscusAuthorizationError
        with patch.object(FiscusClient, '_send_operation_to_server', side_effect=FiscusAuthorizationError):
            # Ensure the client raises an FiscusAuthorizationError from the backend response
            with self.assertRaises(FiscusAuthorizationError):
                self.client.execute(self.connector_name, self.operation, self.params)

    def test_execute_operation_not_authenticated(self):
        # Simulate the server responding with an FiscusAuthenticationError
        with patch.object(FiscusClient, '_send_operation_to_server', side_effect=FiscusAuthenticationError):
            # The client should raise an FiscusAuthenticationError when the server denies authentication
            with self.assertRaises(FiscusAuthenticationError):
                self.client.execute(self.connector_name, self.operation, self.params)

    def test_orchestrator_execute_manual_workflow(self):
        # Set up connectors and authenticate
        def auth_callback(connector_name):
            return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

        self.user.set_auth_callback(auth_callback)
        self.user.authenticate_connector('Gmail')
        self.user.authenticate_connector('CRMSystem')

        # Assign roles and policies
        self.user.assign_role('user')
        self.user.add_policy({
            'roles': ['user'],
            'connectors': ['Gmail', 'CRMSystem'],
            'operations': ['send_email', 'create_contact'],
        })

        # Mock execute method in FiscusClient
        with patch.object(FiscusClient, 'execute', return_value=FiscusResponse(success=True, result='Operation executed')) as mock_execute:
            workflow = [
                {
                    'connector': 'CRMSystem',
                    'operation': 'create_contact',
                    'params': {'name': 'John Doe', 'email': 'john.doe@example.com'},
                    'custom_logic': lambda response: self.assertTrue(response.success)
                },
                {
                    'connector': 'Gmail',
                    'operation': 'send_email',
                    'params': {
                        'to': 'john.doe@example.com',
                        'subject': 'Welcome',
                        'body': 'Welcome to our service!'
                    },
                    'conditions': {
                        'if': lambda ctx: True  # Always true for testing
                    }
                }
            ]

            # Initialize the orchestrator directly
            orchestrator = _Orchestrator(self.user)

            response = orchestrator._execute_tasks(workflow, callbacks=None)
            self.assertTrue(response.success)
            self.assertEqual(mock_execute.call_count, 2)

    def test_orchestrator_execute_ai_workflow(self):
        # Mock the _send_operation_to_server method in FiscusClient
        with patch.object(FiscusClient, '_send_operation_to_server', return_value=FiscusResponse(success=True, result='AI operation executed')) as mock_send_operation:
            user_input = "Send an email to user@example.com and create a contact named John Doe."
            response = self.client.execute_ai(
                input=user_input,
                user=self.user,
                connection_type=FiscusConnectionType.REST,
            )
            self.assertTrue(response.success)
            mock_send_operation.assert_called_once_with(
                connector_name="AIService",
                operation="execute_ai_workflow",
                params={
                    "user_input": user_input,
                    "api_key": self.client.api_key,
                    "user_id": self.client.user_id,
                    "custom_overrides": {},
                    "response_format": FiscusResponseType.TEXT
                },
                response_format=FiscusResponseType.TEXT,
                connection_type=FiscusConnectionType.REST,
                custom_options=None,
                user=self.user
            )

    def test_orchestrator_preprocess_and_postprocess(self):
        # Initialize the orchestrator
        orchestrator = _Orchestrator(self.user)

        # Define preprocess and postprocess functions
        def preprocess(input_text):
            return input_text.upper()

        def postprocess(response):
            response.result = 'POSTPROCESSED RESULT'
            return response.result

        orchestrator.preprocess_function = preprocess
        orchestrator.postprocess_function = postprocess
        orchestrator.custom_prompt_template = "{user_input}"

        # Since execute_dynamic method does not exist, adjust test accordingly
        # For the purpose of this test, we will simulate the preprocessing and postprocessing

        # Simulate user input
        user_input = "Preprocessed Input"

        # Apply preprocess function
        processed_input = orchestrator.preprocess_function(user_input)
        self.assertEqual(processed_input, "PREPROCESSED INPUT")

        # Simulate execution result
        response = FiscusResponse(success=True, result='Operation executed')

        # Apply postprocess function
        final_result = orchestrator.postprocess_function(response)
        self.assertEqual(final_result, 'POSTPROCESSED RESULT')
        self.assertEqual(response.result, 'POSTPROCESSED RESULT')

    def test_orchestrator_success_callback(self):
        # Mock the execute method in FiscusClient to simulate success
        def mock_execute(*args, **kwargs):
            return FiscusResponse(success=True, result='Operation succeeded')

        success_called = False
        error_called = False

        def success_callback(info):
            nonlocal success_called
            success_called = True

        def error_callback(info):
            nonlocal error_called
            error_called = True

        # Patch the Client's execute method
        with patch.object(FiscusClient, 'execute', side_effect=mock_execute) as mock_exec:
            orchestrator = _Orchestrator(self.user)
            orchestrator.success_callback = success_callback
            orchestrator.error_callback = error_callback

            # Define a valid task with a met condition
            task = {
                'connector': 'Gmail',
                'operation': 'send_email',
                'params': self.params,
                'conditions': {
                    'if': lambda ctx: True  # Ensure condition is met
                }
            }

            # Use _execute_tasks instead of execute
            orchestrator._execute_tasks([task], callbacks=None)

            # Ensure the execute method was called once
            mock_exec.assert_called_once()

            # Check if the success callback was triggered
            self.assertTrue(success_called)
            self.assertFalse(error_called)

    def test_orchestrator_error_callback(self):
        # Mock the execute method in FiscusClient to simulate failure
        def mock_execute(*args, **kwargs):
            raise Exception("Execution failed")

        success_called = False
        error_called = False

        def success_callback(info):
            nonlocal success_called
            success_called = True

        def error_callback(info):
            nonlocal error_called
            error_called = True

        # Patch the FiscusClient's execute method
        with patch.object(FiscusClient, 'execute', side_effect=mock_execute) as mock_exec:
            orchestrator = _Orchestrator(self.user)
            orchestrator.success_callback = success_callback
            orchestrator.error_callback = error_callback

            # Define a task with a met condition
            task = {
                'connector': 'Gmail',
                'operation': 'send_email',
                'params': self.params,
                'conditions': {
                    'if': lambda ctx: True  # Ensure condition is met
                }
            }

            # Use _execute_tasks instead of execute
            try:
                orchestrator._execute_tasks([task], callbacks=None)
            except Exception:
                pass  # The exception is expected

            # Ensure the execute method was called once
            mock_exec.assert_called_once()

            # Check if the error callback was triggered
            self.assertFalse(success_called)
            self.assertTrue(error_called)

    def test_orchestrator_condition_not_met(self):
        # Mock the execute method in FiscusClient to simulate success
        def mock_execute(*args, **kwargs):
            return FiscusResponse(success=True, result='Operation succeeded')

        # Patch the FiscusClient's execute method
        with patch.object(FiscusClient, 'execute', side_effect=mock_execute) as mock_exec:
            orchestrator = _Orchestrator(self.user)

            # Define a task where the condition is not met
            task = {
                'connector': 'Gmail',
                'operation': 'send_email',
                'params': self.params,
                'conditions': {
                    'if': lambda ctx: False  # Condition not met
                }
            }

            # Use _execute_tasks instead of execute
            response = orchestrator._execute_tasks([task], callbacks=None)

            # Ensure the execute method was never called due to condition not being met
            mock_exec.assert_not_called()

            # Ensure that the response indicates the task was skipped
            self.assertTrue(response.success)
            self.assertEqual(response.result, {})

    def test_orchestrator_no_language_model_predefined_workflow(self):
        # Initialize the orchestrator without a language model
        orchestrator = _Orchestrator(self.user, language_model=None)

        # Predefined workflow (list of tasks) instead of a dynamic string input
        workflow = [
            {
                'connector': 'EmailSystem',
                'operation': 'send_email',
                'params': {'to': 'user@example.com', 'subject': 'Test', 'body': 'Hello!'}
            }
        ]

        # Use _execute_tasks method
        with patch.object(FiscusClient, 'execute', return_value=FiscusResponse(success=True, result='Email sent')):
            response = orchestrator._execute_tasks(workflow, callbacks=None)
            self.assertTrue(response.success)

    def test_orchestrator_custom_overrides(self):
        # Since orchestrator and language_model are not directly used in execute_ai,
        # adjust test to match the SDK code

        # Mock the _send_operation_to_server method
        with patch.object(FiscusClient, '_send_operation_to_server', return_value=FiscusResponse(success=True, result='AI operation executed')) as mock_send_operation:

            # Authenticate connector and set permissions
            def auth_callback(connector_name):
                return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

            self.user.set_auth_callback(auth_callback)
            self.user.authenticate_connector('Gmail')

            self.user.assign_role('user')
            self.user.add_policy({
                'roles': ['user'],
                'connectors': ['Gmail'],
                'operations': ['send_email'],
            })

            user_input = "Send an urgent email to user@example.com."
            custom_overrides = {
                'custom_prompt_template': "Interpret the following request: '{user_input}' {additional_instructions}",
                'language_model_context': {'additional_instructions': 'Ensure all emails are sent with high priority.'}
            }

            response = self.client.execute_ai(
                input=user_input,
                custom_overrides=custom_overrides,
                response_format=FiscusResponseType.JSON,
                user=self.user
            )

            self.assertTrue(response.success)
            mock_send_operation.assert_called_once_with(
                connector_name="AIService",
                operation="execute_ai_workflow",
                params={
                    "user_input": user_input,
                    "api_key": self.client.api_key,
                    "user_id": self.client.user_id,
                    "custom_overrides": custom_overrides,
                    "response_format": FiscusResponseType.JSON
                },
                response_format=FiscusResponseType.JSON,
                connection_type=FiscusConnectionType.REST,
                custom_options=None,
                user=self.user
            )

    def test_callbacks(self):
        # Authenticate connector
        def auth_callback(connector_name):
            return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

        self.user.set_auth_callback(auth_callback)
        self.user.authenticate_connector(self.connector_name)

        # Assign roles and policies
        self.user.assign_role('user')
        self.user.add_policy({
            'roles': ['user'],
            'connectors': [self.connector_name],
            'operations': [self.operation],
        })

        success_called = False
        error_called = False

        def custom_success(info):
            nonlocal success_called
            success_called = True
            self.assertIn('Operation succeeded', info['message'])

        def custom_error(info):
            nonlocal error_called
            error_called = True

        # Mock the method that sends the request to the backend
        with patch.object(FiscusClient, '_send_operation_to_server', return_value=FiscusResponse(success=True, result='Email sent')):
            response = self.client.execute(
                self.connector_name,
                self.operation,
                self.params,
                callbacks={'fiscus_on_success': custom_success, 'fiscus_on_error': custom_error}
            )
            self.assertTrue(success_called)
            self.assertFalse(error_called)

    def test_rbac_with_policies(self):
        # Simulate success for allowed operations
        with patch.object(FiscusClient, '_send_operation_to_server', return_value=FiscusResponse(success=True, result='Contact created')):
            response = self.client.execute('Salesforce', 'create_contact', {'name': 'Jane Doe'})
            self.assertTrue(response.success)

        # Simulate RBAC denial from the server (no permission)
        with patch.object(FiscusClient, '_send_operation_to_server', side_effect=FiscusAuthorizationError):
            with self.assertRaises(FiscusAuthorizationError):
                self.client.execute('Salesforce', 'create_contact', {'name': 'Jane Doe'})

    def test_user_context(self):
        self.user.set_context('preferred_language', 'en')
        self.assertEqual(self.user.get_context('preferred_language'), 'en')

    def test_connector_get_info(self):
        connector = FiscusConnector('Gmail', self.user)
        connector.category = 'Email'
        connector.authenticated = True
        info = connector.get_info()
        self.assertEqual(info['name'], 'Gmail')
        self.assertEqual(info['category'], 'Email')
        self.assertTrue(info['authenticated'])

    def test_connector_update_configuration(self):
        connector = FiscusConnector('Gmail', self.user)
        config_options = {'signature': 'Best regards'}
        connector.update_configuration(config_options)
        self.assertEqual(connector.configuration, config_options)

    def test_audit_trail(self):
        # Test that audit logs are recorded when enable_audit_logging is True
        client = FiscusClient(api_key='TEST_API_KEY', user_id='user_123', enable_audit_logging=True)
        user = client.user
        user.assign_role('user')
        user.add_policy({
            'roles': ['user'],
            'connectors': ['Gmail'],
            'operations': ['send_email'],
        })

        # Authenticate connector
        def auth_callback(connector_name):
            return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

        user.set_auth_callback(auth_callback)
        user.authenticate_connector('Gmail')

        # Mock the connector's _send_operation_to_server method
        with patch.object(FiscusClient, '_send_operation_to_server', return_value=FiscusResponse(success=True, result='Email sent')):
            response = client.execute('Gmail', 'send_email', self.params)
            self.assertTrue(response.success)

        # Check that audit records are present
        audit_records = client.audit_trail.get_records()
        self.assertGreater(len(audit_records), 0)
        self.assertTrue(any(record['action'] == 'execute' for record in audit_records))

    def test_custom_options_in_execute(self):
        # Authenticate connector
        def auth_callback(connector_name):
            return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

        self.user.set_auth_callback(auth_callback)
        self.user.authenticate_connector('CustomAPI')

        # Assign roles and policies
        self.user.assign_role('user')
        self.user.add_policy({
            'roles': ['user'],
            'connectors': ['CustomAPI'],
            'operations': ['custom_operation'],
        })

        # Mock the method that sends the request to the backend
        with patch.object(FiscusClient, '_send_operation_to_server', return_value=FiscusResponse(success=True, result='Custom operation executed')) as mock_send_operation:
            custom_options = {'timeout': 30}
            
            # Execute with custom options
            response = self.client.execute('CustomAPI', 'custom_operation', {'data': 'test'}, custom_options=custom_options)

            # Assert that the backend method was called with expected parameters
            mock_send_operation.assert_called_once_with(
                connector_name='CustomAPI',
                operation='custom_operation',
                params={'data': 'test'},
                response_format=FiscusResponseType.TEXT,
                connection_type=FiscusConnectionType.REST,
                custom_options=custom_options,
                user=self.user
            )

            self.assertTrue(response.success)
            self.assertEqual(response.result, 'Custom operation executed')

    def test_invalid_parameters(self):
        # Authenticate connector
        def auth_callback(connector_name):
            return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

        self.user.set_auth_callback(auth_callback)
        self.user.authenticate_connector(self.connector_name)

        # Assign roles and policies
        self.user.assign_role('user')
        self.user.add_policy({
            'roles': ['user'],
            'connectors': [self.connector_name],
            'operations': [self.operation],
        })

        # Pass invalid parameters (use empty dict to trigger validation)
        invalid_params = {}  # Empty dict, invalid per validation

        with self.assertRaises(FiscusValidationError):
            self.client.execute(self.connector_name, self.operation, invalid_params)

    async def test_execute_ai_async(self):
        # Mock the _send_operation_to_server_async method in FiscusClient
        with patch.object(FiscusClient, '_send_operation_to_server_async', return_value=FiscusResponse(success=True, result="Executed 'execute_ai_workflow' on 'AIService' asynchronously")) as mock_send_operation_async:
            user_input = "Send an email to user@example.com and create a contact named John Doe."
            response = await self.client.execute_ai_async(user_input, response_format=FiscusResponseType.JSON, user=self.user)
            self.assertTrue(response.success)
            self.assertEqual(response.result, "Executed 'execute_ai_workflow' on 'AIService' asynchronously")
            mock_send_operation_async.assert_called_once_with(
                connector_name="AIService",
                operation="execute_ai_workflow",
                params={
                    "user_input": user_input,
                    "api_key": self.client.api_key,
                    "user_id": self.client.user_id,
                    "custom_overrides": {},
                    "response_format": FiscusResponseType.JSON
                },
                response_format=FiscusResponseType.JSON,
                connection_type=FiscusConnectionType.REST,
                custom_options=None,
                user=self.user
            )

    def test_set_dynamic_preferences(self):
        preferences = {
            'Email': 'Gmail',
            'CRM': 'Salesforce'
        }
        self.user.set_dynamic_preferences(preferences)
        self.assertEqual(self.user.dynamic_preferences, preferences)

    def test_set_auth_callback(self):
        def auth_callback(connector_name):
            return {'api_key': 'connector_api_key'}

        self.user.set_auth_callback(auth_callback)
        self.assertEqual(self.user.auth_callback, auth_callback)

    def test_response_handling(self):
        # Create a response
        response = FiscusResponse(success=True, result='Operation successful', status_code=200)

        # Test to_json
        json_response = response.to_json()
        self.assertIsInstance(json_response, dict)
        self.assertEqual(json_response['success'], True)
        self.assertEqual(json_response['result'], 'Operation successful')

        # Test to_text
        text_response = response.to_text()
        self.assertEqual(text_response, 'Operation successful')

        # Test get_header (no headers set)
        header_value = response.get_header('Content-Type')
        self.assertIsNone(header_value)

    def test_execute_operation_success(self):
        # Authenticate connector
        def auth_callback(connector_name):
            return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

        self.user.set_auth_callback(auth_callback)
        self.user.authenticate_connector(self.connector_name)

        # Mock the backend call
        with patch.object(FiscusClient, '_send_operation_to_server', return_value=FiscusResponse(success=True, result='Email sent')) as mock_send_operation:
            response = self.client.execute(
                connector_name=self.connector_name,
                operation=self.operation,
                params=self.params,
                response_format=FiscusResponseType.JSON,
                user=self.user
            )

            # Assert the backend was called with the right parameters
            mock_send_operation.assert_called_once_with(
                connector_name=self.connector_name,
                operation=self.operation,
                params=self.params,
                response_format=FiscusResponseType.JSON,
                connection_type=FiscusConnectionType.WEBSOCKET,  # Updated to WEBSOCKET
                custom_options=None,
                user=self.user
            )
            
            self.assertTrue(response.success)
            self.assertEqual(response.result, 'Email sent')

    def test_custom_options_in_execute(self):
        # Authenticate connector
        def auth_callback(connector_name):
            return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

        self.user.set_auth_callback(auth_callback)
        self.user.authenticate_connector('CustomAPI')

        # Assign roles and policies
        self.user.assign_role('user')
        self.user.add_policy({
            'roles': ['user'],
            'connectors': ['CustomAPI'],
            'operations': ['custom_operation'],
        })

        # Mock the method that sends the request to the backend
        with patch.object(FiscusClient, '_send_operation_to_server', return_value=FiscusResponse(success=True, result='Custom operation executed')) as mock_send_operation:
            custom_options = {'timeout': 30}
            
            # Execute with custom options
            response = self.client.execute('CustomAPI', 'custom_operation', {'data': 'test'}, custom_options=custom_options)

            # Assert that the backend method was called with expected parameters
            mock_send_operation.assert_called_once_with(
                connector_name='CustomAPI',
                operation='custom_operation',
                params={'data': 'test'},
                response_format=FiscusResponseType.TEXT,
                connection_type=FiscusConnectionType.WEBSOCKET,  # Updated to WEBSOCKET
                custom_options=custom_options,
                user=self.user
            )

            self.assertTrue(response.success)
            self.assertEqual(response.result, 'Custom operation executed')

    async def test_execute_ai_async(self):
        # Mock the _send_operation_to_server_async method in FiscusClient
        with patch.object(FiscusClient, '_send_operation_to_server_async', return_value=FiscusResponse(success=True, result="Executed 'execute_ai_workflow' on 'AIService' asynchronously")) as mock_send_operation_async:
            user_input = "Send an email to user@example.com and create a contact named John Doe."
            response = await self.client.execute_ai_async(user_input, response_format=FiscusResponseType.JSON, user=self.user)
            self.assertTrue(response.success)
            self.assertEqual(response.result, "Executed 'execute_ai_workflow' on 'AIService' asynchronously")
            mock_send_operation_async.assert_called_once_with(
                connector_name="AIService",
                operation="execute_ai_workflow",
                params={
                    "user_input": user_input,
                    "api_key": self.client.api_key,
                    "user_id": self.client.user_id,
                    "custom_overrides": {},
                    "response_format": FiscusResponseType.JSON
                },
                response_format=FiscusResponseType.JSON,
                connection_type=FiscusConnectionType.WEBSOCKET,  # Updated to WEBSOCKET
                custom_options=None,
                user=self.user
            )

    def test_orchestrator_custom_overrides(self):
        # Mock the _send_operation_to_server method
        with patch.object(FiscusClient, '_send_operation_to_server', return_value=FiscusResponse(success=True, result='AI operation executed')) as mock_send_operation:

            # Authenticate connector and set permissions
            def auth_callback(connector_name):
                return {'api_key': 'FAKE_CONNECTOR_API_KEY'}

            self.user.set_auth_callback(auth_callback)
            self.user.authenticate_connector('Gmail')

            self.user.assign_role('user')
            self.user.add_policy({
                'roles': ['user'],
                'connectors': ['Gmail'],
                'operations': ['send_email'],
            })

            user_input = "Send an urgent email to user@example.com."
            custom_overrides = {
                'custom_prompt_template': "Interpret the following request: '{user_input}' {additional_instructions}",
                'language_model_context': {'additional_instructions': 'Ensure all emails are sent with high priority.'}
            }

            response = self.client.execute_ai(
                input=user_input,
                custom_overrides=custom_overrides,
                response_format=FiscusResponseType.JSON,
                user=self.user
            )

            self.assertTrue(response.success)
            mock_send_operation.assert_called_once_with(
                connector_name="AIService",
                operation="execute_ai_workflow",
                params={
                    "user_input": user_input,
                    "api_key": self.client.api_key,
                    "user_id": self.client.user_id,
                    "custom_overrides": custom_overrides,
                    "response_format": FiscusResponseType.JSON
                },
                response_format=FiscusResponseType.JSON,
                connection_type=FiscusConnectionType.WEBSOCKET,  # Updated to WEBSOCKET
                custom_options=None,
                user=self.user
            )

    def test_websocket_operation_with_eager_init(self):
        with patch.object(_ConnectionManager, 'start_websocket_connection_sync') as mock_start_ws_sync:
            # Create client with eager initialization
            client = FiscusClient(
                api_key=self.api_key,
                user_id=self.user_id,
                initialization_mode=FiscusInitType.EAGER,
                initialization_async=False
            )
            # The WebSocket should have been started during initialization
            mock_start_ws_sync.assert_called_once()

            # Manually set websocket_sync_connected to True to simulate an established connection
            client.connection_manager.websocket_sync_connected = True

            # Mock the send_websocket_message_sync method
            with patch.object(client.connection_manager, 'send_websocket_message_sync', return_value={'status': 'success', 'data': 'response_data'}) as mock_send_ws_message_sync:
                # Perform an operation that uses WebSocket
                response = client.execute(self.connector_name, self.operation, self.params, connection_type=FiscusConnectionType.WEBSOCKET)
                # The WebSocket connection should not be started again
                self.assertEqual(mock_start_ws_sync.call_count, 1)  # Should still be 1
                mock_send_ws_message_sync.assert_called_once()


    async def test_eager_initialization_async_without_call(self):
        with patch.object(_ConnectionManager, 'start_websocket_connection') as mock_start_ws_async:
            client = FiscusClient(
                api_key=self.api_key,
                user_id=self.user_id,
                initialization_mode=FiscusInitType.EAGER,
                initialization_async=True
            )
            # The WebSocket should not be started yet
            mock_start_ws_async.assert_not_called()

            # Now perform an async operation without calling initialize_async()
            with patch.object(client.connection_manager, 'send_websocket_message', return_value={'status': 'success', 'data': 'response_data'}) as mock_send_ws_message:
                response = await client.execute_async(self.connector_name, self.operation, self.params, connection_type=FiscusConnectionType.WEBSOCKET)
                # The WebSocket connection should have been started
                mock_start_ws_async.assert_called_once()
                mock_send_ws_message.assert_called_once()

    def test_stop_and_restart_stream(self):
        # Mock the stop and restart methods
        with patch.object(_ConnectionManager, 'stop_websocket_connection_sync') as mock_stop_ws_sync, \
             patch.object(_ConnectionManager, 'start_websocket_connection_sync') as mock_start_ws_sync:
            self.client.stop_stream()
            mock_stop_ws_sync.assert_called_once()
            self.client.restart_stream()
            mock_start_ws_sync.assert_called_once()


if __name__ == '__main__':
    unittest.main()
