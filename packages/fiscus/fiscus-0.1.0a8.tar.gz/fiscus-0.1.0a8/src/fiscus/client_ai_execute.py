# fiscus_sdk/client_ai_execute.py

from typing import Optional, Dict, Any, Callable, List

from .utility import _mask_sensitive_info
from .user import FiscusUser
from .response import FiscusResponse
# from .ai_orchestrator import _AIOrchestrator
from .enums import (
	FiscusConnectionType,
	FiscusResponseType,
	FiscusExecutionType,
	FiscusMemoryRetrievalType,
	FiscusMemoryStorageType,
	FiscusLLMType,
	FiscusCallbackType,
	FiscusModeType,
	FiscusPlanningType
)
from .callbacks import (
	FiscusCallback
)

class _ClientAIExecuteMixin:
    def ai_execute(
        self,
        *args, 
        **kwargs
    ) -> None:
        """
        Temporary Method Notice:
        The `ai_execute` function is not available at the moment. 
        It is undergoing development and will be released in an alpha version within the next 7 days. 
        Stay tuned for updates!
        """
        print("The `ai_execute` function is not available yet. Its alpha release will be coming in the next 7 days. Stay tuned for updates!")

	# def ai_execute(
	# 	self,
	# 	input: str,
	# 	llm_type: FiscusLLMType,
	# 	llm: Any,
	# 	state_id: Optional[str] = None,
	# 	mode: FiscusModeType = FiscusModeType.EXECUTE,
	# 	control_level: FiscusPlanningType = FiscusPlanningType.STREAMLINED,
	# 	memory: Any = None,
	# 	callbacks: Optional[Dict[FiscusCallbackType, FiscusCallback]] = None,
	# 	custom_overrides: Optional[Dict[str, Any]] = None,
	# 	connection_type: Optional[FiscusConnectionType] = None,
	# 	response_format: Optional[FiscusResponseType] = None,
	# 	user: Optional[FiscusUser] = None,
	# 	custom_prompt_template: Optional[str] = None,
	# 	preprocess_function: Optional[Callable[[str], str]] = None,
	# 	postprocess_function: Optional[Callable[[FiscusResponse], Any]] = None,
	# 	custom_options: Optional[Dict[str, Any]] = None,
	# 	execution_mode: FiscusExecutionType = FiscusExecutionType.SEQUENTIAL,
	# 	error_callback: Optional[Callable[[Exception], None]] = None,
	# 	decision_logic_override: Optional[Callable[[str], List[Dict[str, Any]]]] = None,
	# 	memory_retrieval_logic: Optional[Callable[[str], str]] = None,
	# 	memory_storage_logic: Optional[Callable[[Any], None]] = None,
	# 	few_shot_examples: Optional[Dict[str, List[str]]] = None,
	# 	embedding_model: Optional[Any] = None,
	# 	indexing_algorithm: Optional[str] = None,
	# 	retrieval_strategy: FiscusMemoryRetrievalType = FiscusMemoryRetrievalType.SEMANTIC_SEARCH,
	# 	storage_strategy: FiscusMemoryStorageType = FiscusMemoryStorageType.APPEND,
	# 	storage_type: str = 'local',
	# 	is_short_term: bool = True,
	# 	debug_mode: bool = False,
	# 	sandbox_mode: bool = False,
	# 	optimize: bool = False,
	# 	fallback_policy: Optional[str] = None,
	# 	checkpoint_enabled: bool = False
	# ) -> FiscusResponse:
	# 	"""
    #     Execute an AI-driven workflow synchronously.

	# 	This method uses advanced NLP to create agentic workflows, transforming user input into 
	# 	actionable tasks. Acting as an AI Integration Engineer, it enables seamless API integration 
	# 	and dynamic task orchestration within a single tool. 

	# 	With built-in memory, custom logic, and adaptability, it eliminates the need for multiple tools, 
	# 	empowering developers to deploy AI-driven agents that handle any integration efficiently.

    #     Parameters:
    #     - `input` (str): The user-provided input to initialize the AI workflow.
    #     - `llm_type` (FiscusLLMType): The type of large language model (LLM) to use. Supported
    #       types include OpenAI, Anthropic, Gemini, and others.
    #     - `llm` (Any): The LLM instance to process the input.
    #     - `state_id` (Optional[str]): An identifier for stateful workflows. Use this to maintain
    #       continuity across sessions. Defaults to `None`.
    #     - `mode` (FiscusModeType): Specifies the execution mode (`EXECUTE`, `PLAN`, or `TEST`).
    #       Defaults to `EXECUTE`.
    #     - `control_level` (FiscusPlanningType): Defines the level of control in task planning,
    #       such as `STREAMLINED` for simpler flows or `FULL_CONTROL` for advanced workflows.
    #       Defaults to `STREAMLINED`.
    #     - `memory` (Any): Memory object for managing context and state across executions.
    #       Defaults to `None`.
    #     - `callbacks` (Optional[Dict[FiscusCallbackType, FiscusCallback]]): Callback functions
    #       to handle workflow events such as success, error, or task-specific responses.
    #       Defaults to `None`.
    #     - `custom_overrides` (Optional[Dict[str, Any]]): A dictionary of custom overrides to
    #       adjust behavior at specific stages of execution. Defaults to `None`.
    #     - `connection_type` (Optional[FiscusConnectionType]): Specifies the connection type
    #       (`ONLINE` or `OFFLINE`). Defaults to the client's configuration.
    #     - `response_format` (Optional[FiscusResponseType]): The desired response format (`TEXT`
    #       or `JSON`). Defaults to the client's configuration.
    #     - `user` (Optional[FiscusUser]): The `FiscusUser` instance associated with the workflow.
    #       Required if no user is already set in the client. Defaults to `None`.
    #     - `custom_prompt_template` (Optional[str]): A custom template for prompting the LLM.
    #       Defaults to `None`.
    #     - `preprocess_function` (Optional[Callable[[str], str]]): A function to preprocess the
    #       input before sending it to the LLM. Defaults to `None`.
    #     - `postprocess_function` (Optional[Callable[[FiscusResponse], Any]]): A function to
    #       postprocess the AI-generated response. Defaults to `None`.
    #     - `custom_options` (Optional[Dict[str, Any]]): Additional options for fine-tuning the
    #       workflow. Defaults to `None`.
    #     - `execution_mode` (FiscusExecutionType): Specifies the execution flow (`SEQUENTIAL`
    #       or `PARALLEL`). Defaults to `SEQUENTIAL`.
    #     - `error_callback` (Optional[Callable[[Exception], None]]): A function to handle errors
    #       encountered during execution. Defaults to `None`.
    #     - `decision_logic_override` (Optional[Callable[[str], List[Dict[str, Any]]]]): A custom
    #       function to override decision-making logic during execution. Defaults to `None`.
    #     - `memory_retrieval_logic` (Optional[Callable[[str], str]]): Custom logic for retrieving
    #       memory data. Defaults to `None`.
    #     - `memory_storage_logic` (Optional[Callable[[Any], None]]): Custom logic for storing
    #       memory data. Defaults to `None`.
    #     - `few_shot_examples` (Optional[Dict[str, List[str]]]): Few-shot examples to guide the
    #       LLM's responses. Defaults to `None`.
    #     - `embedding_model` (Optional[Any]): Custom embedding model for memory operations.
    #       Defaults to `None`.
    #     - `indexing_algorithm` (Optional[str]): Indexing algorithm for organizing memory.
    #       Defaults to `None`.
    #     - `retrieval_strategy` (FiscusMemoryRetrievalType): Strategy for retrieving memory,
    #       such as `SEMANTIC_SEARCH`. Defaults to `SEMANTIC_SEARCH`.
    #     - `storage_strategy` (FiscusMemoryStorageType): Strategy for storing memory, such as
    #       `APPEND` or `UPDATE`. Defaults to `APPEND`.
    #     - `storage_type` (str): Type of storage for memory (e.g., `local`, `pickle`). Defaults to `local`.
    #     - `is_short_term` (bool): Indicates if memory is short-term. Defaults to `True`.
    #     - `debug_mode` (bool): Enables detailed logs for tracing workflow execution. Defaults to `False`.
    #     - `sandbox_mode` (bool): Simulates the workflow without making actual API calls. Defaults to `False`.
    #     - `optimize` (bool): Enables real-time adjustments for optimized execution. Defaults to `False`.
    #     - `fallback_policy` (Optional[str]): Specifies how to handle failures (e.g., retry,
    #       skip, replan). Defaults to `None`.
    #     - `checkpoint_enabled` (bool): Saves checkpoints during execution to resume workflows
    #       after interruptions. Defaults to `False`.

    #     Returns:
    #     - `FiscusResponse`: Contains the result of the execution, including success status,
    #       output data, and error details (if applicable).

    #     Example:
    #     ```python
    #     response = client.ai_execute(
    #         input="Generate a project plan for developing a new app.",
    #         llm_type=FiscusLLMType.OPENAI,
    #         llm=openai_llm_instance,
    #         user=FiscusUser(user_id="user_123"),
    #         callbacks={
    #             FiscusCallbackType.ON_SUCCESS: lambda r: print("Success!", r),
    #             FiscusCallbackType.ON_ERROR: lambda e: print("Error occurred:", e)
    #         },
    #         execution_mode=FiscusExecutionType.SEQUENTIAL
    #     )
    #     if response.success:
    #         print("Workflow completed:", response.result)
    #     else:
    #         print("Workflow failed:", response.error_message)
    #     ```

    #     Notes:
    #     - The `llm` and `llm_type` parameters are mandatory.
    #     - For stateful workflows, ensure `state_id` and memory configurations are set.
    #     - Use `custom_prompt_template` to tailor LLM prompts for specific tasks.
    #     - For debugging, enable `debug_mode` to capture detailed logs.

    #     Logs:
    #     - Provides comprehensive logs during execution for tracing and debugging.
    #     """
	# 	self.logger.info("Starting synchronous AI execution.")
	# 	self.logger.debug(f"Input: {input}")
	# 	self.logger.debug(f"LLM Type: {llm_type}")
	# 	self.logger.debug(f"Execution mode: {mode}")
	# 	self.logger.debug(f"Control level: {control_level}")
	# 	self.logger.debug(f"Debug mode: {debug_mode}")
	# 	self.logger.debug(f"Sandbox mode: {sandbox_mode}")
	# 	self.logger.debug(f"Optimization enabled: {optimize}")
	# 	self.logger.debug(f"Fallback policy: {fallback_policy}")
	# 	self.logger.debug(f"Checkpoint enabled: {checkpoint_enabled}")

	# 	if connection_type is None:
	# 		connection_type = self.connection_type
	# 	if response_format is None:
	# 		response_format = self.response_format

	# 	# We need the user to proceed
	# 	if not (user or self.user) or not (user or self.user).user_id:
	# 		self.logger.error("A FiscusUser instance with a user_id must be provided for AI execution.")
	# 		raise ValueError("A FiscusUser instance with a user_id must be provided.")
	# 	current_user = user or self.user

	# 	# We need the llm and its type to proceed
	# 	if not llm or not llm_type:
	# 		self.logger.error("Both 'llm' and 'llm_type' must be provided for AI execution.")
	# 		raise ValueError("Both 'llm' and 'llm_type' are required parameters.")

	# 	if memory is None:
	# 		memory = self.memory

	# 	# Initialize ai_callbacks using FiscusCallbackType enums
	# 	ai_callbacks = {
	# 		callback_type.value: callbacks.get(callback_type, globals().get(callback_type.name)) 
	# 		if callbacks else globals().get(callback_type.name)
	# 		for callback_type in FiscusCallbackType
	# 		if "AI" in callback_type.name
	# 	}

	# 	# Initialize AIOrchestrator with AI-specific callbacks and new parameters
	# 	ai_orchestrator = _AIOrchestrator(
	# 		client=self,
	# 		user=current_user,
	# 		llm=llm,
	# 		llm_type=llm_type,
	# 		state_id=state_id,
	# 		control_level=control_level,
	# 		mode=mode,
	# 		memory=memory,
	# 		callbacks=callbacks,
	# 		custom_overrides=custom_overrides,
	# 		connection_type=connection_type,
	# 		response_format=response_format,
	# 		custom_prompt_template=custom_prompt_template,
	# 		preprocess_function=preprocess_function,
	# 		postprocess_function=postprocess_function,
	# 		custom_options=custom_options,
	# 		error_callback=error_callback,
	# 		decision_logic_override=decision_logic_override,
	# 		memory_retrieval_logic=memory_retrieval_logic,
	# 		memory_storage_logic=memory_storage_logic,
	# 		few_shot_examples=few_shot_examples,
	# 		embedding_model=embedding_model,
	# 		indexing_algorithm=indexing_algorithm,
	# 		retrieval_strategy=retrieval_strategy,
	# 		storage_strategy=storage_strategy,
	# 		storage_type=storage_type,
	# 		is_short_term=is_short_term,
	# 		ai_callbacks=ai_callbacks,
	# 		debug_mode=debug_mode,
	# 		sandbox_mode=sandbox_mode,
	# 		optimize=optimize,
	# 		fallback_policy=fallback_policy,
	# 		checkpoint_enabled=checkpoint_enabled,
	# 	)

	# 	# Run AIOrchestrator in selected mode
	# 	self.logger.info(f"Running AIOrchestrator in {mode} mode.")
	# 	if mode == "PLANNING":
	# 		response = ai_orchestrator.plan(input_text=input, control_level=control_level)
	# 	elif mode == "TEST":
	# 		response = ai_orchestrator.run_test(input_text=input, connection_type=connection_type, response_format=response_format)
	# 	else:  # Default to EXECUTE
	# 		response = ai_orchestrator.run(
	# 			input_text=input,
	# 			connection_type=connection_type,
	# 			response_format=response_format,
	# 			execution_mode=execution_mode
	# 		)

	# 	# Debug mode: Return detailed execution trace
	# 	if debug_mode:
	# 		self.logger.debug("Debug mode enabled. Generating execution trace.")
	# 		response.trace = ai_orchestrator.generate_execution_trace()

	# 	if response.success:
	# 		self.logger.info(f"AIOrchestrator {mode} completed successfully.")
	# 	else:
	# 		self.logger.error(f"AIOrchestrator {mode} failed with error: {response.error}")

	# 	self.logger.debug(f"Response from AIOrchestrator: {_mask_sensitive_info(response.data)}")

	# 	# Save user context if context_saver is configured
	# 	if self.context_saver:
	# 		try:
	# 			self.context_saver(current_user.context)
	# 			self.logger.debug("User context saved successfully after AI execution.")
	# 		except Exception as e:
	# 			self.logger.error(f"Failed to save user context after AI execution: {e}", exc_info=True)

	# 	# Final response
	# 	return response
