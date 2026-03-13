# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

# oidc.py
"""
OIDC Authenticator for Anaconda Telemetry.

Handles token lifecycle for OIDC client_credentials grant:
fetching, caching, and proactive refresh before expiry.
"""

import json
import threading
import time
import logging
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Optional, List


class OIDCAuthenticator:
    """
    Authenticator that fetches and manages OIDC access tokens using the
    client_credentials grant. Thread-safe for use across multiple exporter threads.

    Args:
        token_endpoint: The OIDC token endpoint URL.
        client_id: OAuth2 client ID.
        client_secret: OAuth2 client secret.
        scopes: Optional list of scopes to request.
        expiry_buffer_seconds: Seconds before actual expiry to trigger a refresh (default 30).
    """

    def __init__(
        self,
        token_endpoint: str,
        client_id: str,
        client_secret: str,
        scopes: Optional[List[str]] = None,
        expiry_buffer_seconds: int = 30,
    ):
        if not token_endpoint:
            raise ValueError("token_endpoint is required")
        if not client_id:
            raise ValueError("client_id is required")
        if not client_secret:
            raise ValueError("client_secret is required")

        self._token_endpoint = token_endpoint
        self._client_id = client_id
        self._client_secret = client_secret
        self._scopes = scopes
        self._expiry_buffer_seconds = expiry_buffer_seconds

        self._lock = threading.Lock()
        self._access_token: Optional[str] = None
        self._expires_at: float = 0.0

        self._logger = logging.getLogger("anaconda_opentelemetry.oidc")

    def get_token(self) -> str:
        """Returns a valid access token, refreshing if necessary."""
        if self._is_token_valid():
            return self._access_token

        with self._lock:
            # Double-check after acquiring lock
            if self._is_token_valid():
                return self._access_token
            return self._refresh()

    def get_headers(self) -> Dict[str, str]:
        """Returns authorization headers with a valid Bearer token."""
        return {"authorization": f"Bearer {self.get_token()}"}

    def force_refresh(self) -> str:
        """Forces a token refresh regardless of expiry."""
        with self._lock:
            return self._refresh()

    def _is_token_valid(self) -> bool:
        return (
            self._access_token is not None
            and time.time() < self._expires_at - self._expiry_buffer_seconds
        )

    def _refresh(self) -> str:
        data = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        if self._scopes:
            data["scope"] = " ".join(self._scopes)

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
            self._logger.error(f"OIDC token request failed with HTTP {e.code}: {e.reason}")
            raise
        except urllib.error.URLError as e:
            self._logger.error(f"OIDC token request failed: {e.reason}")
            raise

        access_token = body.get("access_token")
        if not access_token:
            raise ValueError("OIDC token response missing 'access_token'")

        expires_in = body.get("expires_in")
        if expires_in is not None:
            self._expires_at = time.time() + int(expires_in)
        else:
            # 5 minute expiry
            self._expires_at = time.time() + 300

        self._access_token = access_token
        return self._access_token
