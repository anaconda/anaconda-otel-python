import base64
import datetime as dt
import json
import re
import uuid
from os import mkdir
from os.path import exists, join
import pytest
from anaconda_opentelemetry.anon_usage import tokens, utils


try:
    import anaconda_auth
except ImportError:
    anaconda_auth = None


@pytest.fixture
def aau_token_path(monkeypatch, tmp_path):
    monkeypatch.setattr(tokens, "CONFIG_DIR", str(tmp_path))
    return str(tmp_path / "aau_token")


@pytest.fixture(autouse=True)
def client_token_string_cache_cleanup(request):
    request.addfinalizer(utils._cache_clear)


def test_client_token(aau_token_path):
    assert not exists(aau_token_path)
    assert tokens.client_token() != ""
    assert exists(aau_token_path)


def test_client_token_no_nodeid(aau_token_path, monkeypatch):
    monkeypatch.setattr("anaconda_opentelemetry.anon_usage.utils._get_node_str", lambda: None)
    node_path = aau_token_path + "_host"
    assert not exists(aau_token_path) and not exists(node_path)
    token1 = tokens.client_token()
    assert token1 != "" and exists(aau_token_path)
    with open(aau_token_path) as fp:
        token2 = fp.read()
    assert token1 == token2, (token1, token2)
    with open(node_path) as fp:
        saved_node = fp.read()
    assert not saved_node, saved_node


def test_client_token_add_hostid(aau_token_path):
    node_path = aau_token_path + "_host"
    assert not exists(aau_token_path) and not exists(node_path)
    token1 = utils._random_token()
    with open(aau_token_path, "w") as fp:
        fp.write(token1)
    token2 = tokens.client_token()
    assert token1 == token2
    with open(aau_token_path) as fp:
        token3 = fp.read()
    with open(node_path) as fp:
        saved_node = fp.read()
    assert token3 == token2, (token2, token3)
    assert saved_node == utils._get_node_str(), saved_node
    utils._cache_clear()
    token4 = tokens.client_token()
    assert token4 == token2, (token2, token4)


def test_client_token_replace_hostid(aau_token_path):
    node_path = aau_token_path + "_host"
    assert not exists(aau_token_path) and not exists(node_path)
    token1 = utils._random_token()
    with open(aau_token_path, "w") as fp:
        fp.write(token1)
    with open(node_path, "w") as fp:
        fp.write("xxxxxxxx")
    token2 = tokens.client_token()
    assert token1 != token2
    with open(aau_token_path) as fp:
        token3 = fp.read()
    with open(node_path) as fp:
        saved_node = fp.read()
    assert token3 == token2, (token2, token3)
    assert saved_node == utils._get_node_str(), saved_node
    utils._cache_clear()
    token4 = tokens.client_token()
    assert token4 == token2, (token2, token4)


def test_client_token_migrate_hostid(aau_token_path):
    node_path = aau_token_path + "_host"
    assert not exists(aau_token_path) and not exists(node_path)
    token1 = utils._random_token()
    with open(aau_token_path, "w") as fp:
        fp.write(token1 + " " + utils._get_node_str())
    token2 = tokens.client_token()
    assert token1 == token2
    with open(aau_token_path) as fp:
        token3 = fp.read()
    with open(node_path) as fp:
        saved_node = fp.read()
    assert token3 == token2, (token2, token3)
    assert saved_node == utils._get_node_str(), saved_node
    utils._cache_clear()
    token4 = tokens.client_token()
    assert token4 == token2, (token2, token4)


def test_session_token():
    token = tokens.session_token()
    assert token != ""
    assert isinstance(token, str)
    assert len(token) == utils.TOKEN_LENGTH


def test_session_token_is_cached():
    utils._cache_clear()
    token1 = tokens.session_token()
    token2 = tokens.session_token()
    assert token1 == token2


def test_environment_token_without_monkey_patching():
    assert tokens.environment_token() is not None


def test_environment_token_with_target_prefix(tmpdir):
    prefix_token = tokens.environment_token(prefix=tmpdir)
    assert prefix_token is not None
    assert prefix_token != tokens.environment_token()


def test_search_path_without_conda(monkeypatch):
    utils._cache_clear()
    monkeypatch.setitem(__import__('sys').modules, 'conda', None)
    monkeypatch.setitem(__import__('sys').modules, 'conda.base', None)
    monkeypatch.setitem(__import__('sys').modules, 'conda.base.constants', None)
    result = tokens._search_path()
    assert isinstance(result, list)
    for path in result:
        assert isinstance(path, str)


def test_system_tokens_empty(monkeypatch):
    utils._cache_clear()
    monkeypatch.setattr(tokens, "_search_path", lambda: [])
    monkeypatch.delenv("ANACONDA_ANON_USAGE_ORG_TOKEN", raising=False)
    result = tokens._system_tokens("org_token", "organization")
    assert result == []


def test_system_tokens_from_env(monkeypatch):
    utils._cache_clear()
    monkeypatch.setattr(tokens, "_search_path", lambda: [])
    test_token = utils._random_token()
    monkeypatch.setenv("ANACONDA_ANON_USAGE_ORG_TOKEN", test_token)
    result = tokens._system_tokens("org_token", "organization")
    assert result == [test_token]


def test_system_tokens_from_file(monkeypatch, tmp_path):
    utils._cache_clear()
    token_dir = str(tmp_path)
    monkeypatch.setattr(tokens, "_search_path", lambda: [token_dir])
    monkeypatch.delenv("ANACONDA_ANON_USAGE_ORG_TOKEN", raising=False)
    test_token = utils._random_token()
    with open(join(token_dir, "org_token"), "w") as fp:
        fp.write(test_token + "\n# Anaconda organization token\n")
    result = tokens._system_tokens("org_token", "organization")
    assert result == [test_token]


def test_system_tokens_from_dotted_file(monkeypatch, tmp_path):
    utils._cache_clear()
    token_dir = str(tmp_path)
    monkeypatch.setattr(tokens, "_search_path", lambda: [token_dir])
    monkeypatch.delenv("ANACONDA_ANON_USAGE_ORG_TOKEN", raising=False)
    test_token = utils._random_token()
    with open(join(token_dir, ".org_token"), "w") as fp:
        fp.write(test_token + "\n# Anaconda organization token\n")
    result = tokens._system_tokens("org_token", "organization")
    assert result == [test_token]


def test_system_tokens_deduplicates(monkeypatch, tmp_path):
    utils._cache_clear()
    token_dir = str(tmp_path)
    monkeypatch.setattr(tokens, "_search_path", lambda: [token_dir])
    test_token = utils._random_token()
    monkeypatch.setenv("ANACONDA_ANON_USAGE_ORG_TOKEN", test_token)
    with open(join(token_dir, "org_token"), "w") as fp:
        fp.write(test_token)
    result = tokens._system_tokens("org_token", "organization")
    assert result == [test_token]


def test_system_tokens_invalid_filtered(monkeypatch):
    utils._cache_clear()
    monkeypatch.setattr(tokens, "_search_path", lambda: [])
    monkeypatch.setenv("ANACONDA_ANON_USAGE_ORG_TOKEN", "invalid token with spaces")
    result = tokens._system_tokens("org_token", "organization")
    assert result == []


def test_system_tokens_env_and_file(monkeypatch, tmp_path):
    utils._cache_clear()
    token_dir = str(tmp_path)
    monkeypatch.setattr(tokens, "_search_path", lambda: [token_dir])
    env_token = utils._random_token()
    file_token = utils._random_token()
    monkeypatch.setenv("ANACONDA_ANON_USAGE_MACHINE_TOKEN", env_token)
    with open(join(token_dir, "machine_token"), "w") as fp:
        fp.write(file_token)
    result = tokens._system_tokens("machine_token", "machine")
    assert env_token in result
    assert file_token in result
    assert len(result) == 2


def test_organization_tokens(monkeypatch):
    utils._cache_clear()
    monkeypatch.setattr(tokens, "_search_path", lambda: [])
    test_token = utils._random_token()
    monkeypatch.setenv("ANACONDA_ANON_USAGE_ORG_TOKEN", test_token)
    result = tokens.organization_tokens()
    assert result == [test_token]


def test_machine_tokens(monkeypatch):
    utils._cache_clear()
    monkeypatch.setattr(tokens, "_search_path", lambda: [])
    test_token = utils._random_token()
    monkeypatch.setenv("ANACONDA_ANON_USAGE_MACHINE_TOKEN", test_token)
    result = tokens.machine_tokens()
    assert result == [test_token]


def test_installer_tokens(monkeypatch):
    utils._cache_clear()
    monkeypatch.setattr(tokens, "_search_path", lambda: [])
    test_token = utils._random_token()
    monkeypatch.setenv("ANACONDA_ANON_USAGE_INSTALLER_TOKEN", test_token)
    result = tokens.installer_tokens()
    assert result == [test_token]


def test_organization_tokens_empty(monkeypatch):
    utils._cache_clear()
    monkeypatch.setattr(tokens, "_search_path", lambda: [])
    monkeypatch.delenv("ANACONDA_ANON_USAGE_ORG_TOKEN", raising=False)
    result = tokens.organization_tokens()
    assert result == []


def test_machine_tokens_empty(monkeypatch):
    utils._cache_clear()
    monkeypatch.setattr(tokens, "_search_path", lambda: [])
    monkeypatch.delenv("ANACONDA_ANON_USAGE_MACHINE_TOKEN", raising=False)
    result = tokens.machine_tokens()
    assert result == []


def test_installer_tokens_empty(monkeypatch):
    utils._cache_clear()
    monkeypatch.setattr(tokens, "_search_path", lambda: [])
    monkeypatch.delenv("ANACONDA_ANON_USAGE_INSTALLER_TOKEN", raising=False)
    result = tokens.installer_tokens()
    assert result == []


def _make_jwt(header=None, payload=None, signature=None):
    if header is None:
        header = {"alg": "RS256", "typ": "JWT"}
    if payload is None:
        exp = int(dt.datetime.now(tz=dt.timezone.utc).timestamp()) + 3600
        sub = str(uuid.uuid4())
        payload = {"exp": exp, "sub": sub}
    if signature is None:
        signature = {"fake": "sig"}
    parts = [header, payload, signature]
    encoded = []
    for p in parts:
        encoded.append(base64.urlsafe_b64encode(json.dumps(p).encode()).decode().rstrip("="))
    return ".".join(encoded), payload.get("sub")


def test_jwt_to_token_valid():
    jwt_str, sub = _make_jwt()
    result = tokens._jwt_to_token(jwt_str)
    assert result is not None
    expected = base64.urlsafe_b64encode(uuid.UUID(sub).bytes).decode("ascii").strip("=")
    assert result == expected


def test_jwt_to_token_empty():
    assert tokens._jwt_to_token("") is None
    assert tokens._jwt_to_token(None) is None


def test_jwt_to_token_expired():
    exp = int(dt.datetime.now(tz=dt.timezone.utc).timestamp()) - 3600
    sub = str(uuid.uuid4())
    jwt_str, _ = _make_jwt(payload={"exp": exp, "sub": sub})
    result = tokens._jwt_to_token(jwt_str)
    assert result is None


def test_jwt_to_token_invalid_format():
    assert tokens._jwt_to_token("not.a.jwt") is None
    assert tokens._jwt_to_token("onlyone") is None
    assert tokens._jwt_to_token("a.b") is None


def test_jwt_to_token_bad_header():
    jwt_str, _ = _make_jwt(header={"alg": "RS256", "typ": "NOTJWT"})
    assert tokens._jwt_to_token(jwt_str) is None


def test_jwt_to_token_no_exp():
    sub = str(uuid.uuid4())
    jwt_str, _ = _make_jwt(payload={"sub": sub})
    assert tokens._jwt_to_token(jwt_str) is None


def test_jwt_to_token_invalid_sub():
    exp = int(dt.datetime.now(tz=dt.timezone.utc).timestamp()) + 3600
    jwt_str, _ = _make_jwt(payload={"exp": exp, "sub": "not-a-uuid"})
    assert tokens._jwt_to_token(jwt_str) is None


def test_jwt_to_token_no_sub():
    exp = int(dt.datetime.now(tz=dt.timezone.utc).timestamp()) + 3600
    jwt_str, _ = _make_jwt(payload={"exp": exp})
    assert tokens._jwt_to_token(jwt_str) is None


def test_anaconda_auth_token_no_module(monkeypatch):
    utils._cache_clear()
    monkeypatch.setitem(
        __import__('sys').modules, 'anaconda_auth', None
    )
    monkeypatch.setitem(
        __import__('sys').modules, 'anaconda_auth.token', None
    )
    result = tokens.anaconda_auth_token()
    assert result is None


def test_anaconda_auth_token_with_valid_key(monkeypatch):
    utils._cache_clear()
    jwt_str, sub = _make_jwt()
    expected = base64.urlsafe_b64encode(uuid.UUID(sub).bytes).decode("ascii").strip("=")

    class FakeTokenInfo:
        api_key = jwt_str
        @classmethod
        def load(cls, domain=None):
            return cls()

    class FakeTokenNotFoundError(Exception):
        pass

    import types
    fake_module = types.ModuleType("anaconda_auth")
    fake_token_module = types.ModuleType("anaconda_auth.token")
    fake_token_module.TokenInfo = FakeTokenInfo
    fake_token_module.TokenNotFoundError = FakeTokenNotFoundError
    fake_module.token = fake_token_module

    import sys
    monkeypatch.setitem(sys.modules, "anaconda_auth", fake_module)
    monkeypatch.setitem(sys.modules, "anaconda_auth.token", fake_token_module)

    result = tokens.anaconda_auth_token()
    assert result == expected


def test_anaconda_auth_token_not_found(monkeypatch):
    utils._cache_clear()

    class FakeTokenNotFoundError(Exception):
        pass

    class FakeTokenInfo:
        @classmethod
        def load(cls, domain=None):
            raise FakeTokenNotFoundError("no token")

    import types
    fake_module = types.ModuleType("anaconda_auth")
    fake_token_module = types.ModuleType("anaconda_auth.token")
    fake_token_module.TokenInfo = FakeTokenInfo
    fake_token_module.TokenNotFoundError = FakeTokenNotFoundError
    fake_module.token = fake_token_module

    import sys
    monkeypatch.setitem(sys.modules, "anaconda_auth", fake_module)
    monkeypatch.setitem(sys.modules, "anaconda_auth.token", fake_token_module)

    result = tokens.anaconda_auth_token()
    assert result is None
