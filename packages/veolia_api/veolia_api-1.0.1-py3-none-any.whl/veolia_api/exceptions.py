"""Custom exception classes for Veolia API errors"""


class VeoliaAPIError(Exception):
    """Custom exception class for Veolia API errors"""

    def __init__(self, message: str) -> None:
        """Initialize the VeoliaAPIException class"""
        super().__init__(message)
