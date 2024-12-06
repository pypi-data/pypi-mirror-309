"""Authentication and authorization implementation"""

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

import jwt
from jwt.exceptions import PyJWTError

from pepperpy.core.module import BaseModule, ModuleMetadata

from .exceptions import AuthError, SecurityError


@dataclass
class AuthToken:
    """Authentication token data"""

    token: str
    expires_at: datetime
    user_id: str
    metadata: dict[str, str]


class JWTHandler:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(
        self, data: dict[str, Any], expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except PyJWTError as e:
            raise SecurityError(f"Invalid token: {e!s}")


class AuthManager(BaseModule):
    """Manager for authentication and authorization"""

    def __init__(self):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="auth",
            version="1.0.0",
            description="Authentication and authorization",
            dependencies=[],
            config={},
        )
        self._secret = secrets.token_hex(32)
        self._tokens = {}
        self.jwt_handler = JWTHandler(self._secret)

    async def _setup(self) -> None:
        """Initialize auth manager"""

    async def _cleanup(self) -> None:
        """Cleanup auth resources"""
        self._tokens.clear()
        self._secret = secrets.token_hex(32)

    def _generate_salt(self) -> str:
        """Generate random salt"""
        return secrets.token_hex(16)

    def _hash_password(self, password: str, salt: str) -> str:
        """Hash password with salt"""
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 100000, dklen=32,
        ).hex()

    async def register(self, user_id: str, password: str) -> None:
        """Register new user"""
        try:
            salt = self._generate_salt()
            password_hash = self._hash_password(password, salt)

            # Store user credentials (in a real system, this would go to a database)
            self._tokens[user_id] = {"salt": salt, "password_hash": password_hash}

        except Exception as e:
            raise AuthError(f"Registration failed: {e!s}", cause=e)

    async def authenticate(self, user_id: str, password: str) -> AuthToken:
        """Authenticate user and generate token"""
        try:
            if user_id not in self._tokens:
                raise AuthError("User not found")

            stored = self._tokens[user_id]
            password_hash = self._hash_password(password, stored["salt"])

            if not hmac.compare_digest(password_hash, stored["password_hash"]):
                raise AuthError("Invalid password")

            # Generate JWT token
            expires_at = datetime.utcnow() + timedelta(hours=24)
            token = self.jwt_handler.create_access_token(
                {"user_id": user_id},
                expires_delta=timedelta(hours=24),
            )

            return AuthToken(token=token, expires_at=expires_at, user_id=user_id, metadata={})

        except AuthError:
            raise
        except Exception as e:
            raise AuthError(f"Authentication failed: {e!s}", cause=e)

    async def verify_token(self, token: str) -> str | None:
        """Verify authentication token"""
        try:
            payload = self.jwt_handler.decode(token)
            return payload.get("user_id")
        except PyJWTError as e:
            raise SecurityError(f"Invalid token: {e!s}")
        except Exception as e:
            raise SecurityError(f"Token verification failed: {e!s}", cause=e)


# Global auth manager instance
auth = AuthManager()
