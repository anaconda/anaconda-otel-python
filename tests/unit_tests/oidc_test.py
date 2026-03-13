# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

import sys
sys.path.append("./")

import pytest, json, threading, time
from unittest.mock import patch, MagicMock, Mock

from anaconda_opentelemetry.oidc import OIDCAuthenticator


class TestOIDCAuthenticatorInit:
    def test_valid_initialization(self):
        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        assert auth._token_endpoint == "https://idp.example.com/oauth/token"
        assert auth._client_id == "my-client"
        assert auth._client_secret == "my-secret"
        assert auth._scopes is None
        assert auth._expiry_buffer_seconds == 30
        assert auth._access_token is None
        assert auth._expires_at == 0.0

    def test_initialization_with_scopes(self):
        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
            scopes=["openid", "telemetry"],
        )

        assert auth._scopes == ["openid", "telemetry"]

    def test_initialization_with_custom_expiry_buffer(self):
        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
            expiry_buffer_seconds=60,
        )

        assert auth._expiry_buffer_seconds == 60

    def test_missing_token_endpoint_raises(self):
        with pytest.raises(ValueError, match="token_endpoint is required"):
            OIDCAuthenticator(
                token_endpoint="",
                client_id="my-client",
                client_secret="my-secret",
            )

    def test_missing_client_id_raises(self):
        with pytest.raises(ValueError, match="client_id is required"):
            OIDCAuthenticator(
                token_endpoint="https://idp.example.com/oauth/token",
                client_id="",
                client_secret="my-secret",
            )

    def test_missing_client_secret_raises(self):
        with pytest.raises(ValueError, match="client_secret is required"):
            OIDCAuthenticator(
                token_endpoint="https://idp.example.com/oauth/token",
                client_id="my-client",
                client_secret="",
            )


class TestOIDCAuthenticatorTokenValidity:
    def test_no_token_is_invalid(self):
        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="id",
            client_secret="secret",
        )

        assert auth._is_token_valid() == False

    def test_expired_token_is_invalid(self):
        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="id",
            client_secret="secret",
            expiry_buffer_seconds=30,
        )
        auth._access_token = "some-token"
        auth._expires_at = time.time() - 10

        assert auth._is_token_valid() == False

    def test_token_within_buffer_is_invalid(self):
        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="id",
            client_secret="secret",
            expiry_buffer_seconds=30,
        )
        auth._access_token = "some-token"
        auth._expires_at = time.time() + 20

        assert auth._is_token_valid() == False

    def test_token_outside_buffer_is_valid(self):
        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="id",
            client_secret="secret",
            expiry_buffer_seconds=30,
        )
        auth._access_token = "some-token"
        auth._expires_at = time.time() + 60

        assert auth._is_token_valid() == True


def _make_mock_response(body, status=200):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(body).encode("utf-8")
    mock_response.__enter__ = Mock(return_value=mock_response)
    mock_response.__exit__ = Mock(return_value=False)
    return mock_response


class TestOIDCAuthenticatorGetToken:
    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_fetches_token_on_first_call(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "fresh-token",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        token = auth.get_token()

        assert token == "fresh-token"
        assert auth._access_token == "fresh-token"
        mock_urlopen.assert_called_once()

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_returns_cached_token_when_valid(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "cached-token",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        token1 = auth.get_token()
        token2 = auth.get_token()

        assert token1 == token2 == "cached-token"
        assert mock_urlopen.call_count == 1

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_refreshes_when_token_expired(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "new-token",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
            expiry_buffer_seconds=30,
        )

        # Simulate an expired cached token
        auth._access_token = "old-token"
        auth._expires_at = time.time() - 10

        token = auth.get_token()

        assert token == "new-token"
        mock_urlopen.assert_called_once()

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_defaults_expiry_when_missing_expires_in(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "no-expiry-token",
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        before = time.time()
        auth.get_token()
        after = time.time()

        # Should default to 300s (5 minutes)
        assert auth._expires_at >= before + 300
        assert auth._expires_at <= after + 300


class TestOIDCAuthenticatorGetHeaders:
    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_returns_bearer_headers(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "header-token",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        headers = auth.get_headers()

        assert headers == {"authorization": "Bearer header-token"}


class TestOIDCAuthenticatorForceRefresh:
    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_force_refresh_fetches_new_token(self, mock_urlopen):
        responses = [
            _make_mock_response({"access_token": "token-1", "expires_in": 3600}),
            _make_mock_response({"access_token": "token-2", "expires_in": 3600}),
        ]
        mock_urlopen.side_effect = responses

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        token1 = auth.get_token()
        token2 = auth.force_refresh()

        assert token1 == "token-1"
        assert token2 == "token-2"
        assert mock_urlopen.call_count == 2


class TestOIDCAuthenticatorRequestFormat:
    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_sends_correct_request_without_scopes(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "tok",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )
        auth.get_token()

        request = mock_urlopen.call_args[0][0]
        assert request.full_url == "https://idp.example.com/oauth/token"
        assert request.get_method() == "POST"
        assert request.get_header("Content-type") == "application/x-www-form-urlencoded"

        body = request.data.decode("utf-8")
        assert "grant_type=client_credentials" in body
        assert "client_id=my-client" in body
        assert "client_secret=my-secret" in body
        assert "scope" not in body

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_sends_correct_request_with_scopes(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "tok",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
            scopes=["openid", "telemetry"],
        )
        auth.get_token()

        body = mock_urlopen.call_args[0][0].data.decode("utf-8")
        assert "scope=openid+telemetry" in body


class TestOIDCAuthenticatorErrorHandling:
    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_http_error_raises(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://idp.example.com/oauth/token",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=None,
        )

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        with pytest.raises(urllib.error.HTTPError):
            auth.get_token()

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_url_error_raises(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        with pytest.raises(urllib.error.URLError):
            auth.get_token()

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_missing_access_token_in_response_raises(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "token_type": "Bearer",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        with pytest.raises(ValueError, match="missing 'access_token'"):
            auth.get_token()


class TestOIDCAuthenticatorThreadSafety:
    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_concurrent_get_token_calls(self, mock_urlopen):
        call_count = [0]
        original_lock = threading.Lock()

        def slow_urlopen(req):
            with original_lock:
                call_count[0] += 1
            time.sleep(0.05)
            return _make_mock_response({
                "access_token": "concurrent-token",
                "expires_in": 3600,
            })

        mock_urlopen.side_effect = slow_urlopen

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        results = []
        errors = []

        def fetch_token():
            try:
                token = auth.get_token()
                results.append(token)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=fetch_token) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
        assert all(r == "concurrent-token" for r in results)
        assert len(results) == 10
        assert call_count[0] <= 2

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_concurrent_force_refresh(self, mock_urlopen):
        token_counter = [0]

        def sequential_urlopen(req):
            token_counter[0] += 1
            return _make_mock_response({
                "access_token": f"token-{token_counter[0]}",
                "expires_in": 3600,
            })

        mock_urlopen.side_effect = sequential_urlopen

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        results = []

        def refresh():
            results.append(auth.force_refresh())

        threads = [threading.Thread(target=refresh) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 5
        assert mock_urlopen.call_count == 5
