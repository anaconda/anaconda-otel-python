# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

# attributes.py

import logging, platform, re, requests
from typing import Dict, Tuple, Literal
from dataclasses import dataclass, field, fields
from .__version__ import __SDK_VERSION__, __TELEMETRY_SCHEMA_VERSION__

@dataclass
class ResourceAttributes:
    """
    Class used to configure common attributes on initialization and dynamic attributes thereafter

    Parameters:
        service_name (str): name of client service. REQUIRED (enforced regex of ^[a-zA-Z0-9._-]{1,30}$), converted later to service.name
        service_version (str): version of client service. REQUIRED (enforced regex of ^[a-zA-Z0-9._-]{1,30}$), converted later to service.version
        os_type (str): operating system type of client machine
        os_version (str): operating system version of client machine
        python_version (str): python version of client the package
        hostname (str): hostname of client machine
        platform (str): infrastructure on which the software is provided
        environment (Literal["", "test", "development", "staging", "production"]): envrionment the software is running in
        user_id (str): some string denoting a user of a client application
        parameters (Dict[str, str]): optional dictionary containing all other telemetry attributes a client would like to add
        client_sdk_version (str): version of package. READONLY
        schema_version (str): version of telemetry schema used by package. READONLY
    """
    # settable
    service_name: str
    service_version: str
    os_type: str = field(
        default="",
        metadata={"otel_name": "os.type"}
    )
    os_version: str = field(
        default="",
        metadata={"otel_name": "os.version"}
    )
    python_version: str = field(
        default="",
        metadata={"otel_name": "python.version"}
    )
    hostname: str = field(
        default="",
        metadata={"otel_name": "hostname"}
    )
    platform: str = field(
        default="",
        metadata={"otel_name": "platform"}
    )
    environment: Literal["", "test", "development", "staging", "production"] = field(
        default="",
        metadata={"otel_name": "environment"}
    )
    user_id: str = field(
        default="",
        metadata={"otel_name": "user.id"}
    )
    # Readonly
    client_sdk_version: str = field(
        default=__SDK_VERSION__,
        init=False,
        metadata={"readonly": True, "otel_name": "client.sdk.version"}
    )
    schema_version: str = field(
        default=__TELEMETRY_SCHEMA_VERSION__,
        init=False,
        metadata={"readonly": True, "otel_name": "schema.version"}
    )
    parameters: dict = field(
        default_factory=dict,
        init=False,
        metadata={"readonly": True, "otel_name": "parameters"}
    )

    def __setattr__(self, key, value):
        if value is None or key is None:
            logging.getLogger(__package__).warning(f"Either an attribute or key is None which is not allowed. Attribute: `{key}`. Value: `{value}`")
        elif hasattr(self, '_readonly_fields') and key in self._readonly_fields:
            logging.getLogger(__package__).warning(f"Attempted overwrite of readonly common attribute {key}")
        elif (key == "service_name" or key == "service_version") and not self._check_valid_string(value):
            raise ValueError(f"{key} not set. {value} is invalid regex for this key: `^[a-zA-Z0-9._-]{{1,50}}$`. This is a required parameter")
        else:
            super().__setattr__(
                str(key),
                value if key == "parameters" else str(value)
            )

    def __post_init__(self):
        # set non-init readonly
        self.client_sdk_version = __SDK_VERSION__
        self.schema_version = __TELEMETRY_SCHEMA_VERSION__
        self._readonly_fields = {
            f.name for f in fields(self)
            if f.metadata.get("readonly", False) is True
        }
        # default certain attribute values if needed
        if not self.os_type or not self.os_version:
            self.os_type, self.os_version = self._get_os_info()
        if not self.python_version:
            self.python_version = platform.python_version()
        if not self.hostname:
            self.hostname = self._get_host_name()

        # check for valid environment
        valid_environments = {"", "test", "development", "staging", "production"}
        
        # enforce lowercase
        self.environment = self.environment.strip().lower()
        if self.environment not in valid_environments:
            logging.getLogger(__package__).warning(f"Invalid environment value `{self.environment}`, setting to empty string. Envrionment must be in {valid_environments}")
            self.environment = ""

    def _get_os_info(self) -> Tuple[str, str]:
        """Get system OS type and version"""
        return platform.system(), platform.release()

    def _get_host_name(self) -> str:
        """Get the hostname of the machine"""
        from socket import gethostname
        return gethostname()

    def _check_valid_string(self, value) -> bool:
        """Check that service_name and service_version match valid regex"""
        if re.match(r"^[a-zA-Z0-9._-]{1,30}$", str(value)):
            return True
        return False

    def _get_attributes(self) -> Dict[str, str]:
        """Convert all attributes to a dictionary"""
        return {k: v for k, v in self.__dict__.items() if k != '_readonly_fields'}

    def set_attributes(self, **kwargs) -> None:
        """
        Sets attributes according to key value pairs passed to this function. Will overwrite existing attributes, unless they are readonly.

        Parameters:
            \\*\\*kwargs: any keyword arguments. This can set named class properties (common attributes), or any other wildcard name (stored in `parameters`)
                        The following are the common attributes of the class:\n
                        
                        - service_name (str): name of client service\n
                        - service_version (str): version of client service\n
                        - os_type (str): operating system type of client machine\n
                        - os_version (str): operating system version of client machine\n
                        - python_version (str): python version of client the package\n
                        - hostname (str): hostname of client machine\n
                        - platform (str): infrastructure on which the software runs\n
                        - environment (Literal["", "test", "development", "staging", "production"]): environment of the software\n
                        - user_id (str): some string denoting a user of a client application\n
        """
        for kwarg in kwargs:
            # if kwarg has already been initialized as a property
            if kwarg in self.__dict__.keys():
                self.__setattr__(kwarg, kwargs[kwarg])
            else:
                self.parameters[str(kwarg)] = str(kwargs[kwarg])

        return self
    
def get_public_ip(attributes: ResourceAttributes, IPv4=True, IPv6=True):
    """Get public IPs synchronously (runs in Telemetry-Init thread)"""  
    ipv4_services = [
        'https://api.ipify.org?format=json',
        'https://ipinfo.io/json',
    ]
    
    ipv6_services = [
        'https://v6.ipinfo.io/json',
        'https://api6.ipify.org?format=json'
    ]
    
    result = {'ipv4': None, 'ipv6': None}
    
    # Try IPv4
    if IPv4:
        for service in ipv4_services:
            try:
                response = requests.get(service, timeout=10)
                data = response.json()
                ip = data.get('ip') or data.get('query')
                if ip and ':' not in ip:
                    result['ipv4'] = ip
                    break
            except Exception:
                pass
    
    # Try IPv6
    if IPv6:
        for service in ipv6_services:
            try:
                response = requests.get(service, timeout=10)
                data = response.json()
                ip = data.get('ip') or data.get('ipv6')
                if ip and ':' in ip:
                    result['ipv6'] = ip
                    break
            except Exception:
                pass
    
    attributes.set_attributes(IPv4_address=result['ipv4'], IPv6_address=result['ipv6'])