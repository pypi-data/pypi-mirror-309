# callback_utils.py

from typing import Dict, Any
from .enums import FiscusCallbackType

class _AIOrchestratorCallbackUtilsMixin:
    def _trigger_callback(self, callback_type: FiscusCallbackType, data: Dict[str, Any]):
        """Helper method to trigger a callback if it exists in ai_callbacks."""
        callback = self.ai_callbacks.get(callback_type.value)  # Use .value for lookup consistency
        if callback:
            self.logger.debug(f"Triggering callback '{callback_type.value}' with data: {data}")
            callback(data)
