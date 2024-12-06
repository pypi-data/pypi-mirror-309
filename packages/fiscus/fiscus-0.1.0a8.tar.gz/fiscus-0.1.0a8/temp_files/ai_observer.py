# ai_observer.py

from typing import Dict, Any, Optional, Callable, List

class _AIObserver:
	def __init__(self, orchestrator: Any):
		"""
		Observer that manages responses to events in planning, testing, and execution phases.
		Adjusts task parameters, reconfigures task sequences, and requests retries or re-planning as needed.
		"""
		self.orchestrator = orchestrator
		self.context = {}
		self.retry_limit = 3  # Example retry limit, can be configurable
		self.event_handlers = self._initialize_event_handlers()

	def _initialize_event_handlers(self) -> Dict[str, Callable]:
		"""
		Initialize handlers for various events in the workflow. Each handler allows
		customization of responses based on the specific phase of the workflow.
		"""
		return {
			# Planning Phase
			"planning_start": self.on_planning_start,
			"planning_success": self.on_planning_success,
			"planning_failure": self.on_planning_failure,
			"replan_request": self.on_replan_request,

			# Testing Phase
			"testing_start": self.on_testing_start,
			"testing_success": self.on_testing_success,
			"testing_failure": self.on_testing_failure,
			"test_case_retry": self.on_test_case_retry,

			# Execution Phase
			"task_start": self.on_task_start,
			"task_success": self.on_task_success,
			"task_failure": self.on_task_failure,
			"task_retry": self.on_task_retry,
			"task_fallback": self.on_task_fallback,
			"task_skipped": self.on_task_skipped,
			"memory_update": self.on_memory_update,
			"execution_complete": self.on_execution_complete,

			# Context Management
			"context_update": self.on_context_update,
			"dynamic_reconfiguration": self.on_dynamic_reconfiguration,
			"logging_event": self.on_logging_event,

			# Workflow Failure
			"workflow_failure": self.on_workflow_failure,
		}

	def update(self, event_type: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		"""
		Trigger the appropriate handler based on the event type, and pass data relevant to the event.
		"""
		handler = self.event_handlers.get(event_type)
		if handler:
			response = handler(data)
			# Evaluate if we need further LLM-based actions for complex decisions
			if self._needs_ai_evaluation(response):
				ai_response = self._ai_evaluate_event(event_type, data)
				response.update(ai_response)  # Integrate LLM recommendations into the response
			return response
		else:
			self.log_event("warning", f"No handler found for event type: {event_type}")
			return None

	def _needs_ai_evaluation(self, response: Dict[str, Any]) -> bool:
		"""
		Determines if the response requires further evaluation by the LLM, such as for overrides or halts.
		"""
		return any(key in response for key in ["override_task", "halt", "reconfigure", "alternative_plan", "retry_task"])

	def _ai_evaluate_event(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Use the orchestrator's LLM adapter to evaluate the event and decide on next actions.
		"""
		ai_input = {
			"event_type": event_type,
			"data": data,
			"context": self.context,
		}
		return self.orchestrator._ai_evaluate_event(ai_input)
	
	def cleanup(self):
		"""
		Clean up resources or state held within the observer.
		"""
		self.context.clear()  # Example: Clear context dictionary
		self.orchestrator = None  # Remove reference to orchestrator if no longer needed
		print("AIObserver cleanup completed.")

	# --- Overall Orchestration Flow ---
	def on_connector_selection_failure(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		self.log_event("error", "Connector selection failed.")
		alternative_connectors = self.orchestrator.override_connectors if self.orchestrator.override_connectors else []
		return {"override_connectors": alternative_connectors}

	def on_category_selection_failure(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		self.log_event("error", "Category selection failed.")
		alternative_categories = self.orchestrator.override_categories if self.orchestrator.override_categories else []
		return {"override_categories": alternative_categories}

	# --- Planning Phase Handlers ---
	def on_planning_start(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		self.log_event("info", "Planning phase initiated.")
		return {"status": "planning_started"}

	def on_planning_success(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		tasks = data.get("tasks")
		self.log_event("info", f"Planning successful with {len(tasks)} tasks.")
		# Example of modifying tasks based on observer context
		for task in tasks:
			task["params"].update({"observer_context": self.context})
		return {"updated_tasks": tasks}

	def on_planning_failure(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		error = data.get("error")
		self.log_event("error", f"Planning failed: {error}")
		alternative_plan = self.orchestrator.replan()
		return {"alternative_plan": alternative_plan, "error": error}

	def on_replan_request(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		reason = data.get("reason", "unspecified")
		self.log_event("info", f"Replan requested due to: {reason}")
		new_plan = self.orchestrator.replan()
		return {"new_plan": new_plan}

	# --- Testing Phase Handlers ---
	def on_testing_start(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		self.log_event("info", "Testing phase started.")
		return {"status": "testing_started"}

	def on_testing_success(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		test_results = data.get("results")
		self.log_event("info", f"Testing successful: {test_results}")
		return {"test_results": test_results}

	def on_testing_failure(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		failure_details = data.get("error")
		self.log_event("error", f"Testing failed with error: {failure_details}")
		fallback_test = self.orchestrator.get_fallback_test()
		return {"fallback_test": fallback_test, "error": failure_details}

	def on_test_case_retry(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		attempt = data.get("attempt", 0)
		if attempt < self.retry_limit:
			self.log_event("info", f"Retrying test case (Attempt {attempt + 1}).")
			return {"retry": True}
		else:
			self.log_event("warning", "Max retries reached for test case.")
			return {"retry": False}

	# --- Execution Phase Handlers ---
	def on_task_start(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		task = data["task"]
		# Example of modifying task parameters
		task["params"]["dynamic_flag"] = "added_by_observer"
		self.log_event("info", f"Task started: {task.get('operation')}")
		return {"override_task": task}

	def on_task_success(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		task = data["task"]
		result = data.get("response", {})
		self.log_event("info", f"Task successful: {task.get('operation')}, result: {result}")
		return {"status": "task_completed", "task_id": task.get('id')}

	def on_task_failure(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		task = data["task"]
		response = data.get("response")
		error = response.error if response else "Unknown error"
		self.log_event("error", f"Task failed: {task.get('operation')}, error: {error}")
		retry_attempt = task.get("retry_attempts", 0)
		if retry_attempt < self.retry_limit:
			task["retry_attempts"] = retry_attempt + 1
			self.log_event("info", f"Retrying task: {task.get('operation')}, attempt: {task['retry_attempts']}")
			return {"retry_task": True}
		else:
			fallback_task = self.orchestrator.get_fallback_task()
			return {"fallback_task": fallback_task}

	def on_task_retry(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		attempt = data.get("attempt")
		task = data["task"]
		self.log_event("info", f"Retrying task: {task.get('operation')}, attempt: {attempt}")
		return {"status": "retrying", "attempt": attempt}

	def on_task_fallback(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		original_task = data.get("original_task")
		fallback_task = data.get("fallback_task")
		self.log_event("info", f"Executing fallback for task: {original_task.get('operation')}")
		return {"status": "fallback_executed", "fallback_task": fallback_task}

	def on_task_skipped(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		task = data["task"]
		reason = data.get("reason", "Unknown reason")
		self.log_event("info", f"Task skipped: {task.get('operation')}, reason: {reason}")
		return {"status": "task_skipped", "task_id": task.get('id')}

	def on_memory_update(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		updated_memory = data.get("memory")
		self.context.update(updated_memory)
		self.log_event("info", "Memory updated with new context.")
		return {"updated_context": self.context}

	def on_execution_complete(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		self.log_event("info", "Execution phase complete.")
		return {"status": "execution_complete"}

	# --- Context Management and Reconfiguration ---
	def on_context_update(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		new_context = data.get("new_context", {})
		self.context.update(new_context)
		self.log_event("info", f"Context updated: {new_context}")
		return {"updated_context": self.context}

	def on_dynamic_reconfiguration(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		new_config = data.get("new_config", {})
		self.retry_limit = new_config.get("retry_limit", self.retry_limit)
		self.log_event("info", f"Dynamically reconfigured with: {new_config}")
		return {"status": "reconfigured"}

	def on_logging_event(self, data: Dict[str, Any]) -> None:
		level = data.get("level", "info")
		message = data.get("message", "")
		self.log_event(level, message)

	def on_workflow_failure(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		error = data.get("error")
		self.log_event("error", f"Workflow failed: {error}")
		# Optionally, decide to halt or replan
		# For example, you might replan
		# new_plan = self.orchestrator.replan()
		# return {"new_plan": new_plan}
		return None

	def log_event(self, level: str, message: str):
		"""
		Helper method to log events. This could be enhanced to integrate with a logging framework.
		"""
		if level == "info":
			print(f"[INFO] {message}")
		elif level == "warning":
			print(f"[WARNING] {message}")
		elif level == "error":
			print(f"[ERROR] {message}")
