# fiscus_sdk/callbacks.py

from typing import Callable, Any, Dict, Optional

# Define a single callback type for all SDK and AI-related callbacks
FiscusCallback = Callable[[Dict[str, Any]], None]

# SDK callback hooks with a Fiscus prefix to avoid clashes
FiscusOnSuccess: Optional[FiscusCallback] = None
FiscusOnError: Optional[FiscusCallback] = None
FiscusOnAuth: Optional[Callable[[str], Dict[str, Any]]] = None
FiscusOnStream: Optional[Callable[[Any], None]] = None
FiscusOnLog: Optional[FiscusCallback] = None
FiscusOnResponse: Optional[FiscusCallback] = None

# AI-driven process callbacks
FiscusAIFetchCategories: Optional[FiscusCallback] = None
FiscusAICategorySelection: Optional[FiscusCallback] = None
FiscusAIFetchConnectors: Optional[FiscusCallback] = None
FiscusAIConnectorSelection: Optional[FiscusCallback] = None
FiscusAIFetchOperations: Optional[FiscusCallback] = None
FiscusAIOperationSelection: Optional[FiscusCallback] = None
FiscusAIFetchOperationDetails: Optional[FiscusCallback] = None
FiscusAITaskCreation: Optional[FiscusCallback] = None
FiscusAIComplete: Optional[FiscusCallback] = None  # For summarizing the whole AI-driven flow