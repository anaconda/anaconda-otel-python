# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""Every third-party distribution the package imports must be declared here.

Update this list whenever an import is added or removed from anaconda_opentelemetry/.
anaconda-anon-usage is conda-only (not on PyPI) so it is not in pyproject.toml,
but it is declared in conda-recipe/meta.yaml.
"""

import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PYPROJECT = _REPO_ROOT / "pyproject.toml"

_DIRECT_IMPORTS = {
    "grpcio",
    "opentelemetry-api",
    "opentelemetry-sdk",
    "opentelemetry-exporter-otlp-proto-grpc",
    "opentelemetry-exporter-otlp-proto-http",
    "requests",
}

_CONDA_ONLY = {"anaconda-anon-usage"}


def _declared_distributions() -> set[str]:
    block = re.search(
        r"^dependencies\s*=\s*\[(.*?)^\]", _PYPROJECT.read_text(), re.S | re.M
    )
    assert block, "could not locate [project] dependencies in pyproject.toml"
    body = "\n".join(
        line for line in block.group(1).splitlines()
        if not line.lstrip().startswith("#")
    )
    return {
        re.match(r"\s*([A-Za-z0-9._-]+)", entry).group(1).lower().replace("_", "-")
        for entry in re.findall(r'"([^"]+)"', body)
    }


@pytest.mark.parametrize("package", sorted(_DIRECT_IMPORTS))
def test_direct_import_is_declared(package):
    assert package in _declared_distributions(), (
        f"{package} is imported by anaconda_opentelemetry but not declared in "
        "pyproject.toml. Declare it or remove the import."
    )


@pytest.mark.parametrize("package", sorted(_CONDA_ONLY))
def test_conda_only_import_not_in_pyproject(package):
    assert package not in _declared_distributions(), (
        f"{package} is conda-only and must not appear in pyproject.toml"
    )
