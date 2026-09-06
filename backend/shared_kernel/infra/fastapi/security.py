"""Define security utilities for FastAPI."""
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

access_token_scheme = HTTPBearer(
    scheme_name="AccessToken",
    bearerFormat="JWT",
    description="Paste your access token here, without the 'Bearer' prefix. Example: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'"
)

def get_access_token_scheme(
        credentials: Annotated[
            HTTPAuthorizationCredentials,
            Depends(access_token_scheme)
            ]
) -> HTTPBearer:
    """Get the access token scheme for FastAPI security."""
    return credentials.credentials