# fiscus_sdk/llm_config.py

import logging
from typing import Dict, Any, List
from .enums import FiscusLLMType

class _LLMConfig:
    def __init__(self):
        self.logger = logging.getLogger(f'.llm_config.{self.__class__.__name__}')
        # Define action-specific configurations for each LLM type, using the FiscusLLMType enum directly
        self.action_configs = {
            'classify_input': {
                FiscusLLMType.ANTHROPIC: {
                    'prompt_suffix': "\n\nPlease respond in JSON format as follows, no text:\n{\"categories\": [\"Email\", \"Finance\", ...]}",
                    'response_key': 'categories',
                    'function_schema': {
                        "name": "classify_input",
                        "description": "Classify the user's input into categories.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "categories": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "List of categories relevant to the user's request."
                                }
                            },
                            "required": ["categories"]
                        }
                    }
                },
                FiscusLLMType.OPENAI: {
                    'prompt_suffix': "\n\nReturn categories in JSON format, no text::\n{\"categories\": [\"Email\", \"Finance\", ...]}",
                    'response_key': 'categories',
                    'function_schema': {
                        "name": "classify_input",
                        "description": "Classify the user's input into categories.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "categories": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "enum": []
                                    },
                                    "description": "List of categories relevant to the user's request."
                                }
                            },
                            "required": ["categories"]
                        }
                    }
                }
            },
            'select_connectors': {
                FiscusLLMType.ANTHROPIC: {
                    'prompt_suffix': "\n\nProvide connectors in JSON format only, no text:\n{\"connectors\": [\"connector_1\", \"connector_2\", ...]}",
                    'response_key': 'connectors',
                    'function_schema': {
                        "name": "select_connectors",
                        "description": "Select the most relevant connector(s) based on the user's request.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "connectors": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "List of connectors relevant to the user's request."
                                }
                            },
                            "required": ["connectors"]
                        }
                    }
                },
                FiscusLLMType.OPENAI: {
                    'prompt_suffix': "\n\nRespond with connectors in JSON format only:\n{\"connectors\": [\"connector_1\", \"connector_2\", ...]}",
                    'response_key': 'connectors',
                    'function_schema': {
                        "name": "select_connectors",
                        "description": "Select the most relevant connectors based on the user's request.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "connectors": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "enum": []
                                    },
                                    "description": "List of connectors relevant to the user's request."
                                }
                            },
                            "required": ["connectors"]
                        }
                    }
                }
            },
            'select_operations': {
                FiscusLLMType.ANTHROPIC: {
                    'prompt_suffix': "\n\nProvide operations in JSON format only:\n{\"operations\": [\"operation_1\", \"operation_2\", ...]}",
                    'response_key': 'operations',
                    'function_schema': {
                        "name": "select_operations",
                        "description": "Select the most relevant operations based on the selected connectors.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "operations": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "List of operations relevant to the selected connectors."
                                }
                            },
                            "required": ["operations"]
                        }
                    }
                },
                FiscusLLMType.OPENAI: {
                    'prompt_suffix': "\n\nRespond with operations in JSON:\n{\"operations\": [\"operation_1\", \"operation_2\", ...]}",
                    'response_key': 'operations',
                    'function_schema': {
                        "name": "select_operations",
                        "description": "Select the most relevant operations based on the selected connectors.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "operations": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "List of operations relevant to the selected connectors."
                                }
                            },
                            "required": ["operations"]
                        }
                    }
                }
            },
            'plan_tasks': {
                FiscusLLMType.ANTHROPIC: {
                    'prompt_suffix': "\n\nPlan out tasks in JSON only, no text:\n[{\"connector\": \"...\", \"operation\": \"...\", \"params\": {\"key\": \"value\"}}]",
                    'response_key': 'tasks',
                    'function_schema': {
                        "name": "plan_tasks",
                        "description": "Plan out the sequence of API calls needed to fulfill the user's request.",
                        "parameters": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "connector": {"type": "string"},
                                    "operation": {"type": "string"},
                                    "params": {"type": "object"},
                                    "conditional_logic": {"type": "string"}
                                },
                                "required": ["connector", "operation"]
                            }
                        }
                    }
                },
                FiscusLLMType.OPENAI: {
					'prompt_suffix': "\n\nProvide task plans in JSON format:\n{\"tasks\": [{\"connector\": \"...\", \"operation\": \"...\", \"params\": {...}, \"conditional_logic\": \"...\"}]}",
					'response_key': 'tasks',
					'function_schema': {
						"name": "plan_tasks",
						"description": "Plan out the sequence of API calls needed to fulfill the user's request.",
						"parameters": {
							"type": "object",
							"properties": {
								"tasks": {
									"type": "array",
									"items": {
										"type": "object",
										"properties": {
											"connector": {"type": "string"},
											"operation": {"type": "string"},
											"params": {"type": ["object", "null"]},
											"conditional_logic": {"type": ["string", "null"]}
										},
										"required": ["connector", "operation", "params", "conditional_logic"],
										"additionalProperties": False
									}
								}
							},
							"required": ["tasks"],
							"additionalProperties": False
						}
					}
				}
            },
            'evaluate_conditional_logic': {
                FiscusLLMType.ANTHROPIC: {
                    'prompt_suffix': "\n\nEvaluate the condition and respond in JSON:\n{\"result\": true/false}",
                    'response_key': 'result',
                    'function_schema': {
                        "name": "evaluate_conditional_logic",
                        "description": "Evaluate the condition and respond with the result.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "boolean",
                                    "description": "Result of the condition evaluation."
                                }
                            },
                            "required": ["result"]
                        }
                    }
                },
                FiscusLLMType.OPENAI: {
					'prompt_suffix': "\n\nEvaluate the condition and respond with result in JSON:\n{\"result\": true/false}",
					'response_key': 'result',
					'function_schema': {
						"name": "evaluate_conditional_logic",
						"description": "Evaluate the conditional logic based on the provided context.",
						"parameters": {
							"type": "object",
							"properties": {
								"result": {
									"type": "boolean",
									"description": "The result of evaluating the conditional logic."
								}
							},
							"required": ["result"],
							"additionalProperties": False
						}
					}
				}
            },
            'evaluate_workflow_step': {
                FiscusLLMType.ANTHROPIC: {
                    'prompt_suffix': "\n\nProvide guidance in JSON format only:\n{\"next_action\": \"...\", \"override_task\": {...}, \"halt\": true/false, \"reconfigure\": {...}}",
                    'response_key': 'next_action',
                    'function_schema': {
                        "name": "evaluate_workflow_step",
                        "description": "Evaluate the current step and provide next actions or overrides.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "next_action": {
                                    "type": "string",
                                    "description": "The recommended next action, e.g., 'proceed', 'retry', 'modify'."
                                },
                                "override_task": {
                                    "type": ["object", "null"],
                                    "description": "Task details to override the current task, if applicable."
                                },
                                "halt": {
                                    "type": "boolean",
                                    "description": "Indicates whether the workflow should halt."
                                },
                                "reconfigure": {
                                    "type": ["object", "null"],
                                    "description": "Parameters for reconfiguration, if needed."
                                }
                            },
                            "required": ["next_action", "halt"],
                            "additionalProperties": False
                        }
                    }
                },
                FiscusLLMType.OPENAI: {
                    'prompt_suffix': "\n\nRespond with next steps in JSON format only:\n{\"next_action\": \"...\", \"override_task\": {...}, \"halt\": true/false, \"reconfigure\": {...}}",
                    'response_key': 'next_action',
                    'function_schema': {
                        "name": "evaluate_workflow_step",
                        "description": "Evaluate the workflow step to decide on next actions, possible overrides, or halts.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "next_action": {
                                    "type": "string",
                                    "description": "The suggested action to proceed, retry, or modify the task."
                                },
                                "override_task": {
                                    "type": ["object", "null"],
                                    "description": "Optional override task details if a modification is suggested."
                                },
                                "halt": {
                                    "type": "boolean",
                                    "description": "Indicate whether the workflow should halt at this step."
                                },
                                "reconfigure": {
                                    "type": ["object", "null"],
                                    "description": "Optional reconfiguration parameters to update the workflow logic."
                                }
                            },
                            "required": ["next_action", "halt"],
                            "additionalProperties": False
                        }
                    }
                }
			}
        }

    def get_action_config(self, action: str, llm_type: FiscusLLMType) -> Dict[str, Any]:
        """
        Retrieve configuration details for a specific action and LLM type using FiscusLLMType enums.

        :param action: The action to retrieve configuration for (e.g., 'classify_input').
        :param llm_type: The type of LLM being used (from FiscusLLMType).
        :return: A dictionary with the prompt suffix, response key, and function schema for the action.
        """
        action_config = self.action_configs.get(action, {}).get(llm_type, {})

        # Add logging to verify retrieval of prompt suffix
        prompt_suffix = action_config.get('prompt_suffix', '')
        if not prompt_suffix:
            self.logger.debug(f"No prompt suffix found for action '{action}' and llm_type '{llm_type}'")
        else:
            self.logger.debug(f"Retrieved prompt suffix for action '{action}' and llm_type '{llm_type}': {prompt_suffix}")

        return action_config

    def get_function_schema(self, action: str, llm_type: FiscusLLMType, available_enums: List[str] = None) -> Dict[str, Any]:
        """
        Retrieves the function schema for a specific action and LLM type, allowing customization of enums.

        :param action: The action to retrieve configuration for (e.g., 'classify_input').
        :param llm_type: The type of LLM being used (from FiscusLLMType).
        :param available_enums: Optional list of enum values for categories or connectors.
        :return: The function schema with enums populated if applicable.
        """
        schema = self.action_configs.get(action, {}).get(llm_type, {}).get('function_schema', {}).copy()
        if available_enums:
            # Insert available enums for "categories" or "connectors" as needed.
            properties = schema.get("parameters", {}).get("properties", {})
            if "categories" in properties:
                properties["categories"]["items"]["enum"] = available_enums
            elif "connectors" in properties:
                properties["connectors"]["items"]["enum"] = available_enums
        return schema
