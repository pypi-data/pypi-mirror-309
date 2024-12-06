# fiscus_sdk/exceptions.py

class FiscusError(Exception):
    """Base exception class for Fiscus SDK."""
    pass

class FiscusAuthenticationError(FiscusError):
    """Raised when authentication fails."""
    pass

class FiscusAuthorizationError(FiscusError):
    """Raised when authorization fails."""
    pass

class FiscusValidationError(FiscusError):
    """Raised when validation of input fails."""
    pass
