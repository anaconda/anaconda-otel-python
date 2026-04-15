# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""Anonymous token generation and retrieval.

Ported from anaconda-anon-usage so that this package can operate
without depending on it. This module provides functions for reading
and writing the anonymous token set. It has been designed to rely
only on the Python standard library. In particular, hard dependencies
on conda must be avoided so that this package can be used in child
environments.
"""

import atexit
import base64
import datetime as dt
import errno
import json
import logging
import os
import re
import sys
import uuid
from os.path import dirname, expanduser, isdir, isfile, join
from threading import RLock
from typing import List, Optional

logger = logging.getLogger(__name__)

# Number of bits of randomness to include in the token
_MIN_ENTROPY = 128
# Number of base64-encoded characters required to contain
# at least MIN_ENTROPY bits of randomness
_TOKEN_LENGTH = (_MIN_ENTROPY - 1) // 6 + 1

_WRITE_SUCCESS = 0
_WRITE_DEFER = 1
_WRITE_FAIL = 2

_CONFIG_DIR = expanduser("~/.conda")

_INSTALLER_TOKEN_NAME = "installer_token"
_ORG_TOKEN_NAME = "org_token"
_MACHINE_TOKEN_NAME = "machine_token"

# System tokens may consist of only letters, numbers,
# underscores, and dashes, with no more than 36 characters.
_VALID_TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{1,36}$")

# While lru_cache is thread safe, it does not prevent two threads
# from beginning the same computation. This simple cache mechanism
# uses a lock to ensure that only one thread even attempts.
_CACHE: dict = {}
_LOCK = RLock()


def _cached(func):
    def _call_if_needed(*args, **kwargs):
        key = (func.__name__, args, tuple(kwargs.items()))
        if key not in _CACHE:
            with _LOCK:
                # Need to check again, just in case the
                # computation was happening between the
                # first check and the lock acquisition.
                if key not in _CACHE:
                    _CACHE[key] = func(*args, **kwargs)
        return _CACHE[key]

    return _call_if_needed


# When creating a new environment, the environment token will be
# created in advance of the action creation of the standard conda
# directory structure. If we write the token to its location and
# then the creation is interrupted, the directory will now be in
# a state where conda is unwilling to install into it, thinking
# it is a non-empty non-conda directory.
_DEFERRED: List = []


def _final_attempt():
    """
    Called upon graceful exit from the process, this attempts to
    write an environment token that was deferred because the
    environment directory was not yet available.
    """
    for must_exist, fpath, token, _what in _DEFERRED:
        _write_attempt(must_exist, fpath, token)


atexit.register(_final_attempt)

def _random_token(what: str = "random") -> str:
    # base64 encoding captures 6 bits per character.
    # Generate enough random bytes to ensure all characters are random
    data = os.urandom((_TOKEN_LENGTH * 6 - 1) // 8 + 1)
    result = base64.urlsafe_b64encode(data).decode("ascii")[:_TOKEN_LENGTH]
    logger.debug("Generated %s token: %s", what, result)
    return result


def _write_attempt(must_exist, fpath: str, token: str) -> int:
    """
    Attempt to write the token to the given location.
    Return True with success, False otherwise.
    """
    if must_exist and not isdir(must_exist):
        logger.debug("Directory not ready: %s", must_exist)
        return _WRITE_DEFER
    try:
        os.makedirs(dirname(fpath), exist_ok=True)
        with open(fpath, "w") as fp:
            fp.write(token)
        logger.debug("Token saved: %s", fpath)
        return _WRITE_SUCCESS
    except Exception as exc:
        # If we get here, a second attempt is unlikely to succeed,
        # so we return a code to indicate that we should not re-attempt.
        if getattr(exc, "errno", None) in (errno.EACCES, errno.EPERM, errno.EROFS):
            logger.debug("No write permissions; cannot write token")
        else:
            logger.debug(
                "Unexpected error writing token file:\n  path: %s\n  exception: %s",
                fpath,
                exc,
            )
        return _WRITE_FAIL


def _deferred_exists(fpath: str, what: str) -> Optional[str]:
    """
    Check if the deferred token write exists in the DEFERRED write array.
    If the path must already exist, this helper function determines
    if the token will be written in the future.

    Args:
        fpath: The file path to check for.
        what: The type of token to check for.
        deferred_tokens: The list of deferred tokens to check.

    Returns:
        The token if it exists, otherwise None.
    """
    for _, fp, token, w in _DEFERRED:
        if fp == fpath and w == what:
            return token
    return None


def _read_file(fpath: str, what: str, single_line: bool = False) -> Optional[str]:
    """
    Implements the saved token functionality. If the specified
    file exists, and contains a token with the right format,
    return it. Otherwise, generate a new one and save it in
    this location. If that fails, return an empty string.
    """
    # If a deferred token exits for the given fpath, return it instead of generating a new one.
    deferred_token = _deferred_exists(fpath, what)
    if deferred_token:
        logger.debug("Returning deferred %s: %s", what, deferred_token)
        return deferred_token

    logger.debug("%s path: %s", what.capitalize(), fpath)
    if not isfile(fpath):
        logger.debug("%s file is not present", what)
        return None

    try:
        with open(fpath) as fp:
            data = fp.read()
        if single_line:
            data = data.strip()
            if data:
                data = data.splitlines()[0]
        logger.debug("Retrieved %s: %s", what, data)
        return data
    except Exception as exc:
        logger.debug("Unexpected error reading: %s\n  %s", fpath, exc)
        return None


def _get_node_str() -> str:
    """
    Returns a base64-encoded representation of the host ID
    as determined by uuid.getnode().
    """
    val = getattr(uuid, "_unix_getnode", lambda: None)()
    if not val:
        val = getattr(uuid, "_windll_getnode", lambda: None)()
    if not val and getattr(uuid, "_generate_time_safe", None):
        val = uuid.UUID(bytes=uuid._generate_time_safe()[0]).node
    if val:
        raw = val.to_bytes(6, byteorder=sys.byteorder)
        return base64.urlsafe_b64encode(raw).decode("ascii")
    return ""


def _saved_token(
    fpath: str,
    what: str,
    must_exist=None,
    node_tie: bool = False,
) -> str:
    """
    Implements the saved token functionality. If the specified
    file exists, and contains a token with the right format,
    return it. Otherwise, generate a new one and save it in
    this location. If that fails, return an empty string.
    """
    what_label = what + " token"
    regenerate = resave = False
    raw = _read_file(fpath, what_label, single_line=True) or ""
    # Version 0.7.0 stored the host ID alongside the client token
    token, *xtra = raw.split(" ", 1)

    if len(token) < _TOKEN_LENGTH:
        if token:
            logger.debug("Regenerating %s due to short length", what_label)
        regenerate = True

    if node_tie:
        # Client tokens should be unique to each user, but under some
        # scenarios they are inadvertently copied to multiple machines,
        # which breaks that behavior. To resolve this issue, we create a
        # sidecar file containing the host ID. If the host ID changes,
        # we can regenerate the token. The token itself remains 100%
        # anonymous under this approach, and the host ID is not sent.
        current_node = _get_node_str()
        npath = fpath + "_host"
        saved_node = _read_file(npath, "Host id", single_line=True) or ""
        true_node = saved_node or (xtra[0] if xtra else None)

        if regenerate or not true_node:
            pass
        elif true_node != current_node:
            logger.debug("Regenerating %s due to hostID change", what_label)
            regenerate = True
        elif xtra:
            logger.debug("Stripping host ID from %s file", what_label)
            resave = True
        else:
            logger.debug("Host ID match confirmed for %s", what_label)

        if saved_node != current_node:
            current_node_val = current_node or ""
            if _write_attempt(False, npath, current_node_val) == _WRITE_DEFER:
                _DEFERRED.append((False, npath, current_node_val, "Host ID"))

    if regenerate or resave:
        if regenerate:
            token = _random_token()
        status = _write_attempt(must_exist, fpath, token)
        if status == _WRITE_FAIL:
            logger.debug("Returning blank %s", what_label)
            return ""
        elif status == _WRITE_DEFER:
            # If the environment has not yet been created we need
            # to defer the token write until later.
            logger.debug("Deferring %s write", what_label)
            _DEFERRED.append((must_exist, fpath, token, what_label))

    return token


# ---------------------------------------------------------------------------
# Search path for system tokens
# ---------------------------------------------------------------------------


def _search_path() -> List[str]:
    """
    Returns the search path for system tokens.
    """
    try:
        # Do not import SEARCH_PATH directly since we need to
        # temporarily patch it for testing
        from conda.base import constants as c_constants

        search_path = c_constants.SEARCH_PATH
    except ImportError:
        # Because this module was designed to be used even in
        # environments that do not include conda, we need a
        # fallback in case conda.base.constants.SEARCH_PATH
        # is not available. This is a pruned version of the
        # constructed value of this path as of 2024-12-13.
        logger.debug("conda not installed in this environment")
        if sys.platform == "win32":
            search_path = ("C:/ProgramData/conda/.condarc",)
        else:
            search_path = ("/etc/conda/.condarc", "/var/lib/conda/.condarc")
        search_path += (
            "$XDG_CONFIG_HOME/conda/.condarc",
            "~/.config/conda/.condarc",
            "~/.conda/.condarc",
            "~/.condarc",
            "$CONDARC",
        )

    result: List[str] = []
    home = expanduser("~")
    for path in search_path:
        # Only consider directories where
        # .condarc could also be found
        if not path.endswith("/.condarc"):
            continue
        parts = path.split("/")[:-1]
        if parts[0] == "~":
            parts[0] = home
        elif parts[0].startswith("$"):
            parts[0] = os.environ.get(parts[0][1:])
            if not parts[0]:
                continue
        path = "/".join(parts)
        if isdir(path) and path != home:
            result.append(path)
    # Deduplicate preserving order
    return list(dict.fromkeys(result))


# ---------------------------------------------------------------------------
# System tokens (installer / organization / machine)
# ---------------------------------------------------------------------------


def _system_tokens(fname: str, what: str) -> List[str]:
    """
    Returns an organization or machine token installed somewhere
    in the conda path. Unlike most tokens, these will typically
    be installed by system administrators, often by mobile device
    management software. There can also be multiple tokens present
    along the path, in which case we combine them
    """
    tokens: List[str] = []
    env_name = "ANACONDA_ANON_USAGE_" + fname.upper()
    t_token = os.environ.get(env_name)
    if t_token:
        logger.debug("Found %s token in environment: %s", what, t_token)
        tokens.append(t_token)
    for path in _search_path():
        for pfx in ("", "."):
            fpath = join(path, pfx + fname)
            if isfile(fpath):
                t_token = _read_file(fpath, what + " token", single_line=True)
                if t_token:
                    tokens.append(t_token)
    # Deduplicate while preserving order
    tokens = list(dict.fromkeys(t for t in tokens if t))
    if not tokens:
        logger.debug("No %s tokens found", what)
    # Make sure the tokens we omit have only valid characters, so any
    # server-side token parsing is not frustrated.
    valid = [t for t in tokens if _VALID_TOKEN_RE.match(t)]
    if len(valid) < len(tokens):
        invalid = ", ".join(t for t in tokens if not _VALID_TOKEN_RE.match(t))
        logger.debug("One or more invalid %s tokens discarded: %s", what, invalid)
    return valid


# ---------------------------------------------------------------------------
# JWT parsing for Anaconda Cloud token
# ---------------------------------------------------------------------------


def _jwt_to_token(s: str) -> Optional[str]:
    """Unpacks an Anaconda auth token and returns the encoded user ID for
    potential inclusion in the user agent, along with its expiration.

    The Anaconda API key takes the form of a standard OAuth2 access token,
    with the additional requirement that the "sub" field is a UUID string.
    This code perorms a basic set of integrity checks to confirm that this
    is the case. If the checks pass, the function returns an encoded form
    of "sub" as well as the "exp" value to enable sorting by expiration.
    If the checks fail, the function returns (None, 0).

    The signature is not fully validated as part of the check; only that it
    is a base64-encoded value. Validation is left to anaconda-auth.

    Returns:
      token: the token if valid; None otherwise
      exp: the expiration time
    """
    if not s:
        return None
    try:
        # The JWT should have three parts separated by periods
        parts = s.split(".")
        assert len(parts) == 3 and all(parts), "3 parts expected"
        # Each part should be base64 encoded
        decoded = [base64.urlsafe_b64decode(p + "===") for p in parts]
        # The header and payload should be json dictionaries
        header, payload = json.loads(decoded[0]), json.loads(decoded[1])
        assert isinstance(header, dict), "Invalid header"
        assert header.get("typ") == "JWT", "Invalid header"
        assert isinstance(payload, dict), "Invalid payload"
        # The payload should have a positive integer expiration
        exp = payload.get("exp")
        assert isinstance(exp, int) and exp > 0, "Invalid expiration"
        now = dt.datetime.now(tz=dt.timezone.utc).timestamp()
        if exp < now:
            logger.debug("API key expired %ds ago", int(now - exp))
            return None
        # The subscriber should be a non-empty UUID string
        sub = payload.get("sub")
        assert sub, "Invalid subscriber"
        # This is an Anaconda requirement, not a JWT requirement
        sub_bytes = uuid.UUID(sub).bytes
        token = base64.urlsafe_b64encode(sub_bytes).decode("ascii").rstrip("=")
        return token
    except Exception as exc:
        logger.debug("Unexpected %s parsing API key: %s", type(exc).__name__, exc)
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


@_cached
def client_token() -> str:
    """
    Returns the client token. If a token has not yet
    been generated, an attempt is made to do so. If
    that fails, an empty string is returned.
    """
    fpath = join(_CONFIG_DIR, "aau_token")
    return _saved_token(fpath, "client", node_tie=True)


@_cached
def session_token() -> str:
    """
    Returns the session token, generated randomly for each
    execution of the process.
    """
    return _random_token("session")


@_cached
def environment_token(prefix: Optional[str] = None) -> str:
    """
    Returns the environment token for the given prefix, or
    sys.prefix if one is not supplied. If a token has not
    yet been generated, an attempt is made to do so. If that
    fails, an empty string is returned.
    """
    if prefix is None:
        prefix = sys.prefix
    fpath = join(prefix, "etc", "aau_token")
    return _saved_token(fpath, "environment", must_exist=prefix)


@_cached
def anaconda_cloud_token() -> Optional[str]:
    """Returns the base64-encoded uid corresponding to the logged
    in Anaconda Cloud user, if one is present.
    Returns:
        str: Base64-encoded token, or None if no valid token found.
    """
    try:
        from anaconda_auth.token import TokenInfo, TokenNotFoundError

        logger.debug("Module anaconda_auth loaded")
        tinfo = TokenInfo.load(domain="anaconda.com")
        if tinfo.api_key:
            token = _jwt_to_token(tinfo.api_key)
            logger.debug("Retrieved Anaconda auth token: %s", token)
            return token
    except ImportError:
        logger.debug("Module anaconda_auth not available")
    except Exception as exc:
        # TokenNotFoundError is caught here implicitly when anaconda_auth
        # is available; we also guard against any other unexpected errors.
        logger.debug(
            "Unexpected error retrieving token using anaconda_auth: %s", exc
        )
    logger.debug("No Anaconda API token found")
    return None


@_cached
def installer_tokens() -> List[str]:
    """
    Returns the list of installer tokens.
    """
    return _system_tokens(_INSTALLER_TOKEN_NAME, "installer")


@_cached
def organization_tokens() -> List[str]:
    """
    Returns the list of organization tokens.
    """
    return _system_tokens(_ORG_TOKEN_NAME, "organization")


@_cached
def machine_tokens() -> List[str]:
    """
    Returns the list of machine tokens.
    """
    return _system_tokens(_MACHINE_TOKEN_NAME, "machine")
