# fiscus_sdk/audit.py

import logging
from typing import Any, Dict, List
from datetime import datetime, timezone

from .enums import FiscusActionType

class FiscusAuditTrail:
    """
    Records actions and events for auditing purposes.
    """

    def __init__(self, entity_name: str, enable_logging: bool = False):
        """
        Initialize the FiscusAuditTrail.

        :param entity_name: Name of the entity being audited (e.g., FiscusConnector name).
        :param enable_logging: If True, audit records will be logged.
        """
        self.entity_name = entity_name
        self.records: List[Dict[str, Any]] = []
        self.enable_logging = enable_logging
        self.logger = logging.getLogger(f'.connection.{self.entity_name}')

        if not self.enable_logging:
            # Disable logging for this logger
            self.logger.disabled = True

    def record(self, action: FiscusActionType, details: Dict[str, Any]) -> None:
        """
        Record an action in the audit trail.

        :param action: Action name.
        :param details: Details of the action.
        """
        timestamp = datetime.now(tz=timezone.utc).isoformat()
        record = {
            'timestamp': timestamp,
            'entity': self.entity_name,
            'action': action,
            'details': details
        }
        self.records.append(record)
        if self.enable_logging:
            self.logger.info(f"Audit record: {record}")

    def get_records(self) -> List[Dict[str, Any]]:
        """
        Get all audit records.

        :return: List of audit records.
        """
        return self.records

    def clear_records(self) -> None:
        """
        Clear all audit records.
        """
        self.records.clear()
        if self.enable_logging:
            self.logger.info("Audit records cleared.")
