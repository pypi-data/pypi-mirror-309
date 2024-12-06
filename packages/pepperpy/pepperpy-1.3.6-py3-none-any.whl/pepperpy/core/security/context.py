"""Security context management"""


from pepperpy.core.module import BaseModule, ModuleMetadata

from .exceptions import AuthError


class SecurityContext(BaseModule):
    """Manager for security context"""

    def __init__(self):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="security_context",
            version="1.0.0",
            description="Security context management",
            dependencies=[],
            config={},
        )
        self._user_id: str | None = None
        self._roles: list[str] = []
        self._permissions: list[str] = []
        self._metadata: dict[str, str] = {}

    async def _setup(self) -> None:
        """Initialize security context"""

    async def _cleanup(self) -> None:
        """Cleanup security context"""
        self._user_id = None
        self._roles.clear()
        self._permissions.clear()
        self._metadata.clear()

    async def set_user(self, user_id: str) -> None:
        """Set current user"""
        self._user_id = user_id

    async def set_roles(self, roles: list[str]) -> None:
        """Set user roles"""
        self._roles = roles

    async def set_permissions(self, permissions: list[str]) -> None:
        """Set user permissions"""
        self._permissions = permissions

    async def set_metadata(self, metadata: dict[str, str]) -> None:
        """Set security metadata"""
        self._metadata = metadata

    async def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self._user_id is not None

    async def has_role(self, role: str) -> bool:
        """Check if user has role"""
        if not self._user_id:
            raise AuthError("No user in context")
        return role in self._roles

    async def has_permission(self, permission: str) -> bool:
        """Check if user has permission"""
        if not self._user_id:
            raise AuthError("No user in context")
        return permission in self._permissions

    async def get_metadata(self, key: str) -> str | None:
        """Get security metadata"""
        return self._metadata.get(key)


# Global security context instance
security_context = SecurityContext()
