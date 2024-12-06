# fiscus_sdk/enums.py
"""
This module contains enums used throughout the Fiscus SDK.

Enums provide a structured and standardized way to manage configuration options,
logging levels, connection types, response formats, and various SDK behavior controls.
"""

import logging
import json
from enum import Enum

# Define a custom TRACE level numeric value
TRACE_LEVEL_NUM = 5
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")

# Add trace logging method to Logger class
"""
Defines a custom TRACE logging level for detailed debugging.
"""
def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kwargs)

logging.Logger.trace = trace

# Custom enum class to expose logs through the SDK
class FiscusLogLevel(Enum):
    """
    Represents log levels used within the Fiscus SDK.

    Levels:
    - TRACE: Detailed logs for debugging.
    - DEBUG: Debugging information.
    - INFO: General information logs.
    - WARNING: Warnings about potential issues.
    - ERROR: Errors that occurred during execution.
    - FATAL: Critical errors requiring immediate attention.

    Methods:
    - `public_levels`: Returns a subset of levels suitable for end-users.
    - `to_logging_level`: Maps enum values to Python's logging module levels.
    """
    TRACE = 'Trace'
    DEBUG = 'Debug'
    INFO = 'Info'
    WARNING = 'Warning'
    ERROR = 'Error'
    FATAL = 'Fatal'

    @classmethod
    def public_levels(cls):
        return {cls.INFO, cls.WARNING, cls.ERROR, cls.FATAL}

    def to_logging_level(self):
        level_map = {
            FiscusLogLevel.TRACE: TRACE_LEVEL_NUM,
            FiscusLogLevel.DEBUG: logging.DEBUG,
            FiscusLogLevel.INFO: logging.INFO,
            FiscusLogLevel.WARNING: logging.WARNING,
            FiscusLogLevel.ERROR: logging.ERROR,
            FiscusLogLevel.FATAL: logging.CRITICAL,
        }
        return level_map[self]

class FiscusConnectionType(Enum):
    """
    Represents connection types available in the Fiscus SDK.

    Types:
    - REST: RESTful HTTP connections.
    - WEBSOCKET: WebSocket-based connections.
    """
    REST = 'rest'
    WEBSOCKET = 'websocket'

class FiscusRestType(Enum):
    """
    Represents HTTP request types for REST connections.

    Types:
    - GET: HTTP GET requests.
    - POST: HTTP POST requests.
    - PUT: HTTP PUT requests.
    - DELETE: HTTP DELETE requests.
    """
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'

class FiscusResponseType(Enum):
    """
    Represents response formats for Fiscus SDK operations.

    Types:
    - TEXT: Plain text responses.
    - JSON: JSON-formatted responses.
    """
    TEXT = 'text'
    JSON = 'json'

class FiscusInitType(Enum):
    """
    Controls initialization behavior of the Fiscus SDK.

    Types:
    - LAZY: Resources are initialized on demand.
    - EAGER: Resources are initialized immediately.
    """
    LAZY = 'lazy'
    EAGER = 'eager'

class FiscusExecutionType(Enum):
    """
    Determines execution behavior for tasks in the Fiscus SDK.

    Types:
    - PARALLEL: Tasks are executed concurrently.
    - SEQUENTIAL: Tasks are executed one after another.
    """
    PARALLEL = 'parallel'
    SEQUENTIAL = 'sequential'

class FiscusMemoryRetrievalType(Enum):
    """
    Defines retrieval strategies for vector memory in the Fiscus SDK.

    Types:
    - SEMANTIC_SEARCH: Retrieves data based on semantic similarity.
    - KEYWORD_SEARCH: Retrieves data based on keyword matching.
    - HYBRID_SEARCH: Combines semantic and keyword-based retrieval.
    """
    SEMANTIC_SEARCH = 'semantic_search'
    KEYWORD_SEARCH = 'keyword_search'
    HYBRID_SEARCH = 'hybrid_search'

class FiscusMemoryStorageType(Enum):
    """
    Controls how vector memory is stored in the Fiscus SDK.

    Types:
    - APPEND: Adds new data without modifying existing data.
    - UPDATE: Updates existing data.
    - UPSERT: Combines update and insert operations.
    """
    APPEND = 'append'
    UPDATE = 'update'
    UPSERT = 'upsert'

class FiscusActionType(Enum):
    """
    Represents WebSocket message types for the Fiscus SDK.

    Types:
    - ACTION: General action-related messages.
    - USER: User-specific messages.
    """
    ACTION = 'action'
    USER = 'user'

    def __str__(self):
        return self.value

    def to_json(self):
        return self.value

class FiscusLLMType(Enum):
    """
    Specifies supported Large Language Model (LLM) providers for AI-driven workflows.

    Types:
    - OPENAI: OpenAI models.
    - ANTHROPIC: Anthropic models.
    - GEMINI: Google Gemini models.
    - LLAMA: Meta LLaMA models.
    - COHERE: Cohere models.
    """
    OPENAI = 'openai'
    ANTHROPIC = 'anthropic'
    GEMINI = 'gemini'
    LLAMA = 'llama'
    COHERE = 'cohere'

class FiscusLLMTaskType(Enum):
    """
    Specifies AI task types supported in the Fiscus SDK.

    Types:
    - CATEGORY_CLASSIFICATION: Classify input into predefined categories.
    - CONNECTOR_SELECTION: Select appropriate connectors for a workflow.
    - TASK_PLANNING: Plan tasks based on input data.
    - LOGIC_EVALUATION: Evaluate conditional logic.
    """
    CATEGORY_CLASSIFICATION = "classify_input"
    CONNECTOR_SELECTION = "select_connectors"
    TASK_PLANNING = "plan_tasks"
    LOGIC_EVALUATION = "evaluate_conditional_logic"

class FiscusActionTypeEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for serializing `FiscusActionType` enums.
    """
    def default(self, obj):
        if isinstance(obj, FiscusActionType):
            return obj.value
        return super().default(obj)

class FiscusCallbackType(Enum):
    """
    Defines callback types for handling events in the Fiscus SDK.

    SDK Callbacks:
    - ON_SUCCESS: Triggered when an operation succeeds.
    - ON_ERROR: Triggered when an operation fails.
    - ON_AUTH: Triggered during authentication.
    - ON_STREAM: Triggered for streaming events.
    - ON_LOG: Triggered for logging events.
    - ON_RESPONSE: Triggered upon receiving a response.

    AI Callbacks:
    - AI_FETCH_CATEGORIES: Triggered when fetching categories.
    - AI_CATEGORY_SELECTION: Triggered during category selection.
    - AI_FETCH_CONNECTORS: Triggered when fetching connectors.
    - AI_CONNECTOR_SELECTION: Triggered during connector selection.
    - AI_FETCH_OPERATIONS: Triggered when fetching operations.
    - AI_OPERATION_SELECTION: Triggered during operation selection.
    - AI_FETCH_OPERATION_DETAILS: Triggered when fetching operation details.
    - AI_TASK_CREATION: Triggered during task creation.
    - AI_COMPLETE: Triggered when AI processing completes.
    """
    ON_SUCCESS = "on_success"
    ON_ERROR = "on_error"
    ON_AUTH = "on_auth"
    ON_STREAM = "on_stream"
    ON_LOG = "on_log"
    ON_RESPONSE = "on_response"
    AI_FETCH_CATEGORIES = "on_fetch_categories"
    AI_CATEGORY_SELECTION = "on_category_selection"
    AI_FETCH_CONNECTORS = "on_fetch_connectors"
    AI_CONNECTOR_SELECTION = "on_connector_selection"
    AI_FETCH_OPERATIONS = "on_fetch_operations"
    AI_OPERATION_SELECTION = "on_operation_selection"
    AI_FETCH_OPERATION_DETAILS = "on_fetch_operation_details"
    AI_TASK_CREATION = "on_task_creation"
    AI_COMPLETE = "on_ai_complete"

class FiscusPlanningType(Enum):
    """
    Specifies planning control types for AI-driven workflows in the Fiscus SDK.

    Types:
    - STREAMLINED: Minimal user input, fully automated planning.
    - HYBRID: Balanced control between user and automation.
    - FULL_CONTROL: Full user control over planning.
    """
    STREAMLINED = 'streamlined'
    HYBRID = 'hybrid'
    FULL_CONTROL = 'full_control'

class FiscusModeType(Enum):
    """
    Represents operational modes in the Fiscus SDK.

    Types:
    - PLAN: Plan workflows or operations.
    - TEST: Test workflows or operations.
    - EXECUTE: Execute workflows or operations.
    """
    PLAN = 'plan'
    TEST = 'test'
    EXECUTE = 'execute'
