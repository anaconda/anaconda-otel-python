# Authentication

There are two ways to authenticate with a telemetry collector via this package: a static API token or OIDC client credentials.

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

## OIDC Client Credentials

Use `OIDCAuthenticator` for automatic token fetching and refresh via the OAuth2 `client_credentials` grant. Tokens are cached in memory and refreshed before expiry.

```python
from anaconda_opentelemetry import Configuration
from anaconda_opentelemetry.oidc import OIDCAuthenticator

auth = OIDCAuthenticator(
    token_endpoint="https://idp.example.com/oauth/token",
    client_id="my-client",
    client_secret="my-secret",
    scopes=["openid"],           # optional
    expiry_buffer_seconds=30     # refresh 30s before expiry (default)
)

cfg = Configuration(
    default_endpoint="https://collector.example.com:4317",
    default_auth_token=auth.get_token()
)
```

The authenticator is thread-safe. Key methods:

| Method | Description |
|---|---|
| `get_token()` | Returns a valid token, refreshing automatically if needed |
| `get_headers()` | Returns `{'authorization': 'Bearer <token>'}` |
| `force_refresh()` | Forces a new token fetch regardless of expiry |

### Token Refresh

`get_token()` handles refresh automatically. It returns the cached token when still valid and fetches a new one when the token is within `expiry_buffer_seconds` of expiry. No manual intervention is needed for typical use.

```python
# Each call returns a valid token, refreshing transparently if needed
token = auth.get_token()
```

To force a refresh regardless of expiry (e.g. after receiving a 401 from the collector):

```python
new_token = auth.force_refresh()
```