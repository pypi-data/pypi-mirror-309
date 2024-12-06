"""Metrics configuration"""

from dataclasses import asdict, dataclass
from typing import Any

from pepperpy.core.config import ModuleConfig


@dataclass
class MetricsConfig(ModuleConfig):
    """Configuration for metrics collection"""

    enabled: bool = True
    interval: int = 60  # Intervalo de coleta em segundos
    batch_size: int = 100  # Tamanho do lote para processamento
    storage_path: str | None = None  # Caminho para armazenamento
    max_samples: int = 1000  # Número máximo de amostras
    retention_days: int = 30  # Dias para retenção dos dados

    def dict(self) -> dict[str, Any]:
        """Convert config to dictionary"""
        return asdict(self)
