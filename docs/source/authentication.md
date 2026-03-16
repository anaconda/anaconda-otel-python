# Authentication

There are two ways to authenticate with a telemetry collector via this package: a static API token or OIDC.

## Static Token

Pass a token string directly to `Configuration`. The token is fixed for the lifetime of the process.

```python
from anaconda_opentelemetry import Configuration

cfg = Configuration(
    default_endpoint="https://collector.example.com:4317",
    default_auth_token="your-api-token"
)
```

Or via environment variable:

```bash
export ATEL_DEFAULT_AUTH_TOKEN=your-api-token
```

Per-signal tokens can also be set:

```python
cfg.set_auth_token_metrics("metrics-token")
cfg.set_auth_token_logging("logging-token")
cfg.set_auth_token_tracing("tracing-token")
```

## OIDC Authentication

Use `OIDCAuthenticator` for token fetching via OAuth2. It supports two grant types: `client_credentials` (machine-to-machine) and `password` (Resource Owner Password Credentials). The authenticator is stateless — each call makes a network request and returns a fresh `TokenSet`. The caller is responsible for caching tokens and deciding when to refresh.

```python
from anaconda_opentelemetry import OIDCAuthenticator, TokenSet
```

### Constructor

```python
auth = OIDCAuthenticator(
    token_endpoint="https://idp.example.com/oauth/token",
    client_id="my-client",
    client_secret="my-secret",  # optional for password grant
    scopes=["openid"],          # optional
)
```

- `token_endpoint` must use `http` or `https` scheme.
- `client_secret` is required for `client_credentials` grant but optional for `password` grant (public clients).

### Client Credentials Grant

For machine-to-machine authentication. Requires `client_secret`.

```python
token_set = auth.client_credentials_grant()
token = token_set.access_token
```

### Password Grant (ROPC)

For user-facing authentication with username and password.

```python
token_set = auth.authenticate("username", "password")
token = token_set.access_token
```

### Refreshing Tokens

Exchange a refresh token for a new `TokenSet`. Checks refresh token expiry locally before making a network call.

```python
new_token_set = auth.refresh_token(token_set)
```

### TokenSet

All grant methods return a `TokenSet` dataclass:

| Field | Type | Description |
|---|---|---|
| `access_token` | `str` | The access token |
| `refresh_token` | `str` | The refresh token (empty string if not provided) |
| `access_token_expires_at` | `float` | Absolute timestamp when the access token expires |
| `refresh_token_expires_at` | `float \| None` | Absolute timestamp when the refresh token expires |
| `token_type` | `str` | Token type (e.g. `"Bearer"`) |
| `scope` | `str \| None` | Granted scopes |

### Error Handling

All methods raise `AuthError` on failure, which includes structured error details:

```python
from anaconda_opentelemetry import AuthError

try:
    token_set = auth.client_credentials_grant()
except AuthError as e:
    print(e.status_code)               # HTTP status code (if applicable)
    print(e.server_error)              # OAuth2 error code (e.g. "invalid_client")
    print(e.server_error_description)  # Human-readable description from server
```

### Example: Using with Configuration

```python
from anaconda_opentelemetry import Configuration, OIDCAuthenticator

auth = OIDCAuthenticator(
    token_endpoint="https://idp.example.com/oauth/token",
    client_id="my-client",
    client_secret="my-secret",
)

token_set = auth.client_credentials_grant()

cfg = Configuration(
    default_endpoint="https://collector.example.com:4317",
    default_auth_token=token_set.access_token,
)
```

### Rotating Tokens After Initialization

> **Important:** After `initialize_telemetry()` has been called, updating the `Configuration` object will **not** update the token used by active exporters. You must use `change_signal_endpoint` from `signals` to rotate the token on a live exporter.

```python
from anaconda_opentelemetry import change_signal_endpoint

# Fetch a fresh token
new_token_set = auth.client_credentials_grant()

# Update each signal's exporter with the new token
change_signal_endpoint("metrics", "https://collector.example.com:4317", auth_token=new_token_set.access_token)
change_signal_endpoint("tracing", "https://collector.example.com:4317", auth_token=new_token_set.access_token)
change_signal_endpoint("logging", "https://collector.example.com:4317", auth_token=new_token_set.access_token)
```

This recreates the underlying exporter with the new token. The endpoint can remain the same — only the `auth_token` needs to change.
