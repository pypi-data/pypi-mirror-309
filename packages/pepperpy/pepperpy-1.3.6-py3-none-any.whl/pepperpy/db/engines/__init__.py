"""Database engines"""

from typing import Any

from ..config import DatabaseConfig
from .base import BaseEngine
from .postgres import PostgresEngine
from .sqlite import SQLiteEngine


def get_engine(config: dict[str, Any]) -> BaseEngine:
    """Get database engine based on configuration"""
    engine_type = config.get("engine", "sqlite")

    # Convert dictionary config to DatabaseConfig object
    db_config = DatabaseConfig(**config)

    if engine_type == "postgres":
        return PostgresEngine(db_config)
    if engine_type == "sqlite":
        return SQLiteEngine(db_config)
    raise ValueError(f"Unsupported database engine: {engine_type}")
