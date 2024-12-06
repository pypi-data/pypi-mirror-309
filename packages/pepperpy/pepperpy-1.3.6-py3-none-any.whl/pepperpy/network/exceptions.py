"""Network-related exceptions"""

from pepperpy.core.exceptions import PepperPyError


class NetworkError(PepperPyError):
    """Base exception for network-related errors"""


class ConnectionError(NetworkError):
    """Connection error"""


class RequestError(NetworkError):
    """Request error"""


class ResponseError(NetworkError):
    """Response error"""


class TimeoutError(NetworkError):
    """Timeout error"""


class SSLError(NetworkError):
    """SSL error"""


class ProxyError(NetworkError):
    """Proxy error"""


class DNSError(NetworkError):
    """DNS resolution error"""
