class AdEngineError(Exception):
    """Base error. Message is safe to show to the calling model."""

class NotFound(AdEngineError): ...
class Forbidden(AdEngineError): ...
class GateRefused(AdEngineError):
    """A law or approval gate refused the action. `details` explains what to fix."""
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message); self.details = details or {}
class ProviderError(AdEngineError): ...
