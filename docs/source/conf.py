# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath('../../'))  # adjust path as needed
from anaconda.opentelemetry import __version__

project = 'Anaconda OpenTelemetry Wrapper'
copyright = '2025, Anaconda, Inc.'
author = 'Anaconda, Inc.'
release = __version__
license = 'Apache License 2.0'


def skip_member(app, what, name, obj, skip, options):
    if name in [
        'DEFAULT_ENDPOINT_NAME',
        'LOGGING_ENDPOINT_NAME',
        'TRACING_ENDPOINT_NAME',
        'METRICS_ENDPOINT_NAME',
        'USE_TLS_NAME',
        'USE_CONSOLE_EXPORTER_NAME',
        'AUTH_TOKEN_NAME',
        'METRICS_EXPORT_INTERVAL_MS_NAME',
        'LOGGING_LEVEL_NAME',
        'SESSION_ENTROPY_VALUE_NAME',
        'TLS_PRIVATE_CA_CERT_FILE_NAME',
        'SKIP_INTERNET_CHECK_NAME',
        'REQUEST_PROTOCOL_NAME',
        'client_sdk_version',
        'environment',
        'hostname',
        'os_type',
        'os_version',
        'platform',
        'python_version',
        'schema_version',
        'service_name',
        'service_version',
        'user_id'
    ]:
        return True  # skip it
    return skip  # default behavior

def setup(app):
    app.connect("autodoc-skip-member", skip_member)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc.typehints'
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'private-members': False,
    'special-members': False,
    'show-inheritance': True,
}
templates_path = ['_templates']
exclude_patterns = []

# -- Options for PDF output --------------------------------------------------
latex_elements = {
    'classoptions': ',openany,oneside',
    'babel': r'\usepackage[english]{babel}',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
