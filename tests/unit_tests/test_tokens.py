from os.path import exists

from anaconda_opentelemetry.anon_usage import tokens, utils


def test_client_token(aau_token_path):
    assert not exists(aau_token_path)
    assert tokens.client_token() != ""
    assert exists(aau_token_path)


def test_client_token_no_nodeid(aau_token_path, mocker):
    m1 = mocker.patch("anaconda_opentelemetry.anon_usage.utils._get_node_str")
    m1.return_value = None
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


def test_environment_token_without_monkey_patching():
    assert tokens.environment_token() is not None


def test_environment_token_with_target_prefix(tmpdir):
    prefix_token = tokens.environment_token(prefix=tmpdir)
    assert prefix_token is not None
    assert prefix_token != tokens.environment_token()
