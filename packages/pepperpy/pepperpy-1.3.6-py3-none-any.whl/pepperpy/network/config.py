"""Network configuration"""

from dataclasses import dataclass, field
from ssl import SSLContext


@dataclass
class NetworkConfig:
    """Network client configuration"""

    timeout: float = 30.0
    connect_timeout: float = 10.0
    max_retries: int = 3
    retry_backoff: float = 1.0
    verify_ssl: bool = True
    cert_path: str | None = None
    max_connections: int = 100
    dns_cache_ttl: int = 10
    default_headers: dict[str, str] = field(default_factory=dict)
    ssl_context: SSLContext | None = None
