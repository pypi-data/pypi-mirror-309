# input_processing.py

import json
from typing import Dict, Any, List, Optional
from .enums import FiscusCallbackType, FiscusResponseType

class _AIOrchestratorInputProcessingMixin:
    def process_input(self, input_text: str) -> Optional[List[Dict[str, Any]]]:
        """
        Process user input to generate a list of tasks based on LLM reasoning.
        This involves querying the LLM and accessing memory.
        Supports reverse-order override priority: tasks > operations > connectors > categories.
        Each override level feeds into the remaining flow steps without premature return.
        """
        # Preprocess input if necessary
        if self.preprocess_function:
            input_text = self.preprocess_function(input_text)

        # Notify observer at input start
        observer_response = self.notify_observer("input_processing_start", {"input_text": input_text})
        if observer_response and observer_response.get("halt"):
            self.logger.info("Processing halted by observer at 'input_processing_start'.")
            return None

        # Retrieve context from memory if necessary
        context = ""
        if self.memory:
            context = self.retrieve_memory(input_text)
            observer_response = self.notify_observer("context_retrieved", {"context": context})
            if observer_response and observer_response.get("halt"):
                self.logger.info("Processing halted by observer at 'context_retrieved'.")
                return None

        # Handle overrides in priority order: tasks > operations > connectors > categories
        tasks, operations, connectors, categories = None, None, None, None

        # 1. Check for task override
        if self.custom_overrides and 'tasks' in self.custom_overrides:
            tasks = self.custom_overrides['tasks']
            self.notify_observer("task_override_used", {"tasks": tasks})

        # 2. Check for operations override if tasks are not overridden
        if not tasks and self.custom_overrides and 'operations' in self.custom_overrides:
            operations = self.custom_overrides['operations']
            tasks = self.plan_tasks(input_text, operations, context)
            self.notify_observer("operation_override_used", {"operations": operations, "tasks": tasks})

        # 3. Check for connectors override if neither tasks nor operations are overridden
        if not tasks and not operations and self.custom_overrides and 'connectors' in self.custom_overrides:
            connectors = self.custom_overrides['connectors']
            operations = self.select_operations(connectors, input_text, context)
            if not operations:
                self.notify_observer("operation_selection_failure", {"connectors": connectors})
                return None
            tasks = self.plan_tasks(input_text, operations, context)
            self.notify_observer("connector_override_used", {"connectors": connectors, "tasks": tasks})

        # 4. Check for categories override if no tasks, operations, or connectors are overridden
        if not tasks and not operations and not connectors and self.custom_overrides and 'categories' in self.custom_overrides:
            categories = self.custom_overrides['categories']

        # Normal flow if no overrides: Start with category classification
        if not tasks and not operations and not connectors and not categories:
            categories = self.classify_input(input_text, context)
            if not categories:
                observer_response = self.notify_observer("classification_failure", {"input_text": input_text})
                if observer_response and observer_response.get("proceed_with_empty"):
                    categories = observer_response.get("override_categories", [])
                if not categories:
                    self.logger.warning("No categories found or provided. Halting processing.")
                    return None

        # Proceed to connector selection if we still need connectors
        if not tasks and not operations and not connectors:
            connectors = self.select_connectors(input_text, categories, context)
            if not connectors:
                observer_response = self.notify_observer("connector_selection_failure", {"categories": categories})
                if observer_response and observer_response.get("proceed_with_empty"):
                    connectors = observer_response.get("override_connectors", [])
                if not connectors:
                    self.logger.warning("No connectors found or provided. Halting processing.")
                    return None

        # Proceed to operation selection if we still need operations
        if not tasks and not operations:
            operations = self.select_operations(connectors, input_text, context)
            if not operations:
                observer_response = self.notify_observer("operation_selection_failure", {"connectors": connectors})
                if observer_response and observer_response.get("proceed_with_empty"):
                    operations = observer_response.get("override_operations", [])
                if not operations:
                    self.logger.warning("No operations found or provided. Halting processing.")
                    return None

        # Proceed to task planning if we still need tasks
        if not tasks:
            tasks = self.plan_tasks(input_text, operations, context)
            if not tasks:
                observer_response = self.notify_observer("task_planning_failure", {"operations": operations})
                if observer_response and observer_response.get("proceed_with_empty"):
                    tasks = observer_response.get("override_tasks", [])
                if not tasks:
                    self.logger.warning("No tasks planned or provided. Halting processing.")
                    return None

        # Notify observer of successful task planning
        observer_response = self.notify_observer("task_planning_success", {"tasks": tasks})
        if observer_response and observer_response.get("override_tasks"):
            tasks = observer_response["override_tasks"]  # Use overridden tasks if provided by observer

        return tasks

    def classify_input(self, input_text: str, context: str) -> List[str]:
        """
        Use _LLMAdapter to classify the user input into categories.
        """
        self.logger.debug(f"Classifying input: {input_text}")

        # Load the categories few-shot examples
        all_categories_examples = self._load_categories_few_shot()
        available_category_names = self.user._get_connected_categories()

        # Notify observer about available categories
        observer_response = self.notify_observer("fetch_categories", {"available_categories": available_category_names})
        if observer_response:
            self.logger.debug(f"Observer response for 'fetch_categories': {observer_response}")
            if observer_response.get("override_categories"):
                available_category_names = observer_response["override_categories"]
        else:
            self.logger.debug("No observer response for 'fetch_categories'.")

        # Filter few-shot examples
        available_categories = [
            category for category in all_categories_examples if category["category"] in available_category_names
        ]
        few_shot_examples = [
            {
                "user": f"User Input: {example}",
                "assistant": f"Categories: {json.dumps([category['category']])}"
            }
            for category in available_categories
            for example in category["examples"]
        ]

        # Prepare function schema and prompt
        function_schema = self.llm_config.get_function_schema(
            action="classify_input",
            llm_type=self.llm_type,
            available_enums=available_category_names
        )
        prompt = f"User Input: {input_text}\nIdentify the categories relevant to the user's request."

        # Execute using _LLMAdapter
        result = self.llm_adapter.execute(
            action="classify_input",
            prompt=prompt,
            context=context,
            function_schema=function_schema,
            few_shot_examples=few_shot_examples,
            temperature=0.0,
            max_tokens=256,
            response_format=FiscusResponseType.JSON,
            **self.custom_options
        )

        # Notify observer with the classification result
        observer_response = self.notify_observer("category_selection", {"input_text": input_text, "selected_categories": result})
        if observer_response:
            self.logger.debug(f"Observer response for 'category_selection': {observer_response}")
            return observer_response.get("override_categories", result) if result else []
        else:
            self.logger.warning("No observer response for 'category_selection'. Proceeding with original categories.")
            return result if result else []

    def select_connectors(self, input_text: str, categories: List[str], context: str) -> List[str]:
        """
        Use _LLMAdapter to select appropriate connectors based on categories.
        """
        self.logger.debug(f"Selecting connectors for categories: {categories}")

        # Retrieve available connectors from user data
        available_connectors = self.user._get_connected_connectors(categories)

        # Notify observer about available connectors
        observer_response = self.notify_observer("fetch_connectors", {"available_connectors": available_connectors})
        if observer_response:
            self.logger.debug(f"Observer response for 'fetch_connectors': {observer_response}")
            if observer_response.get("override_connectors"):
                available_connectors = observer_response["override_connectors"]
        else:
            self.logger.debug("No observer response for 'fetch_connectors'.")

        # Load few-shot examples
        all_connectors_examples = self._load_connectors_few_shot()
        few_shot_examples = [
            {
                "user": json.dumps({"categories": example["user"]}),
                "assistant": json.dumps({"connectors": example["assistant"]["connectors"]})
            }
            for example in all_connectors_examples if any(cat in categories for cat in example["user"])
        ]

        # Prepare schema and prompt
        function_schema = self.llm_config.get_function_schema(
            action="select_connectors",
            llm_type=self.llm_type,
            available_enums=available_connectors
        )
        prompt = (
            f"User Input: {input_text}\n"
            f"Available Connectors: {available_connectors}\n"
            "Select the most relevant connector(s) to fulfill user needs."
        )

        # Execute LLM
        result = self.llm_adapter.execute(
            action="select_connectors",
            prompt=prompt,
            context=context,
            function_schema=function_schema,
            few_shot_examples=few_shot_examples,
            temperature=0.0,
            max_tokens=256,
            response_format=FiscusResponseType.JSON,
            **self.custom_options
        )

        # Notify observer of connector selection result
        observer_response = self.notify_observer("connector_selection", {"categories": categories, "selected_connectors": result})
        if observer_response:
            self.logger.debug(f"Observer response for 'connector_selection': {observer_response}")
            return observer_response.get("override_connectors", result if isinstance(result, list) else result.get("connectors", []))
        else:
            self.logger.warning("No observer response for 'connector_selection'. Proceeding with original connectors.")
            return result if isinstance(result, list) else result.get("connectors", [])

    def select_operations(self, connectors: List[str], input_text: str, context: str) -> List[str]:
        """
        Use LLM to select the relevant operations based on the user's selected connectors.
        """
        self.logger.debug(f"Selecting operations for connectors: {connectors}")

        # Retrieve available operations from user data
        available_operations = self.user._get_connected_operations(connectors)

        # Notify observer about available operations
        observer_response = self.notify_observer("fetch_operations", {"available_operations": available_operations})
        if observer_response:
            self.logger.debug(f"Observer response for 'fetch_operations': {observer_response}")
            if observer_response.get("override_operations"):
                available_operations = observer_response["override_operations"]
        else:
            self.logger.debug("No observer response for 'fetch_operations'.")

        # Create few-shot examples for connectors and operations
        all_operations_examples = self._load_operations_few_shot()
        few_shot_examples = [
            {
                "user": json.dumps({"connector": example["user"]}),
                "assistant": json.dumps({"operations": example["assistant"]["operations"]})
            }
            for example in all_operations_examples if any(conn in example["user"] for conn in connectors)
        ]

        # Prepare schema and prompt
        function_schema = self.llm_config.get_function_schema(
            action="select_operations",
            llm_type=self.llm_type,
            available_enums=available_operations
        )
        prompt = (
            f"User Input: {input_text}\n"
            f"Selected Connectors: {connectors}\n"
            f"Available Operations: {json.dumps(available_operations)}\n"
            "Provide the exact operation names for each connector."
        )

        # Execute LLM
        result = self.llm_adapter.execute(
            action="select_operations",
            prompt=prompt,
            context=context,
            function_schema=function_schema,
            few_shot_examples=few_shot_examples,
            temperature=0.0,
            max_tokens=256,
            response_format=FiscusResponseType.JSON,
            **self.custom_options
        )

        # Notify observer of operation selection result
        observer_response = self.notify_observer("operation_selection", {"connectors": connectors, "selected_operations": result})
        if observer_response:
            self.logger.debug(f"Observer response for 'operation_selection': {observer_response}")
            return observer_response.get("override_operations", result if isinstance(result, list) else result.get("operations", []))
        else:
            self.logger.warning("No observer response for 'operation_selection'. Proceeding with original operations.")
            return result if isinstance(result, list) else result.get("operations", [])

    def plan_tasks(self, input_text: str, connectors_operations: List[Dict[str, Any]], context: str) -> List[Dict[str, Any]]:
        """
        Use _LLMAdapter to plan out the sequence of tasks (API calls) to perform.
        """
        self.logger.debug(f"Planning tasks based on connectors and operations.")

        # Load all task few-shot examples
        few_shot_examples = self._load_tasks_few_shot()

        # Prepare function schema and prompt
        function_schema = self.llm_config.get_function_schema(
            action="plan_tasks",
            llm_type=self.llm_type,
            available_enums=connectors_operations
        )
        prompt = (
            f"User Input: {input_text}\n"
            f"Connectors and Operations: {json.dumps(connectors_operations)}\n"
            "Using only the exact connector and operation names listed, generate the JSON tasks."
        )

        # Execute using _LLMAdapter
        result = self.llm_adapter.execute(
            action="plan_tasks",
            prompt=prompt,
            context=context,
            function_schema=function_schema,
            few_shot_examples=few_shot_examples,
            temperature=0.0,
            max_tokens=1024,
            response_format=FiscusResponseType.JSON,
            **self.custom_options
        )

        # Notify observer of task planning result
        observer_response = self.notify_observer("task_planning", {"planned_tasks": result})
        if observer_response:
            self.logger.debug(f"Observer response for 'task_planning': {observer_response}")
            tasks = observer_response.get("override_tasks", result if isinstance(result, list) else result.get("tasks", []))
        else:
            self.logger.warning("No observer response for 'task_planning'. Proceeding with original tasks.")
            tasks = result if isinstance(result, list) else result.get("tasks", [])

        # Validate each task's format, report if invalid
        for task in tasks:
            if not isinstance(task, dict) or "connector" not in task or "operation" not in task:
                self.logger.error("Each task must be a dictionary with 'connector' and 'operation'.")
                self.notify_observer("task_validation_failure", {"invalid_task": task})
                return []

        return tasks

    def evaluate_conditional_logic(self, conditional_logic: str, context: Dict[str, Any]) -> Any:
        """
        Use _LLMAdapter to evaluate the conditional logic specified in the task.
        Returns the result of the evaluation, or uses observer feedback if available.
        """
        self.logger.debug(f"Evaluating conditional logic: {conditional_logic}")

        # Notify observer at the start of evaluation
        observer_response = self.notify_observer("conditional_evaluation_start", {
            "conditional_logic": conditional_logic,
            "context": context
        })
        if observer_response:
            self.logger.debug(f"Observer response for 'conditional_evaluation_start': {observer_response}")
            if observer_response.get("halt"):
                self.logger.info("Evaluation halted by observer at 'conditional_evaluation_start'.")
                return None  # Stop if observer instructs to halt
        else:
            self.logger.debug("No observer response for 'conditional_evaluation_start'.")

        # Allow observer to override conditional logic or context
        conditional_logic = observer_response.get("override_conditional_logic", conditional_logic) if observer_response else conditional_logic
        context = observer_response.get("override_context", context) if observer_response else context

        few_shot_examples = self.few_shot_examples.get("conditional_evaluation", [])

        # Prepare function schema
        function_schema = {
            "name": "evaluate_conditional_logic",
            "description": "Evaluate the conditional logic based on the provided context.",
            "parameters": {
                "type": "object",
                "properties": {
                    "result": {
                        "type": ["boolean", "number", "string", "object", "array"],
                        "description": "The result of evaluating the conditional logic."
                    }
                },
                "required": ["result"]
            }
        }

        # Prepare prompt
        prompt = (
            f"Conditional Logic: {conditional_logic}\n"
            f"Context: {json.dumps(context)}\n"
            "Evaluate the conditional logic and provide the result."
        )

        # Execute using _LLMAdapter
        result = self.llm_adapter.execute(
            action="evaluate_conditional_logic",
            prompt=prompt,
            context=None,
            function_schema=function_schema,
            few_shot_examples=few_shot_examples,
            temperature=0.0,
            max_tokens=256,
            response_format=FiscusResponseType.JSON,
            **self.custom_options
        )

        if not result or "result" not in result:
            self.logger.warning("No result from LLM for conditional logic.")
            self.notify_observer("conditional_evaluation_failure", {
                "conditional_logic": conditional_logic,
                "context": context
            })

            if self.error_callback:
                self.error_callback(Exception("No result from LLM for conditional logic."))
            return None

        # Notify observer of successful evaluation with the result
        observer_response = self.notify_observer("conditional_evaluation_success", {
            "conditional_logic": conditional_logic,
            "context": context,
            "result": result["result"]
        })
        if observer_response:
            self.logger.debug(f"Observer response for 'conditional_evaluation_success': {observer_response}")
            return observer_response.get("override_result", result["result"])
        else:
            self.logger.warning("No observer response for 'conditional_evaluation_success'. Proceeding with LLM result.")
            return result["result"]
