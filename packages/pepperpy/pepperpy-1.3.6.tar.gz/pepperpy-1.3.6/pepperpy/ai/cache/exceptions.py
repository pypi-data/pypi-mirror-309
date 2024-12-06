"""Cache specific exceptions"""

from pepperpy.core.exceptions import PepperPyError


class CacheError(PepperPyError):
    """Base exception for cache errors"""



class CacheKeyError(CacheError):
    """Error for invalid cache key operations"""



class CacheValueError(CacheError):
    """Error for invalid cache value operations"""

