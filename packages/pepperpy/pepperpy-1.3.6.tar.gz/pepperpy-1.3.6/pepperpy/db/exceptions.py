"""Database exceptions"""


class DatabaseError(Exception):
    """Base database exception"""

    def __init__(self, message: str, cause: Exception | None = None):
        super().__init__(message)
        self.cause = cause


class ConnectionError(DatabaseError):
    """Database connection error"""



class QueryError(DatabaseError):
    """Query execution error"""



class TransactionError(DatabaseError):
    """Transaction error"""



class ConfigurationError(DatabaseError):
    """Configuration error"""



class EngineError(DatabaseError):
    """Engine-related error"""

