# ai_orchestrator.py

import logging
import json
from typing import TYPE_CHECKING, Optional, Dict, Any, List, Callable
from weakref import WeakSet

from .ai_observer import _AIObserver
from .response import FiscusResponse, FiscusError, FiscusErrorCode
from .user import FiscusUser
from .audit import FiscusAuditTrail
from .llm_adapter import _LLMAdapter
from .llm_config import _LLMConfig
from .callbacks import FiscusCallback
from .enums import (
    FiscusModeType,
    FiscusResponseType,
    FiscusPlanningType,
    FiscusMemoryRetrievalType,
    FiscusMemoryStorageType,
    FiscusLLMType,
    FiscusCallbackType,
    FiscusConnectionType,
    FiscusExecutionType
)

# Import mixin classes
from .ai_orchestrator_logging_config import _AIOrchestratorLoggingConfigMixin
from .ai_orchestrator_callback_utils import _AIOrchestratorCallbackUtilsMixin
from .ai_orchestrator_input_processing import _AIOrchestratorInputProcessingMixin
from .ai_orchestrator_memory_management import _AIOrchestratorMemoryManagementMixin
from .ai_orchestrator_task_execution import _AIOrchestratorTaskExecutionMixin
from .ai_orchestrator_response_generation import _AIOrchestratorResponseGenerationMixin
from .ai_orchestrator_run_methods import _AIOrchestratorRunMethodsMixin

if TYPE_CHECKING:
    from .client import FiscusClient


class _AIOrchestrator(
    _AIOrchestratorLoggingConfigMixin,
    _AIOrchestratorCallbackUtilsMixin,
    _AIOrchestratorInputProcessingMixin,
    _AIOrchestratorMemoryManagementMixin,
    _AIOrchestratorTaskExecutionMixin,
    _AIOrchestratorResponseGenerationMixin,
    _AIOrchestratorRunMethodsMixin,
):
    def __init__(
        self,
        client: 'FiscusClient',
        user: FiscusUser,
        llm: Any,
        llm_type: FiscusLLMType,
        state_id: Optional[str] = None,
        mode: FiscusModeType = FiscusModeType.EXECUTE,
        control_level: FiscusPlanningType = FiscusPlanningType.STREAMLINED,
        memory: Any = None,
        callbacks: Optional[Dict[FiscusCallbackType, FiscusCallback]] = None,
        custom_overrides: Optional[Dict[str, Any]] = None,
        connection_type: Optional[FiscusConnectionType] = None,
        response_format: Optional[FiscusResponseType] = None,
        custom_prompt_template: Optional[str] = None,
        preprocess_function: Optional[Callable[[str], str]] = None,
        postprocess_function: Optional[Callable[[FiscusResponse], Any]] = None,
        custom_options: Optional[Dict[str, Any]] = None,
        execution_mode: FiscusExecutionType = FiscusExecutionType.SEQUENTIAL,
        error_callback: Optional[Callable[[Exception], None]] = None,
        decision_logic_override: Optional[Callable[[str], List[Dict[str, Any]]]] = None,
        memory_retrieval_logic: Optional[Callable[[str], str]] = None,
        memory_storage_logic: Optional[Callable[[Any], None]] = None,
        few_shot_examples: Optional[Dict[str, List[str]]] = None,
        embedding_model: Optional[Any] = None,
        indexing_algorithm: Optional[str] = None,
        retrieval_strategy: FiscusMemoryRetrievalType = FiscusMemoryRetrievalType.SEMANTIC_SEARCH,
        storage_strategy: FiscusMemoryStorageType = FiscusMemoryStorageType.APPEND,
        storage_type: str = 'local',
        is_short_term: bool = True,
        ai_callbacks: Optional[Dict[str, FiscusCallback]] = None,
        debug_mode: bool = False,  # New Parameter
        sandbox_mode: bool = False,  # New Parameter
        optimize: bool = False,       # New Parameter
        fallback_policy: Optional[str] = None,  # New Parameter
        checkpoint_enabled: bool = False        # New Parameter
    ):
        # Initialize mixins
        super().__init__()

        # Initialize core orchestrator attributes
        self.client = client
        self.user = user
        self.llm = llm
        self.llm_type = llm_type
        self.state_id = state_id
        self.mode = mode
        self.control_level = control_level
        self.memory = memory
        self.callbacks = callbacks or {}
        self.custom_overrides = custom_overrides
        self.connection_type = connection_type
        self.response_format = response_format
        self.custom_prompt_template = custom_prompt_template
        self.preprocess_function = preprocess_function
        self.postprocess_function = postprocess_function
        self.custom_options = custom_options or {}
        self.error_callback = error_callback
        self.memory_retrieval_logic = memory_retrieval_logic
        self.memory_storage_logic = memory_storage_logic
        self.few_shot_examples = few_shot_examples or {}
        self.embedding_model = embedding_model
        self.indexing_algorithm = indexing_algorithm or 'hnsw'
        self.retrieval_strategy = retrieval_strategy
        self.storage_strategy = storage_strategy
        self.decision_logic_override = decision_logic_override
        self.execution_mode = execution_mode
        self.storage_type = storage_type
        self.is_short_term = is_short_term
        self.ai_callbacks = ai_callbacks or {}
        self.debug_mode = debug_mode
        self.sandbox_mode = sandbox_mode
        self.optimize = optimize
        self.fallback_policy = fallback_policy
        self.checkpoint_enabled = checkpoint_enabled

        # Set logger name
        logger_name = f".ai_orchestrator.{self.user.user_id}" if self.user and self.user.user_id else ".ai_orchestrator.unknown"
        self.logger = logging.getLogger(logger_name)
        self._configure_logging()

        # Initialize orchestrator class
        self.orchestrator = self.client.orchestrator

        # Initialize _LLMAdapter with parameters
        self.llm_adapter = _LLMAdapter(
            llm=self.llm,
            llm_type=self.llm_type,
            logger=self.logger,
            error_callback=self.error_callback
        )

        # Initialize audit trail for logging actions
        self.audit_trail = FiscusAuditTrail(
            f"AIOrchestrator_{self.user.user_id}",
            enable_logging=self.client.enable_audit_logging,
        )

        # Initialize observers as a WeakSet to prevent memory leaks
        self.observers = WeakSet()
        self.register_observer(_AIObserver(self))

        # Make sure to instantiate the _LLMConfig for LLM usage
        self.llm_config = _LLMConfig()

        # For stateful re-planning
        self.last_input_text = None

    def register_observer(self, observer: _AIObserver):
        """
        Register an observer to receive notifications about events.
        """
        self.observers.add(observer)

    def deregister_observer(self, observer: _AIObserver):
        """
        Deregister an observer to stop receiving notifications.
        """
        self.observers.discard(observer)

    def notify_observer(self, event_type: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Notify the first observer (assuming a single observer pattern) about an event.
        """
        if self.observers:
            return next(iter(self.observers)).update(event_type, data)
        else:
            self.logger.warning("No observer registered to receive events.")
            return None

    def notify_observers(self, event_type: str, data: Optional[Dict[str, Any]] = None) -> List[Optional[Dict[str, Any]]]:
        """
        Notify all registered observers about an event.
        """
        responses = []
        for observer in self.observers:
            response = observer.update(event_type, data)
            responses.append(response)
        return responses

    def cleanup(self):
        """
        Cleanup method to remove observer references and release memory safely.
        """
        # Call the observer's own cleanup method if it exists, to ensure observer-specific cleanup.
        for observer in self.observers:
            if hasattr(observer, 'cleanup'):
                observer.cleanup()
        
        # Clear all observers in the orchestrator
        self.observers.clear()
        self.logger.info("Cleared all observer references for memory management.")
        
    def retrieve_context(self, input_text: str) -> str:
        """
        Retrieve memory context based on input, mode, and configuration.
        """
        return self.retrieve_memory(
            input_text=input_text,
            retrieval_strategy=self.retrieval_strategy,
            state_id=self.state_id,
            storage_type=self.storage_type,
            is_short_term=self.is_short_term,
            context=self.custom_prompt_template,
            **self.custom_options
        )

    def store_context(self, data: Any) -> None:
        """
        Store context in memory based on mode and configuration.
        """
        self.store_memory(
            data=data,
            storage_strategy=self.storage_strategy,
            state_id=self.state_id,
            storage_type=self.storage_type,
            is_short_term=self.is_short_term,
            **self.custom_options
        )

    def run_workflow(self, input_text: str) -> FiscusResponse:
        """
        Main orchestrator method to run the workflow from input processing to final response generation,
        while actively responding to observer-triggered adjustments or replans.
        """
        self.last_input_text = input_text  # Store input text for possible re-planning

        try:
            # Notify observer about planning start
            planning_start_response = self.notify_observers("planning_start", {"input_text": input_text})
            if any(response.get("halt") for response in planning_start_response):
                self.logger.info("Workflow halted by observer at planning start.")
                return FiscusResponse(success=False, error=FiscusError(FiscusErrorCode.HALT_REQUESTED, "Planning halted by observer."))

            # Step 1: Retrieve context if needed
            context = self.retrieve_context(input_text)
            self.logger.debug(f"Context retrieved: {context}")

            # Step 2: Process input and obtain initial tasks
            tasks = self.process_input(input_text)
            if not tasks:
                raise ValueError("No tasks were planned based on the input.")

            # Step 3: Notify observers of planning success and check for updates to tasks or state changes
            planning_responses = self.notify_observers("planning_success", {"tasks": tasks})
            for response in planning_responses:
                # Handle any replan or halt requested by the observer
                if response.get("replan"):
                    self.logger.info("Replanning requested by observer.")
                    tasks = self.process_input(input_text)  # Re-enter flow if replanning requested
                    if not tasks:
                        raise ValueError("No tasks were planned after replan request.")

                if response.get("halt"):
                    self.logger.info("Workflow halted by observer after planning success.")
                    return FiscusResponse(success=False, error=FiscusError(FiscusErrorCode.HALT_REQUESTED, "Workflow halted by observer."))

                # Update tasks if observer provided new ones
                if response and 'updated_tasks' in response:
                    tasks = response['updated_tasks']

            # Step 4: Execute Planned Tasks
            execution_response = self.execute_tasks(tasks)
            if not execution_response.success:
                raise Exception("Task execution failed.")

            # Step 5: Generate Final Response based on successful execution
            final_response = self.generate_final_response(input_text, execution_response.data, FiscusResponseType.TEXT)

            # Notify observers that execution is complete and check if further actions are needed
            execution_complete_responses = self.notify_observers("execution_complete", {"final_response": final_response})
            for response in execution_complete_responses:
                if response.get("replan"):
                    self.logger.info("Replanning requested by observer after execution completion.")
                    return self.run_workflow(input_text)  # Restart the flow if replan is requested post-execution

                if response.get("halt"):
                    self.logger.info("Workflow halted by observer after execution complete.")
                    return FiscusResponse(success=False, error=FiscusError(FiscusErrorCode.HALT_REQUESTED, "Workflow halted by observer."))

            # Step 6: Store context after execution if needed
            self.store_context(final_response)

            # Step 7: Cleanup resources and observers
            self.cleanup()

            # Step 8: Handle Debug Mode - Generate Execution Trace
            if self.debug_mode:
                self.logger.debug("Debug mode enabled. Generating execution trace.")
                execution_trace = self.generate_execution_trace()
                final_response += f"\nExecution Trace:\n{json.dumps(execution_trace, indent=2)}"

            return FiscusResponse(success=True, result=final_response)

        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")
            self.notify_observers("workflow_failure", {"error": str(e)})
            if self.error_callback:
                self.error_callback(e)

            # Clean up on failure to prevent memory leaks
            self.cleanup()

            return FiscusResponse(success=False, error=FiscusError(FiscusErrorCode.EXECUTION_FAILURE, str(e)))

    # Implementing the methods for different modes: run, plan, and run_test
    def run(self, input_text: str, connection_type: Optional[FiscusConnectionType], response_format: Optional[FiscusResponseType], execution_mode: Any):
        """
        Execute the workflow in EXECUTE mode.
        """
        self.mode = FiscusModeType.EXECUTE
        return self.run_workflow(input_text)

    def plan(self, input_text: str, control_level: FiscusPlanningType):
        """
        Plan the workflow without executing it.
        """
        self.mode = FiscusModeType.PLAN
        self.last_input_text = input_text
        try:
            self.notify_observers("planning_start", {"input_text": input_text})
            tasks = self.process_input(input_text)
            # Notify observers that planning was successful
            planning_responses = self.notify_observers("planning_success", {"tasks": tasks})
            # Check if any observer provided updated tasks
            for response in planning_responses:
                if response and 'updated_tasks' in response:
                    tasks = response['updated_tasks']
            return FiscusResponse(success=True, result=tasks)
        except Exception as e:
            self.logger.error(f"Planning failed: {e}")
            self.notify_observers("planning_failure", {"error": str(e)})
            if self.error_callback:
                self.error_callback(e)

            # Clean up on planning failure
            self.cleanup()

            return FiscusResponse(success=False, error=FiscusError(FiscusErrorCode.PLANNING_FAILURE, str(e)))

    def run_test(self, input_text: str, connection_type: Optional[FiscusConnectionType], response_format: Optional[FiscusResponseType]):
        """
        Test the workflow by simulating task execution without actual API calls.
        """
        self.mode = FiscusModeType.TEST
        self.last_input_text = input_text
        try:
            self.notify_observers("testing_start", {"input_text": input_text})
            tasks = self.process_input(input_text)
            # Notify observers that planning was successful
            planning_responses = self.notify_observers("planning_success", {"tasks": tasks})
            # Check if any observer provided updated tasks
            for response in planning_responses:
                if response and 'updated_tasks' in response:
                    tasks = response['updated_tasks']
            # Simulate task execution (you would implement your test logic here)
            if self.sandbox_mode:
                test_results = [{"task": task, "result": "Simulated Test Passed"} for task in tasks]
            else:
                test_results = [{"task": task, "result": "Test passed"} for task in tasks]
            self.notify_observers("testing_success", {"results": test_results})

            # Clean up after test run
            self.cleanup()

            return FiscusResponse(success=True, result=test_results)
        except Exception as e:
            self.logger.error(f"Testing failed: {e}")
            self.notify_observers("testing_failure", {"error": str(e)})
            if self.error_callback:
                self.error_callback(e)

            # Clean up on test failure
            self.cleanup()

            return FiscusResponse(success=False, error=FiscusError(FiscusErrorCode.TESTING_FAILURE, str(e)))

    # Method for re-planning tasks
    def replan(self):
        """
        Method to replan tasks, possibly called by the observer.
        """
        self.logger.info("Replanning tasks.")
        try:
            tasks = self.process_input(self.last_input_text)
            self.notify_observers("replanning_success", {"tasks": tasks})
            return tasks
        except Exception as e:
            self.logger.error(f"Replanning failed: {e}")
            self.notify_observers("replanning_failure", {"error": str(e)})
            return []

    # Method to get a fallback task
    def get_fallback_task(self):
        """
        Method to get a fallback task, possibly called by the observer.
        """
        self.logger.info("Retrieving fallback task.")
        fallback_task = {
            "connector": "default_connector",
            "operation": "default_operation",
            "params": {}
        }
        return fallback_task

    def get_fallback_test(self):
        """
        Method to get a fallback test, possibly called by the observer during testing.
        """
        self.logger.info("Retrieving fallback test.")
        fallback_test = {
            "test_name": "default_test",
            "steps": []
        }
        return fallback_test

    def _ai_evaluate_event(self, ai_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Helper method to use the LLMAdapter for dynamic evaluation of each event.
        """
        prompt = f"""
            You are an AI assistant helping to orchestrate a workflow. An event has occurred during the workflow execution.

            Event Type: {ai_input['event_type']}
            Event Data: {json.dumps(ai_input['data'], indent=2)}
            Current Context: {json.dumps(ai_input.get('context', {}), indent=2)}

            Based on this information, decide the next action. You can choose to:

            - Proceed as normal.
            - Modify the task or data.
            - Skip the task.
            - Halt the workflow.
            - Retry the task.
            - Reconfigure parameters.

            Provide your decision in JSON format without additional text:

            {{
            "next_action": "proceed/modify/skip/halt/retry/reconfigure",
            "override_data": {{}},  # Any data overrides
            "update_context": {{}},  # Any context updates
            "message": ""  # Optional message or reason
            }}
            """
        response = self.llm_adapter.execute(
            action='evaluate_event',
            prompt=prompt,
            response_format=FiscusResponseType.JSON,
            max_tokens=200,
            temperature=0.3,
        )
        if response:
            self.logger.debug(f"AI evaluation response: {response}")
            return response
        else:
            self.logger.warning("AI evaluation did not return a response. Proceeding as normal.")
            return {"next_action": "proceed"}

    def generate_execution_trace(self) -> Dict[str, Any]:
        """
        Generate a detailed execution trace for debugging purposes.
        """
        # This method should collect and return detailed information about the workflow execution.
        # Implementation would depend on how tasks and their states are tracked internally.
        # For illustration, here's a mock implementation:
        trace = {
            "last_input_text": self.last_input_text,
            "state_id": self.state_id,
            "mode": self.mode.value,
            "control_level": self.control_level.value,
            "tasks_executed": [],  # Populate with actual task execution details
            "errors_encountered": [],  # Populate with actual errors
            "execution_time": "N/A",  # Populate with actual execution time
        }
        # Populate trace with actual data
        # Example:
        # for task in self.executed_tasks:
        #     trace["tasks_executed"].append({
        #         "task_id": task.id,
        #         "operation": task.operation,
        #         "status": task.status,
        #         "response": task.response,
        #     })
        return trace

    # Additional methods to handle new features can be implemented here or within mixins
    # For example, handling sandbox_mode, optimize, fallback_policy, checkpoint_enabled
    # These would likely involve modifying methods within the relevant mixins or adding new methods
