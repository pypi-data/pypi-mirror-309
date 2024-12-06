# task_execution.py

import asyncio
import time
import json
from typing import Dict, Any, List, Optional
from .enums import FiscusExecutionType, FiscusConnectionType, FiscusResponseType
from .response import FiscusResponse, FiscusError, FiscusErrorCode
from .utility import _mask_sensitive_info
from .callbacks import FiscusCallback

from .category_few_shot import category_few_shot_examples
from .connector_few_shot import connector_few_shot_examples
from .operation_few_shot import operation_few_shot_examples
from .task_few_shot import task_few_shot_examples

class _AIOrchestratorTaskExecutionMixin:
	def __init__(self):
		self.observers = []

	def register_observer(self, observer):
		self.observers.append(observer)

	def notify_observers(self, event: str, data: Dict[str, Any]):
		for observer in self.observers:
			observer.update(event, data)
		
	def _load_categories_few_shot(self) -> List[Dict[str, Any]]:
		"""
		Load the categories few shot examples from categories_few_shot.py.
		"""
		return category_few_shot_examples

	def _load_connectors_few_shot(self) -> List[Dict[str, Any]]:
		"""
		Load the connectors few shot examples from connectors_few_shot.py.
		"""
		return connector_few_shot_examples

	def _load_operations_few_shot(self) -> List[Dict[str, Any]]:
		"""
		Load the operations few shot examples from operations_few_shot.py.
		"""
		return operation_few_shot_examples

	def _load_tasks_few_shot(self) -> List[Dict[str, Any]]:
		"""
		Load the tasks few shot examples from tasks_few_shot.py.
		"""
		return task_few_shot_examples

	def execute_tasks(
		self,
		tasks: List[Dict[str, Any]],
		callbacks: Optional[Dict[str, FiscusCallback]] = None,
		connection_type: Optional[FiscusConnectionType] = None,
		response_format: Optional[FiscusResponseType] = None,
		execution_mode: FiscusExecutionType = FiscusExecutionType.SEQUENTIAL,
	) -> FiscusResponse:
		"""
		Execute the tasks, possibly sequentially or in parallel.
		"""
		responses = []
		self.logger.debug(f"Executing tasks with execution_mode={execution_mode}")

		# Context to pass between tasks
		context = {}

		if execution_mode == FiscusExecutionType.SEQUENTIAL:
			for task in tasks:
				self.notify_observers('task_start', {'task': task})
				self.logger.debug(f"Executing task: {_mask_sensitive_info(task)}")

				# Pre-execution hook
				if 'pre_execution_hook' in task and callable(task['pre_execution_hook']):
					self.logger.debug("Executing pre-execution hook for task.")
					task = task['pre_execution_hook'](task)

				# Handle conditional logic
				if task.get('conditional_logic') not in [None, '', 'none', 'null', False, 0]:
					condition_result = self.evaluate_conditional_logic(task['conditional_logic'], context)
					if not condition_result:
						self.logger.debug(f"Skipping task due to conditional logic result: {condition_result}")
						self.notify_observers('task_skipped', {'task': task, 'reason': 'conditional_logic_failed'})
						continue  # Skip this task
					else:
						self.logger.debug(f"Conditional logic evaluated to: {condition_result}")

				response = self.orchestrator._execute_operation(
					connector_name=task['connector'],
					operation=task['operation'],
					params=task.get('params', {}),
					callbacks=task.get('callbacks', callbacks),
					custom_options=task.get('custom_options', self.custom_options),
					connection_type=connection_type,
					response_format=response_format,
					user=self.user,
				)

				# Add logging here to inspect the response
				self.logger.debug(f"Received response: {response}")
				self.logger.debug(f"Response success: {response.success}")
				self.logger.debug(f"Response data: {_mask_sensitive_info(response.data)}")
				responses.append(response)

				# Notify observers of task completion or failure
				if response.success:
					self.notify_observers('task_success', {'task': task, 'response': response})
				else:
					self.notify_observers('task_failure', {'task': task, 'response': response})

				# Update context with the response
				if response.success and response.data:
					if isinstance(response.data, dict):
						context.update(response.data)
					else:
						context['last_result'] = response.data

				# Post-execution hook
				if 'post_execution_hook' in task and callable(task['post_execution_hook']):
					self.logger.debug("Executing post-execution hook for task.")
					response = task['post_execution_hook'](response)

				# Error handling and retry logic
				if not response.success:
					retry_attempts = task.get('retry_attempts', 0)
					max_retries = task.get('max_retries', self.client.retries)
					while not response.success and retry_attempts < max_retries:
						retry_attempts += 1
						sleep_time = self.client.backoff_factor * (2 ** retry_attempts)
						self.logger.warning(f"Retrying task '{task['operation']}' after {sleep_time} seconds (Attempt {retry_attempts}).")
						time.sleep(sleep_time)
						response = self.orchestrator._execute_operation(
							connector_name=task['connector'],
							operation=task['operation'],
							params=task.get('params', {}),
							callbacks=task.get('callbacks', callbacks),
							custom_options=task.get('custom_options', self.custom_options),
							connection_type=connection_type,
							response_format=response_format,
							user=self.user,
						)
						responses.append(response)
						if response.success:
							self.notify_observers('retry_success', {'task': task, 'retry_attempt': retry_attempts})
					if not response.success:
						# Fallback mechanism
						fallback_task = task.get('fallback_task')
						if fallback_task:
							self.logger.warning(f"Executing fallback task for '{task['operation']}'.")
							response = self.orchestrator._execute_operation(
								connector_name=fallback_task['connector'],
								operation=fallback_task['operation'],
								params=fallback_task.get('params', {}),
								callbacks=fallback_task.get('callbacks', callbacks),
								custom_options=fallback_task.get('custom_options', self.custom_options),
								connection_type=connection_type,
								response_format=response_format,
								user=self.user,
							)
							responses.append(response)
							self.notify_observers('fallback_task_executed', {'task': fallback_task, 'original_task': task})
						else:
							if self.error_callback:
								self.logger.error(f"Task '{task['operation']}' failed after retries. Invoking error callback.")
								self.error_callback(Exception(f"Task '{task['operation']}' failed after retries."))
							else:
								self.logger.fatal(f"Task '{task['operation']}' failed after retries with no error callback.")
							break  # Stop execution if no fallback is provided
					else:
						self.logger.info(f"Task '{task['operation']}' succeeded after retries.")

				else:
					# Store memory if necessary
					if self.memory and ('store_memory' not in task or task['store_memory']):
						self.logger.debug("Storing response data into memory.")
						self.store_memory(response.data)

		elif execution_mode == FiscusExecutionType.PARALLEL:
			self.logger.debug("Executing tasks in parallel.")
			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)
			tasks_coroutines = [
				self._execute_task_async(
					task=task,
					callbacks=callbacks,
					connection_type=connection_type,
					response_format=response_format,
					context=context,
				)
				for task in tasks
			]
			responses = loop.run_until_complete(asyncio.gather(*tasks_coroutines))
			loop.close()
		else:
			self.logger.error("Invalid execution_mode specified.")
			raise ValueError("Invalid execution_mode. Must be FiscusExecutionType.SEQUENTIAL or FiscusExecutionType.PARALLEL.")

		self.logger.debug(f"All responses collected: {responses}")
		return FiscusResponse(success=True, result=responses)

	async def _execute_task_async(
		self,
		task: Dict[str, Any],
		callbacks: Optional[Dict[str, FiscusCallback]] = None,
		connection_type: Optional[FiscusConnectionType] = None,
		response_format: Optional[FiscusResponseType] = None,
		context: Dict[str, Any] = None,
	) -> FiscusResponse:
		"""
		Helper function to execute a single task asynchronously.
		"""
		context = context or {}
		self.notify_observers('task_start', {'task': task})
		self.logger.debug(f"Starting async execution of task: {_mask_sensitive_info(task)}")

		# Pre-execution hook
		if 'pre_execution_hook' in task and callable(task['pre_execution_hook']):
			self.logger.debug("Executing pre-execution hook for task.")
			task = task['pre_execution_hook'](task)

		# Handle conditional logic
		if task.get('conditional_logic') not in [None, '', 'none', 'null', False, 0]:
			condition_result = self.evaluate_conditional_logic(task['conditional_logic'], context)
			if not condition_result:
				self.logger.debug(f"Skipping task due to conditional logic result: {condition_result}")
				self.notify_observers('task_skipped', {'task': task, 'reason': 'conditional_logic_failed'})
				return FiscusResponse(success=True, result="Task skipped due to conditional logic.")
			else:
				self.logger.debug(f"Conditional logic evaluated to: {condition_result}")

		response = await self.orchestrator._execute_operation_async(
			connector_name=task['connector'],
			operation=task['operation'],
			params=task.get('params', {}),
			callbacks=task.get('callbacks', callbacks),
			custom_options=task.get('custom_options', self.custom_options),
			connection_type=connection_type,
			response_format=response_format,
			user=self.user,
		)

		# Add logging here to inspect the response
		self.logger.debug(f"Received response: {response}")
		self.logger.debug(f"Response success: {response.success}")
		self.logger.debug(f"Response data: {_mask_sensitive_info(response.data)}")

		# Update context with the response
		if response.success and response.data:
			if isinstance(response.data, dict):
				context.update(response.data)
			else:
				context['last_result'] = response.data

		# Notify observers of task completion or failure
		if response.success:
			self.notify_observers('task_success', {'task': task, 'response': response})
		else:
			self.notify_observers('task_failure', {'task': task, 'response': response})

		# Post-execution hook
		if 'post_execution_hook' in task and callable(task['post_execution_hook']):
			self.logger.debug("Executing post-execution hook for task.")
			response = task['post_execution_hook'](response)

		# Retry logic (if async)
		if not response.success:
			retry_attempts = task.get('retry_attempts', 0)
			max_retries = task.get('max_retries', self.client.retries)
			while not response.success and retry_attempts < max_retries:
				retry_attempts += 1
				sleep_time = self.client.backoff_factor * (2 ** retry_attempts)
				self.logger.warning(f"Retrying task '{task['operation']}' after {sleep_time} seconds (Attempt {retry_attempts}).")
				await asyncio.sleep(sleep_time)
				response = await self.orchestrator._execute_operation_async(
					connector_name=task['connector'],
					operation=task['operation'],
					params=task.get('params', {}),
					callbacks=task.get('callbacks', callbacks),
					custom_options=task.get('custom_options', self.custom_options),
					connection_type=connection_type,
					response_format=response_format,
					user=self.user,
				)
				if response.success:
					self.notify_observers('retry_success', {'task': task, 'retry_attempt': retry_attempts})
		if not response.success:
			fallback_task = task.get('fallback_task')
			if fallback_task:
				self.logger.warning(f"Executing fallback task for '{task['operation']}'.")
				response = await self.orchestrator._execute_operation_async(
					connector_name=fallback_task['connector'],
					operation=fallback_task['operation'],
					params=fallback_task.get('params', {}),
					callbacks=fallback_task.get('callbacks', callbacks),
					custom_options=fallback_task.get('custom_options', self.custom_options),
					connection_type=connection_type,
					response_format=response_format,
					user=self.user,
				)
				self.notify_observers('fallback_task_executed', {'task': fallback_task, 'original_task': task})
			else:
				if self.error_callback:
					self.logger.error(f"Task '{task['operation']}' failed after retries. Invoking error callback.")
					self.error_callback(Exception(f"Task '{task['operation']}' failed after retries."))
				else:
					self.logger.fatal(f"Task '{task['operation']}' failed after retries with no error callback.")
		else:
			# Store memory if necessary
			if self.memory and ('store_memory' not in task or task['store_memory']):
				self.logger.debug("Storing response data into memory.")
				self.store_memory(response.data)

		return response

	async def execute_tasks_async(
		self,
		tasks: List[Dict[str, Any]],
		callbacks: Optional[Dict[str, FiscusCallback]] = None,
		connection_type: Optional[FiscusConnectionType] = None,
		response_format: Optional[FiscusResponseType] = None,
		execution_mode: FiscusExecutionType = FiscusExecutionType.SEQUENTIAL,
	) -> FiscusResponse:
		"""
		Execute the tasks asynchronously.
		"""
		responses = []
		self.logger.debug(f"Executing tasks asynchronously with execution_mode={execution_mode}")

		# Context to pass between tasks
		context = {}

		if execution_mode == FiscusExecutionType.SEQUENTIAL:
			for task in tasks:
				self.logger.debug(f"Executing task asynchronously: {_mask_sensitive_info(task)}")
				response = await self._execute_task_async(
					task=task,
					callbacks=callbacks,
					connection_type=connection_type,
					response_format=response_format,
					context=context,
				)
				responses.append(response)
				if not response.success:
					break  # Stop execution if a task fails and no fallback is provided
		elif execution_mode == FiscusExecutionType.PARALLEL:
			self.logger.debug("Executing tasks in parallel asynchronously.")
			tasks_coroutines = [
				self._execute_task_async(
					task=task,
					callbacks=callbacks,
					connection_type=connection_type,
					response_format=response_format,
					context=context,
				)
				for task in tasks
			]
			responses = await asyncio.gather(*tasks_coroutines)
		else:
			self.logger.error("Invalid execution_mode specified.")
			raise ValueError("Invalid execution_mode. Must be FiscusExecutionType.SEQUENTIAL or FiscusExecutionType.PARALLEL.")

		self.logger.debug(f"All responses collected asynchronously: {responses}")
		return FiscusResponse(success=True, result=responses)

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
				return response
			else:
				return {"next_action": "proceed"}