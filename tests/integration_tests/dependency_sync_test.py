# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""Guard against drift between the PyPI and conda dependency declarations."""

import re
from pathlib import Path

import pytest
import yaml

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PYPROJECT = _REPO_ROOT / "pyproject.toml"
_META_YAML = _REPO_ROOT / "conda-recipe" / "meta.yaml"
_PR_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "pull-request-tests.yaml"

_PYPI_JOB = "pypi-package-tests"

# Packages that must carry an identical range in both files. This is exactly the
# set the code imports -- see tests/unit_tests/direct_imports_test.py.
_OTEL_PACKAGES = frozenset({
    "opentelemetry-api",
    "opentelemetry-sdk",
    "opentelemetry-exporter-otlp-proto-grpc",
    "opentelemetry-exporter-otlp-proto-http",
})

# Non-OTel runtime dependencies that must also match across the two files.
_SHARED_PACKAGES = frozenset({"grpcio", "requests"})

_SYNCED_PACKAGES = _OTEL_PACKAGES | _SHARED_PACKAGES


_CONSTRAINT_RE = re.compile(r"(?P<op>[<>=!~]=?)\s*(?P<version>[0-9][0-9a-zA-Z.*+!-]*)")


def _normalize(constraint: str) -> tuple[str, str]:
    """Normalize one constraint to ``(operator, comparable version)``.

    Strips the conda-only pre-release suffix and trailing zero segments so that
    ``<1.44``, ``<1.44.0`` and ``<1.44.0a0`` all compare equal, while
    ``<0.65b0`` stays distinct from ``<0.65`` (the beta suffix there is
    significant in both ecosystems).
    """
    match = _CONSTRAINT_RE.fullmatch(constraint.replace(" ", ""))
    assert match, f"unparseable constraint: {constraint!r}"
    version = match["version"]
    # conda's "below the first alpha of X" spelling -> plain X
    version = re.sub(r"\.0a0$|(?<=[0-9])a0$", "", version)
    while version.endswith(".0"):
        version = version[:-2]
    return match["op"], version


def _parse_spec(spec: str) -> tuple[str, tuple[tuple[str, str], ...]]:
    """Split ``"opentelemetry-sdk >=1.40.0,<1.44"`` into name and constraints."""
    name, _, rest = re.match(r"\s*([A-Za-z0-9._-]+)\s*(,?)(.*)", spec).group(1, 2, 3)
    constraints = tuple(sorted(
        _normalize(part) for part in rest.split(",") if part.strip()
    ))
    return name.lower(), constraints


def _pyproject_requirements() -> dict[str, tuple[tuple[str, str], ...]]:
    block = re.search(
        r"^dependencies\s*=\s*\[(.*?)^\]", _PYPROJECT.read_text(), re.S | re.M
    )
    assert block, "could not locate [project] dependencies in pyproject.toml"
    body = "\n".join(
        line for line in block.group(1).splitlines()
        if not line.lstrip().startswith("#")
    )
    return dict(
        _parse_spec(entry)
        for entry in re.findall(r'"([^"]+)"', body)
    )


def _meta_yaml_run_requirements() -> dict[str, tuple[tuple[str, str], ...]]:
    lines = _META_YAML.read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == "run:")
    indent = len(lines[start]) - len(lines[start].lstrip())
    entries = {}
    for line in lines[start + 1:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if len(line) - len(line.lstrip()) <= indent:
            break
        entries.update([_parse_spec(line.strip().lstrip("-"))])
    assert entries, "could not locate run: requirements in meta.yaml"
    return entries


@pytest.fixture(scope="module")
def pypi_requirements():
    return _pyproject_requirements()


@pytest.fixture(scope="module")
def conda_requirements():
    return _meta_yaml_run_requirements()


def test_all_otel_packages_declared_in_both(pypi_requirements, conda_requirements):
    assert _SYNCED_PACKAGES <= set(pypi_requirements), (
        f"missing from pyproject.toml: {sorted(_SYNCED_PACKAGES - set(pypi_requirements))}"
    )
    assert _SYNCED_PACKAGES <= set(conda_requirements), (
        f"missing from meta.yaml run:: {sorted(_SYNCED_PACKAGES - set(conda_requirements))}"
    )


@pytest.mark.parametrize("package", sorted(_SYNCED_PACKAGES))
def test_otel_ranges_match(package, pypi_requirements, conda_requirements):
    assert pypi_requirements.get(package) == conda_requirements.get(package), (
        f"{package} range differs between pyproject.toml "
        f"({pypi_requirements.get(package)}) and conda-recipe/meta.yaml "
        f"({conda_requirements.get(package)})"
    )


def test_conda_upper_bounds_carry_prerelease_suffix():
    """A bare conda `<1.44` would admit `1.44.0a1`; require the `.0a0` form."""
    text = _META_YAML.read_text()
    for package in sorted(_OTEL_PACKAGES):
        line = next(
            l for l in text.splitlines()
            if l.strip().lstrip("- ").startswith(package + " ")
        )
        upper = re.search(r"<\s*([0-9][0-9a-zA-Z.]*)", line)
        assert upper, f"{package} has no upper bound in meta.yaml: {line.strip()}"
        assert re.search(r"(\.0a0|[0-9]b[0-9]+)$", upper.group(1)), (
            f"{package} conda upper bound {upper.group(1)!r} must end in '.0a0' "
            f"(or a 'bN' suffix for semconv-style versions) so pre-releases are "
            f"excluded: {line.strip()}"
        )


def test_python_floor_mirrored_into_host(pypi_requirements):
    text = _META_YAML.read_text()
    host_block = re.search(r"^  host:\n((?:    .*\n)+)", text, re.M)
    assert host_block, "could not locate host: requirements in meta.yaml"
    assert re.search(r"-\s*python\s*>=3\.10", host_block.group(1)), (
        "meta.yaml host: must mirror the python >=3.10 floor from run:"
    )
    assert 'requires-python = ">=3.10"' in _PYPROJECT.read_text()


# --- CI matrix shape (version coverage is checked in defaults_availability_test) ---


@pytest.fixture(scope="module")
def pypi_matrix():
    include = yaml.safe_load(_PR_WORKFLOW.read_text())["jobs"][_PYPI_JOB][
        "strategy"
    ]["matrix"]["include"]
    assert include, f"no include: matrix found for the {_PYPI_JOB} job"
    return include


def _pin(cell) -> str:
    return str(cell.get("otel-version", "")).strip()


def test_pypi_matrix_pins_exact_patch_versions(pypi_matrix):
    """pip resolves `==1.41.1` to one release; conda's `=1.41` means the series."""
    bad = [
        _pin(cell) for cell in pypi_matrix
        if _pin(cell) and not re.fullmatch(r"\d+\.\d+\.\d+", _pin(cell))
    ]
    assert not bad, (
        f"the {_PYPI_JOB} matrix must pin exact patch versions (pip has no "
        f"`==1.41` series semantics); got: {bad}"
    )


def test_pypi_matrix_has_an_unpinned_cell(pypi_matrix):
    """The unpinned cell is what hands the declared range to a resolver.

    The conda job installs the built conda package, so this cell carries the whole
    of pip's verdict on `pyproject.toml`.
    """
    assert any(not _pin(cell) for cell in pypi_matrix), (
        f"the {_PYPI_JOB} matrix needs a cell with an empty `otel-version` to "
        "verify that pip can satisfy the range in pyproject.toml."
    )


def test_pypi_matrix_pins_fall_inside_the_declared_range(pypi_matrix, pypi_requirements):
    """Keeps a pin the range forbids from surfacing as a bare resolution error."""
    bounds = dict(
        (op, tuple(int(n) for n in re.findall(r"\d+", version)[:3]))
        for op, version in pypi_requirements["opentelemetry-sdk"]
    )
    assert {">=", "<"} <= set(bounds), (
        f"opentelemetry-sdk needs both bounds in pyproject.toml; got {bounds}"
    )
    for cell in pypi_matrix:
        pin = _pin(cell)
        if not pin:
            continue
        version = tuple(int(n) for n in re.findall(r"\d+", pin)[:3])
        assert bounds[">="] <= version < bounds["<"], (
            f"{_PYPI_JOB} pins opentelemetry {pin}, which is outside the range "
            f"declared in pyproject.toml ({bounds})"
        )
