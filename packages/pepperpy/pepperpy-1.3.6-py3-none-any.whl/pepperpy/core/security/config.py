"""Security configuration"""

from dataclasses import dataclass, field


@dataclass
class SecurityConfig:
    """Security configuration"""

    secret_key: str
    algorithm: str = "HS256"
    token_expiration: int = 3600  # 1 hour
    password_min_length: int = 8
    password_require_numbers: bool = True
    password_require_special: bool = True
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class AuthConfig:
    """Authentication configuration"""

    enabled: bool = True
    allow_registration: bool = True
    require_email_verification: bool = False
    max_login_attempts: int = 3
    lockout_duration: int = 300  # 5 minutes
    session_duration: int = 86400  # 24 hours
    metadata: dict[str, str] = field(default_factory=dict)
