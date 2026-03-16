# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

# oidc.py
"""
OIDC Auth Manager for Anaconda Telemetry.

Standalone OIDC authentication manager supporting client_credentials and
password (ROPC) grant types. The caller is responsible for token lifecycle
(caching, refresh timing).
"""

import json
import time
import logging
import urllib.request
import urllib.parse
import urllib.error
from dataclasses import dataclass
from typing import Optional, List
from urllib.parse import urlparse


class AuthError(Exception):
    """Rich error class for OIDC authentication failures."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        server_error: Optional[str] = None,
        server_error_description: Optional[str] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.server_error = server_error
        self.server_error_description = server_error_description


@dataclass
class TokenSet:
    """Represents a token set returned by the OIDC/OAuth2 provider."""

    access_token: str
    refresh_token: str
    access_token_expires_at: float
    refresh_token_expires_at: Optional[float]
    token_type: str
    scope: Optional[str]


def _validate_token_response(body: dict) -> bool:
    """Validates that a token response has the required fields and correct types."""
    if not isinstance(body, dict):
        return False
    if not isinstance(body.get("access_token"), str):
        return False
    if not isinstance(body.get("refresh_token"), str):
        return False
    if not isinstance(body.get("token_type"), str):
        return False
    expires_in = body.get("expires_in")
    if not isinstance(expires_in, (int, float)) or expires_in <= 0:
        return False
    refresh_expires_in = body.get("refresh_expires_in")
    if refresh_expires_in is not None:
        if not isinstance(refresh_expires_in, (int, float)) or refresh_expires_in <= 0:
            return False
    scope = body.get("scope")
    if scope is not None and not isinstance(scope, str):
        return False
    return True


def _validate_client_credentials_response(body: dict) -> bool:
    """Validates a client_credentials token response (refresh_token not required)."""
    if not isinstance(body, dict):
        return False
    if not isinstance(body.get("access_token"), str):
        return False
    expires_in = body.get("expires_in")
    if not isinstance(expires_in, (int, float)) or expires_in <= 0:
        return False
    token_type = body.get("token_type")
    if token_type is not None and not isinstance(token_type, str):
        return False
    refresh_expires_in = body.get("refresh_expires_in")
    if refresh_expires_in is not None:
        if not isinstance(refresh_expires_in, (int, float)) or refresh_expires_in <= 0:
            return False
    scope = body.get("scope")
    if scope is not None and not isinstance(scope, str):
        return False
    return True


class OIDCAuthenticator:
    """
    OIDC authenticator supporting client_credentials and password grants.

    Each method call makes a network request and returns a fresh TokenSet.
    The caller is responsible for caching tokens and deciding when to refresh.

    Args:
        token_endpoint: The OIDC token endpoint URL (must be http or https).
        client_id: OAuth2 client ID.
        client_secret: OAuth2 client secret (optional for public clients in password grant).
        scopes: Optional list of scopes to request.
    """

    def __init__(
        self,
        token_endpoint: str,
        client_id: str,
        client_secret: Optional[str] = None,
        scopes: Optional[List[str]] = None,
    ):
        if not token_endpoint:
            raise ValueError("token_endpoint is required")

        parsed = urlparse(token_endpoint)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("token_endpoint must use http or https scheme")

        if not client_id:
            raise ValueError("client_id is required")

        if client_secret is not None and not client_secret:
            raise ValueError("client_secret cannot be empty when provided")

        self._token_endpoint = token_endpoint
        self._client_id = client_id
        self._client_secret = client_secret
        self._scopes = scopes

        self._logger = logging.getLogger("anaconda_opentelemetry.oidc")

    def authenticate(self, username: str, password: str) -> TokenSet:
        """
        Authenticates using the Resource Owner Password Credentials (ROPC) grant.

        Args:
            username: The user's username.
            password: The user's password.

        Returns:
            A TokenSet containing access and refresh tokens.

        Raises:
            AuthError: If the server rejects the credentials or returns an error.
        """
        data = {
            "grant_type": "password",
            "client_id": self._client_id,
            "username": username,
            "password": password,
        }

        if self._scopes:
            data["scope"] = " ".join(self._scopes)

        if self._client_secret:
            data["client_secret"] = self._client_secret

        return self._request_tokens(data)

    def client_credentials_grant(self) -> TokenSet:
        """
        Obtains tokens using the client_credentials grant (machine-to-machine).

        Requires client_secret to be set.

        Returns:
            A TokenSet containing the access token (refresh_token may be empty).

        Raises:
            AuthError: If the server rejects the credentials or returns an error.
            ValueError: If client_secret is not set.
        """
        if not self._client_secret:
            raise ValueError("client_secret is required for client_credentials grant")

        data = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }

        if self._scopes:
            data["scope"] = " ".join(self._scopes)

        return self._request_tokens(data, is_client_credentials=True)

    def refresh_token(self, current_tokens: TokenSet) -> TokenSet:
        """
        Obtains a fresh TokenSet by exchanging a refresh token.

        Checks refresh token expiry locally before making a network call.

        Args:
            current_tokens: The current TokenSet containing the refresh token.

        Returns:
            A fresh TokenSet.

        Raises:
            AuthError: If the refresh token has expired or is rejected by the server.
        """
        if (
            current_tokens.refresh_token_expires_at is not None
            and current_tokens.refresh_token_expires_at <= time.time()
        ):
            raise AuthError(
                "Refresh token has expired.",
                server_error="invalid_grant",
                server_error_description="The refresh token has expired.",
            )

        data = {
            "grant_type": "refresh_token",
            "client_id": self._client_id,
            "refresh_token": current_tokens.refresh_token,
        }

        if self._scopes:
            data["scope"] = " ".join(self._scopes)

        if self._client_secret:
            data["client_secret"] = self._client_secret

        return self._request_tokens(data)

    def _request_tokens(self, data: dict, is_client_credentials: bool = False) -> TokenSet:
        """Makes a token request and returns a parsed TokenSet."""
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(
            self._token_endpoint,
            data=encoded_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            try:
                error_body = json.loads(e.read().decode("utf-8"))
            except Exception:
                error_body = {}

            server_error = error_body.get("error") if isinstance(error_body, dict) else None
            description = error_body.get("error_description") if isinstance(error_body, dict) else None

            message = f"Authentication failed (HTTP {e.code})"
            if server_error:
                message += f": {server_error}"

            raise AuthError(
                message,
                status_code=e.code,
                server_error=server_error,
                server_error_description=description,
            ) from e
        except urllib.error.URLError as e:
            raise AuthError(
                f"Network request to token endpoint failed: {e.reason}"
            ) from e

        if is_client_credentials:
            if not _validate_client_credentials_response(body):
                raise AuthError(
                    "Token endpoint returned invalid response structure.",
                )
        else:
            if not _validate_token_response(body):
                raise AuthError(
                    "Token endpoint returned invalid response structure.",
                )

        return self._parse_token_response(body)

    @staticmethod
    def _parse_token_response(body: dict) -> TokenSet:
        """Parses a raw token response dict into a TokenSet."""
        now = time.time()

        access_token_expires_at = now + body["expires_in"]

        refresh_expires_in = body.get("refresh_expires_in")
        refresh_token_expires_at = (
            now + refresh_expires_in
            if isinstance(refresh_expires_in, (int, float)) and refresh_expires_in > 0
            else None
        )

        return TokenSet(
            access_token=body["access_token"],
            refresh_token=body.get("refresh_token", ""),
            token_type=body.get("token_type", "Bearer"),
            access_token_expires_at=access_token_expires_at,
            refresh_token_expires_at=refresh_token_expires_at,
            scope=body.get("scope"),
        )
