""""Define the Authentication Service interface for user authentication and session management."""

class IAuthenticationService:
    """Authentication Service interface for user authentication and session management."""

    async def login_by_username(
        self, username: str, password: str, ip_address: str | None = None, user_agent: str | None = None
    ) -> dict:
        """Authenticate a user and return a token pair (access and refresh tokens)."""
        ...

    async def logout(self, session_id: str) -> None:
        """Logout a user by revoking the session and associated tokens."""
        ...