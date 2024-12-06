# fiscus/__init__.py

"""
Fiscus SDK - Your AI Integration Engineer
"""

__version__ = '0.1.0-alpha.8'
__version_info__ = (0, 1, 0, 'alpha', 8)
__author__ = "Fiscus Flows, Inc."
__license__ = "Proprietary"
__description__ = "Fiscus is the definitive platform for AI-driven integrations, serving as your AI Integration Engineer. It empowers developers to deploy intelligent agents and large language models that seamlessly integrate with any API or service. With Fiscus, manual mapping, custom code, and infrastructure complexities are eliminated, enabling a truly adaptive, agentic approach to integration."

# Explicit relative imports for better internal structure and control
from .client import FiscusClient
from .user import FiscusUser
from .connector import FiscusConnector
from .response import FiscusResponse
from .audit import FiscusAuditTrail
from .fiscus_file import FiscusFile
from .exceptions import (
    FiscusError,
    FiscusAuthenticationError,
    FiscusAuthorizationError,
    FiscusValidationError,
)
from .callbacks import (
	FiscusCallback,
	FiscusOnSuccess,
	FiscusOnError,
	FiscusOnAuth,
	FiscusOnLog,
	FiscusOnStream,
	FiscusOnResponse,
	FiscusAIFetchCategories,
	FiscusAICategorySelection,
	FiscusAIFetchConnectors,
	FiscusAIConnectorSelection,
	FiscusAIFetchOperations,
	FiscusAIOperationSelection,
	FiscusAIFetchOperationDetails,
	FiscusAITaskCreation,
	FiscusAIComplete
)
from .enums import (
	FiscusResponseType,
	FiscusConnectionType,
	FiscusExecutionType,
	FiscusInitType,
	FiscusLogLevel,
	FiscusLLMType,
	FiscusMemoryRetrievalType,
	FiscusMemoryStorageType,
	FiscusCallbackType
)

# Only expose essential classes and functions in __all__
__all__ = [
    'FiscusClient',
    'FiscusUser',
    'FiscusConnector',
    'FiscusResponse',
    'FiscusError',
    'FiscusAuthenticationError',
    'FiscusAuthorizationError',
    'FiscusValidationError',
    'FiscusCallback',
    'FiscusOnSuccess',
	'FiscusOnError',
	'FiscusOnAuth',
	'FiscusOnLog',
	'FiscusOnStream',
	'FiscusOnResponse',
	'FiscusAIFetchCategories',
	'FiscusAICategorySelection',
	'FiscusAIFetchConnectors',
	'FiscusAIConnectorSelection',
	'FiscusAIFetchOperations',
	'FiscusAIOperationSelection',
	'FiscusAIFetchOperationDetails',
	'FiscusAITaskCreation',
	'FiscusAIComplete',
    'FiscusAuditTrail',
	'FiscusFile',
    'FiscusResponseType',
    'FiscusConnectionType',
	'FiscusExecutionType',
    'FiscusInitType',
    'FiscusLogLevel',
	'FiscusLLMType',
	'FiscusMemoryRetrievalType',
	'FiscusMemoryStorageType',
	'FiscusCallbackType'
]