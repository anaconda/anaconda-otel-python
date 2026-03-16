# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

import sys
sys.path.append("./")

import pytest, json, time
from unittest.mock import patch, MagicMock, Mock

from anaconda_opentelemetry.oidc import OIDCAuthenticator, TokenSet, AuthError, _validate_token_response, _validate_client_credentials_response


def _make_mock_response(body, status=200):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(body).encode("utf-8")
    mock_response.__enter__ = Mock(return_value=mock_response)
    mock_response.__exit__ = Mock(return_value=False)
    return mock_response


def _make_mock_http_error(code, body=None):
    import urllib.error
    error = urllib.error.HTTPError(
        url="https://idp.example.com/oauth/token",
        code=code,
        msg="Error",
        hdrs={},
        fp=None,
    )
    error.read = Mock(return_value=json.dumps(body or {}).encode("utf-8"))
    return error


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

    def test_initialization_with_scopes(self):
        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
            scopes=["openid", "telemetry"],
        )

        assert auth._scopes == ["openid", "telemetry"]

    def test_initialization_without_client_secret(self):
        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
        )

        assert auth._client_secret is None

    def test_missing_token_endpoint_raises(self):
        with pytest.raises(ValueError, match="token_endpoint is required"):
            OIDCAuthenticator(
                token_endpoint="",
                client_id="my-client",
            )

    def test_invalid_token_endpoint_scheme_raises(self):
        with pytest.raises(ValueError, match="http or https scheme"):
            OIDCAuthenticator(
                token_endpoint="ftp://idp.example.com/oauth/token",
                client_id="my-client",
            )

    def test_missing_client_id_raises(self):
        with pytest.raises(ValueError, match="client_id is required"):
            OIDCAuthenticator(
                token_endpoint="https://idp.example.com/oauth/token",
                client_id="",
            )

    def test_empty_client_secret_raises(self):
        with pytest.raises(ValueError, match="client_secret cannot be empty"):
            OIDCAuthenticator(
                token_endpoint="https://idp.example.com/oauth/token",
                client_id="my-client",
                client_secret="",
            )


class TestClientCredentialsGrant:
    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_successful_client_credentials(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "cc-token",
            "refresh_token": "",
            "token_type": "Bearer",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        token_set = auth.client_credentials_grant()

        assert isinstance(token_set, TokenSet)
        assert token_set.access_token == "cc-token"
        assert token_set.token_type == "Bearer"
        assert token_set.access_token_expires_at > time.time()

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_sends_correct_request_without_scopes(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "tok",
            "token_type": "Bearer",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )
        auth.client_credentials_grant()

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
            "token_type": "Bearer",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
            scopes=["openid", "telemetry"],
        )
        auth.client_credentials_grant()

        body = mock_urlopen.call_args[0][0].data.decode("utf-8")
        assert "scope=openid+telemetry" in body

    def test_requires_client_secret(self):
        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
        )

        with pytest.raises(ValueError, match="client_secret is required"):
            auth.client_credentials_grant()

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_client_credentials_no_refresh_token_in_response(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "cc-token",
            "token_type": "Bearer",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        token_set = auth.client_credentials_grant()
        assert token_set.access_token == "cc-token"
        assert token_set.refresh_token == ""


class TestAuthenticate:
    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_successful_password_grant(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "user-token",
            "refresh_token": "refresh-tok",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_expires_in": 86400,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
        )

        token_set = auth.authenticate("user", "pass")

        assert token_set.access_token == "user-token"
        assert token_set.refresh_token == "refresh-tok"
        assert token_set.refresh_token_expires_at is not None

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_sends_correct_password_grant_request(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "tok",
            "refresh_token": "ref",
            "token_type": "Bearer",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
            scopes=["openid"],
        )
        auth.authenticate("myuser", "mypass")

        body = mock_urlopen.call_args[0][0].data.decode("utf-8")
        assert "grant_type=password" in body
        assert "username=myuser" in body
        assert "password=mypass" in body
        assert "client_id=my-client" in body
        assert "client_secret=my-secret" in body
        assert "scope=openid" in body

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_password_grant_without_client_secret(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "tok",
            "refresh_token": "ref",
            "token_type": "Bearer",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
        )
        auth.authenticate("user", "pass")

        body = mock_urlopen.call_args[0][0].data.decode("utf-8")
        assert "client_secret" not in body


class TestRefreshToken:
    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_successful_refresh(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "new-token",
            "refresh_token": "new-refresh",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_expires_in": 86400,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        current = TokenSet(
            access_token="old",
            refresh_token="old-refresh",
            access_token_expires_at=time.time() - 10,
            refresh_token_expires_at=time.time() + 86400,
            token_type="Bearer",
            scope=None,
        )

        token_set = auth.refresh_token(current)
        assert token_set.access_token == "new-token"
        assert token_set.refresh_token == "new-refresh"

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_sends_correct_refresh_request(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "tok",
            "refresh_token": "ref",
            "token_type": "Bearer",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
            scopes=["openid"],
        )

        current = TokenSet(
            access_token="old",
            refresh_token="the-refresh-token",
            access_token_expires_at=time.time() + 100,
            refresh_token_expires_at=time.time() + 86400,
            token_type="Bearer",
            scope=None,
        )

        auth.refresh_token(current)

        body = mock_urlopen.call_args[0][0].data.decode("utf-8")
        assert "grant_type=refresh_token" in body
        assert "refresh_token=the-refresh-token" in body
        assert "client_id=my-client" in body
        assert "client_secret=my-secret" in body
        assert "scope=openid" in body

    def test_expired_refresh_token_raises_locally(self):
        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
        )

        current = TokenSet(
            access_token="old",
            refresh_token="expired-refresh",
            access_token_expires_at=time.time() - 100,
            refresh_token_expires_at=time.time() - 10,
            token_type="Bearer",
            scope=None,
        )

        with pytest.raises(AuthError, match="Refresh token has expired"):
            auth.refresh_token(current)

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_none_refresh_expiry_skips_local_check(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "tok",
            "refresh_token": "ref",
            "token_type": "Bearer",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
        )

        current = TokenSet(
            access_token="old",
            refresh_token="ref",
            access_token_expires_at=time.time() - 100,
            refresh_token_expires_at=None,
            token_type="Bearer",
            scope=None,
        )

        token_set = auth.refresh_token(current)
        assert token_set.access_token == "tok"


class TestTokenSetParsing:
    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_all_fields_mapped(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "at",
            "refresh_token": "rt",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_expires_in": 86400,
            "scope": "openid profile",
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
        )

        before = time.time()
        ts = auth.authenticate("u", "p")
        after = time.time()

        assert ts.access_token == "at"
        assert ts.refresh_token == "rt"
        assert ts.token_type == "Bearer"
        assert ts.scope == "openid profile"
        assert before + 3600 <= ts.access_token_expires_at <= after + 3600
        assert before + 86400 <= ts.refresh_token_expires_at <= after + 86400

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_no_refresh_expires_in(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "access_token": "at",
            "refresh_token": "rt",
            "token_type": "Bearer",
            "expires_in": 3600,
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
        )

        ts = auth.authenticate("u", "p")
        assert ts.refresh_token_expires_at is None


class TestResponseValidation:
    def test_valid_full_response(self):
        assert _validate_token_response({
            "access_token": "at",
            "refresh_token": "rt",
            "token_type": "Bearer",
            "expires_in": 3600,
        }) is True

    def test_missing_access_token(self):
        assert _validate_token_response({
            "refresh_token": "rt",
            "token_type": "Bearer",
            "expires_in": 3600,
        }) is False

    def test_missing_refresh_token(self):
        assert _validate_token_response({
            "access_token": "at",
            "token_type": "Bearer",
            "expires_in": 3600,
        }) is False

    def test_missing_expires_in(self):
        assert _validate_token_response({
            "access_token": "at",
            "refresh_token": "rt",
            "token_type": "Bearer",
        }) is False

    def test_invalid_expires_in(self):
        assert _validate_token_response({
            "access_token": "at",
            "refresh_token": "rt",
            "token_type": "Bearer",
            "expires_in": -1,
        }) is False

    def test_invalid_refresh_expires_in(self):
        assert _validate_token_response({
            "access_token": "at",
            "refresh_token": "rt",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_expires_in": -1,
        }) is False

    def test_not_a_dict(self):
        assert _validate_token_response("not a dict") is False

    def test_valid_client_credentials_response(self):
        assert _validate_client_credentials_response({
            "access_token": "at",
            "token_type": "Bearer",
            "expires_in": 3600,
        }) is True

    def test_client_credentials_missing_access_token(self):
        assert _validate_client_credentials_response({
            "token_type": "Bearer",
            "expires_in": 3600,
        }) is False


class TestErrorHandling:
    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_http_error_raises_auth_error(self, mock_urlopen):
        mock_urlopen.side_effect = _make_mock_http_error(401, {
            "error": "invalid_client",
            "error_description": "Bad credentials",
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        with pytest.raises(AuthError) as exc_info:
            auth.client_credentials_grant()

        assert exc_info.value.status_code == 401
        assert exc_info.value.server_error == "invalid_client"
        assert exc_info.value.server_error_description == "Bad credentials"

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_url_error_raises_auth_error(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        with pytest.raises(AuthError, match="Network request to token endpoint failed"):
            auth.client_credentials_grant()

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_invalid_response_structure_raises_auth_error(self, mock_urlopen):
        mock_urlopen.return_value = _make_mock_response({
            "token_type": "Bearer",
        })

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        with pytest.raises(AuthError, match="invalid response structure"):
            auth.client_credentials_grant()

    @patch("anaconda_opentelemetry.oidc.urllib.request.urlopen")
    def test_http_error_with_non_json_body(self, mock_urlopen):
        import urllib.error
        error = urllib.error.HTTPError(
            url="https://idp.example.com/oauth/token",
            code=500,
            msg="Server Error",
            hdrs={},
            fp=None,
        )
        error.read = Mock(return_value=b"not json")
        mock_urlopen.side_effect = error

        auth = OIDCAuthenticator(
            token_endpoint="https://idp.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
        )

        with pytest.raises(AuthError) as exc_info:
            auth.client_credentials_grant()

        assert exc_info.value.status_code == 500
        assert exc_info.value.server_error is None
