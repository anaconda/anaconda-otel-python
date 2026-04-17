# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

# common.py
"""
Anaconda Telemetry - Common base class and exceptions for signal classes.
"""

import logging, hashlib, json
from typing import Dict
from dataclasses import fields

from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION

from .config import Configuration as Config
from .attributes import ResourceAttributes as Attributes
from .__version__ import __SDK_VERSION__, __TELEMETRY_SCHEMA_VERSION__
from .formatting import AttrDict

from anaconda_opentelemetry.anon_usage import tokens
TOKEN_FUNCS = [
    ("client_token", tokens.client_token),
    ("session_token", tokens.session_token),
    ("environment_token", tokens.environment_token),
    ("organization_tokens", tokens.organization_tokens),
    ("installer_tokens", tokens.installer_tokens),
    ("machine_tokens", tokens.machine_tokens),
    ("anaconda_auth_token", tokens.anaconda_auth_token),
]

class MetricsNotInitialized(RuntimeError):
    pass


class _AnacondaCommon:
    # Base class for common attributes and methods (internal only)
    def __init__(self, config: Config, attributes: Attributes):
        self._config = config
        # Init resource_attributes
        self._resource_attributes = {}
        self.resource = None
        # session id
        self._session_id = None
        # user id
        self._user_id = None

        # Make self._resource_attributes and self.resource
        self.make_otel_resource(attributes)

        self.logger = logging.getLogger(__package__)

        # assemble config and attribute values
        # default endpoint
        self.default_endpoint = config._get_default_endpoint()
        # export options
        self.use_console_exporters = config._get_console_exporter()
        # anon usage
        self.anon_usage = config._get_anon_usage()

    def make_otel_resource(self, attributes: Attributes):
        # Read resource attributes
        resource_attrs = attributes._get_attributes()
        # Required parameters
        self.service_name = resource_attrs["service_name"]
        self.service_version = resource_attrs["service_version"]
        # prepare to use `_process_attributes`
        self._user_id = resource_attrs["user_id"]
        del resource_attrs["service_name"], resource_attrs["service_version"], resource_attrs["user_id"]

        # convert parameters value to stringified JSON
        resource_attrs["parameters"] = json.dumps(resource_attrs["parameters"])
        # Init resource_attributes
        self._resource_attributes = {
                SERVICE_NAME: self.service_name,
                SERVICE_VERSION: self.service_version
        }
        self._resource_attributes.update(resource_attrs)
        # convert to otel names
        for attr in fields(attributes):
            otel_name = attr.metadata.get('otel_name', None)
            if otel_name:
                self._resource_attributes[attr.metadata['otel_name']] = self._resource_attributes.pop(attr.name)
        self._session_id = self._hash_session_id(self._config._get_tracing_session_entropy())
        self._resource_attributes['session.id'] = self._session_id
        self.resource = Resource.create(self._resource_attributes)

    def _hash_session_id(self, entropy):
        # Hashes a session id for common attributes based on timestamp and user_id
        # entropy value ensures unique session_ids
        if entropy is None:
            raise KeyError("The entropy key has been removed.")

        user_id = self._resource_attributes.get('user.id', '')
        combined = f"{entropy}|{user_id}|{self.service_name}"
        hashed = hashlib.sha256(combined.encode("utf-8")).hexdigest()

        return hashed

    def _build_http_exporter_kwargs(self, signal: str, endpoint: str, headers: Dict[str, str], **extra_kwargs) -> Dict:
        get_ca_cert = getattr(self._config, f"_get_ca_cert_{signal}")
        kwargs = dict(
            endpoint=endpoint,
            certificate_file=get_ca_cert(),
            headers=headers,
            **extra_kwargs
        )
        session = self._config._create_proxy_session()
        if session is not None:
            kwargs['session'] = session
        return kwargs

    def _process_attributes(self, attributes: AttrDict={}):
        # ensure attributes are of type AttrDict
        if not isinstance(attributes, Dict):
            self.logger.error(f"Attributes `{attributes}` are not a dictionary, they are not valid. They will be converted to an empty one.")
            attributes = {}
        # check attributes for invalid keys
        if any(not isinstance(key, str) or not key for key in attributes):
            self.logger.error(f"Attributes `{attributes}` passed with non empty str type key. Invalid attributes.")
            attributes = {}

        # if anon-usage is enabled
        # WILL override any identically named attributes
        if self.anon_usage:
            for name, func in TOKEN_FUNCS:
                print(f"{name}: {func()}")
                attributes[name.replace('_', '.')] = func()

        # pulls a user id initially passed to ResourceAttributes and adds it to event specific events
        # for backwards compatability if people have been setting user.id with ResourceAttributes
        if not self._user_id:
            return attributes  # no op
        elif 'user.id' in attributes:
            return attributes  # key already exists
        else:
            attributes['user.id'] = self._user_id
            return attributes