# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""Availability-drift checks.

* conda ``defaults`` carries 1.40.0 and 1.43.0
* PyPI carries every minor in between, and the declared range is continuous, so pip
  can resolve 1.41.x and 1.42.x. The PyPI matrix covers those

Fails when:

* a version exists on ``defaults`` for **all six** OTel packages, falls inside the
  range declared in ``conda-recipe/meta.yaml``, and is missing from the conda CI
  matrix; or
* a version above our declared ceiling is on ``defaults``, meaning a ceiling
  ratchet is available (see the README policy section: one minor at a time, after
  the matrix passes); or
* a minor series is installable from PyPI inside our range but missing from both
  matrices, leaving a version a pip user can resolve that CI has never imported.
"""

import json
import re
import shutil
import subprocess
import urllib.request
from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.defaults_availability

_REPO_ROOT = Path(__file__).resolve().parents[2]
_META_YAML = _REPO_ROOT / "conda-recipe" / "meta.yaml"
_PR_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "pull-request-tests.yaml"

_CONDA_JOB = "conda-package-tests"
_PYPI_JOB = "pypi-package-tests"

_OTEL_PACKAGES = (
    "opentelemetry-api",
    "opentelemetry-sdk",
    "opentelemetry-exporter-otlp-proto-common",
    "opentelemetry-exporter-otlp-proto-grpc",
    "opentelemetry-exporter-otlp-proto-http",
    "opentelemetry-proto",
)

_MODERN_WINDOW_FLOOR = (1, 39)


def _parse_version(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", text)[:3])


@pytest.fixture(scope="module")
def declared_range() -> tuple[tuple[int, ...], tuple[int, ...]]:
    """The (floor, ceiling) from meta.yaml, e.g. ((1, 40, 0), (1, 44, 0))."""
    line = next(
        line for line in _META_YAML.read_text().splitlines()
        if line.strip().lstrip("- ").startswith("opentelemetry-sdk ")
    )
    floor = re.search(r">=\s*([0-9][0-9.]*)", line)
    ceiling = re.search(r"<\s*([0-9][0-9.]*)", line)
    assert floor and ceiling, f"could not parse bounds from: {line.strip()}"
    return _parse_version(floor.group(1)), _parse_version(ceiling.group(1))


@pytest.fixture(scope="module")
def workflow() -> dict:
    return yaml.safe_load(_PR_WORKFLOW.read_text())


def _matrix_minors(workflow: dict, job: str) -> set[tuple[int, int]]:
    """OTel minor series pinned by one job's matrix, e.g. ``{(1, 40), (1, 43)}``.

    Read from the named job's own ``include:``, since both matrices live in the same
    workflow. Unpinned cells (empty ``otel-version``, meaning "let the resolver
    choose") are skipped.
    """
    jobs = workflow["jobs"]
    assert job in jobs, f"job {job!r} not found in {_PR_WORKFLOW.name}"
    include = jobs[job]["strategy"]["matrix"]["include"]
    minors = {
        _parse_version(str(cell["otel-version"]))[:2]
        for cell in include
        if str(cell.get("otel-version", "")).strip()
    }
    assert minors, f"no pinned otel-version entries in the {job} matrix"
    return minors


@pytest.fixture(scope="module")
def matrix_versions(workflow) -> set[tuple[int, int]]:
    """OTel minor series covered by the conda matrix, e.g. {(1, 40), (1, 43)}."""
    return _matrix_minors(workflow, _CONDA_JOB)


@pytest.fixture(scope="module")
def pypi_matrix_versions(workflow) -> set[tuple[int, int]]:
    """OTel minor series covered by the PyPI matrix, e.g. {(1, 41), (1, 42)}."""
    return _matrix_minors(workflow, _PYPI_JOB)


@pytest.fixture(scope="module")
def pypi_intersection() -> list[tuple[int, ...]]:
    """Versions available on PyPI for *every* one of the OTel packages.

    Same intersection logic as `defaults_intersection`, against the other channel.
    Computed rather than assumed, so a yanked or partial release is excluded.
    """
    per_package = {}
    for package in _OTEL_PACKAGES:
        with urllib.request.urlopen(
            f"https://pypi.org/pypi/{package}/json", timeout=60
        ) as response:
            payload = json.load(response)
        # Keep releases pip can actually resolve: at least one live file, and a
        # final version, since pip reaches a pre-release only when asked.
        per_package[package] = {
            _parse_version(version)
            for version, files in payload["releases"].items()
            if re.fullmatch(r"\d+\.\d+\.\d+", version)
            and files
            and not all(f.get("yanked") for f in files)
        }
    return sorted(set.intersection(*per_package.values()))


@pytest.fixture(scope="module")
def defaults_intersection() -> list[tuple[int, ...]]:
    """Versions available on `defaults` for *every* one of the OTel packages.

    The intersection, not the union: `defaults` carries 1.39.1 of the API but no
    1.39.x SDK or gRPC exporter, so 1.39 is not installable and must not count.
    """
    if shutil.which("conda") is None:
        pytest.skip("conda executable not available")

    per_package = {}
    for package in _OTEL_PACKAGES:
        result = subprocess.run(
            ["conda", "search", "--override-channels", "-c", "defaults",
             "--json", package],
            capture_output=True, text=True, timeout=600,
        )
        payload = json.loads(result.stdout or "{}")
        records = payload.get(package)
        assert records, (
            f"no {package} records returned from defaults: "
            f"{payload.get('error', result.stderr)[:500]}"
        )
        per_package[package] = {_parse_version(r["version"]) for r in records}

    intersection = set.intersection(*per_package.values())
    print("defaults intersection: " + ", ".join(
        ".".join(map(str, v)) for v in sorted(intersection)
    ))
    return sorted(intersection)


def test_every_installable_version_in_range_is_in_the_ci_matrix(
    defaults_intersection, declared_range, matrix_versions
):
    floor, ceiling = declared_range
    uncovered = sorted(
        version for version in defaults_intersection
        if floor <= version < ceiling and version[:2] not in matrix_versions
    )
    assert not uncovered, (
        "conda `defaults` now carries OTel version(s) inside our declared range "
        f"[{'.'.join(map(str, floor))}, {'.'.join(map(str, ceiling))}) that the CI "
        "matrix does not test: "
        + ", ".join(".".join(map(str, v)) for v in uncovered)
        + ". Add them to the `include:` matrix in "
        ".github/workflows/pull-request-tests.yaml."
    )


def test_no_version_above_the_ceiling_is_available(
    defaults_intersection, declared_range
):
    _, ceiling = declared_range
    above = sorted(v for v in defaults_intersection if v >= ceiling)
    assert not above, (
        "conda `defaults` now carries OTel version(s) above our declared ceiling "
        f"{'.'.join(map(str, ceiling))}: "
        + ", ".join(".".join(map(str, v)) for v in above)
        + ". A ceiling ratchet is available. Raise it ONE minor at a time in a "
        "dedicated PR, after re-checking docs/source/otel-private-api.md and confirming "
        "the matrix passes at the new version."
    )


def test_declared_floor_is_installable(defaults_intersection, declared_range):
    floor, _ = declared_range
    assert floor in defaults_intersection, (
        f"declared floor {'.'.join(map(str, floor))} is not available for all "
        "of the OTel packages on `defaults`; the package would be uninstallable "
        "there. "
        "Available: "
        + ", ".join(".".join(map(str, v)) for v in defaults_intersection)
    )


def test_ci_matrix_only_contains_installable_versions(
    defaults_intersection, matrix_versions
):
    installable_minors = {v[:2] for v in defaults_intersection}
    phantom = sorted(matrix_versions - installable_minors)
    assert not phantom, (
        f"the {_CONDA_JOB} matrix pins OTel version(s) unavailable on `defaults`: "
        + ", ".join(f"{major}.{minor}" for major, minor in phantom)
        + f". PyPI-only versions belong in the {_PYPI_JOB} matrix."
    )


def test_every_pypi_reachable_version_in_range_is_tested_somewhere(
    pypi_intersection, defaults_intersection, declared_range,
    matrix_versions, pypi_matrix_versions,
):
    """Every minor pip can resolve inside the range appears in one of the matrices.

    The range is continuous, so that includes the minors `defaults` skipped.
    `_compat.py` degrades to no-op log telemetry on a vanished private import, so an
    untested minor surfaces as missing logs rather than an error.
    """
    floor, ceiling = declared_range
    covered = matrix_versions | pypi_matrix_versions
    uncovered = sorted({
        version[:2] for version in pypi_intersection
        if floor <= version < ceiling and version[:2] not in covered
    })
    conda_minors = {v[:2] for v in defaults_intersection}
    assert not uncovered, (
        "PyPI carries OTel minor series inside our declared range "
        f"[{'.'.join(map(str, floor))}, {'.'.join(map(str, ceiling))}) that neither "
        "CI matrix tests: "
        + ", ".join(
            f"{major}.{minor}"
            + ("" if (major, minor) in conda_minors else " (PyPI-only)")
            for major, minor in uncovered
        )
        + f". Add the highest patch of each to the `{_PYPI_JOB}` include: matrix in "
        ".github/workflows/pull-request-tests.yaml."
    )


def test_modern_window_floor_is_documented(declared_range):
    """Our floor must sit on the post-1.39 side of the ReadableLogRecord rename."""
    floor, _ = declared_range
    assert floor[:2] >= _MODERN_WINDOW_FLOOR, (
        f"floor {'.'.join(map(str, floor))} is below 1.39.0, which straddles the "
        "ReadableLogRecord / ReadWriteLogRecord rename "
        "(open-telemetry/opentelemetry-python#4676). Supporting it requires "
        "dual-path imports in anaconda_opentelemetry/_compat.py -- see "
        "docs/source/otel-private-api.md before lowering."
    )
