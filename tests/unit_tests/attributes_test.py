# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

import sys
sys.path.append("./")

import unittest, pytest
from unittest.mock import patch, MagicMock
from anaconda_opentelemetry.attributes import ResourceAttributes
from anaconda_opentelemetry.__version__ import __SDK_VERSION__, __TELEMETRY_SCHEMA_VERSION__

class TestResourceAttributes(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.test_service_name = "test_service"
        self.test_service_version = "1.0.0"

    # Test initialization
    def test_init_with_required_fields_only(self):
        """Test initialization with only required fields"""
        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        self.assertEqual(attrs.service_name, self.test_service_name)
        self.assertEqual(attrs.service_version, self.test_service_version)

    def test_init_with_all_settable_fields(self):
        """Test initialization with all settable fields"""
        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version,
            os_type="Linux",
            os_version="5.4.0",
            python_version="3.9.0",
            hostname="test-host",
            platform="AWS",
            environment="production",
            user_id="12345"
        )

        self.assertEqual(attrs.os_type, "Linux")
        self.assertEqual(attrs.os_version, "5.4.0")
        self.assertEqual(attrs.python_version, "3.9.0")
        self.assertEqual(attrs.hostname, "test-host")
        self.assertEqual(attrs.platform, "AWS")
        self.assertEqual(attrs.environment, "production")
        self.assertEqual(attrs.user_id, "12345")

    @patch('platform.system')
    @patch('platform.release')
    @patch('platform.python_version')
    @patch('socket.gethostname')
    def test_default_values_populated(
        self,
        mock_hostname: MagicMock,
        mock_python_version: MagicMock,
        mock_release: MagicMock,
        mock_system: MagicMock
    ):
        """Test that default values are populated when not provided"""
        mock_system.return_value = "Darwin"
        mock_release.return_value = "20.6.0"
        mock_python_version.return_value = "3.8.5"
        mock_hostname.return_value = "test-machine"

        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        self.assertEqual(attrs.os_type, "Darwin")
        self.assertEqual(attrs.os_version, "20.6.0")
        self.assertEqual(attrs.python_version, "3.8.5")
        self.assertEqual(attrs.hostname, "test-machine")

    # Test readonly fields
    def test_readonly_fields_initialized(self):
        """Test that readonly fields are properly initialized"""
        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        self.assertEqual(attrs.client_sdk_version, __SDK_VERSION__)
        self.assertEqual(attrs.schema_version, __TELEMETRY_SCHEMA_VERSION__)

    @patch('logging.getLogger')
    def test_readonly_field_modification_warning(self, mock_logger):
        """Test that modifying readonly fields triggers a warning"""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance

        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        # Try to modify readonly fields
        attrs.client_sdk_version = "modified"
        attrs.schema_version = "modified"

        # Check warnings were logged
        self.assertEqual(mock_logger_instance.warning.call_count, 2)

        # Values should remain unchanged
        self.assertEqual(attrs.client_sdk_version, __SDK_VERSION__)
        self.assertEqual(attrs.schema_version, __TELEMETRY_SCHEMA_VERSION__)

    # Test set_attributes method
    def test_set_attributes_keywords(self):
        """Test setting multiple attributes at once"""
        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        attrs.set_attributes(
            service_name="new_service",
            service_version="2.0.0",
            os_type="Windows"
        )

        self.assertEqual(attrs.service_name, "new_service")
        self.assertEqual(attrs.service_version, "2.0.0")
        self.assertEqual(attrs.os_type, "Windows")

    def test_set_attributes_dict(self):
        """Test setting multiple attributes at once"""
        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        attrs.set_attributes(
            **{
                "service_name": "new_service",
                "service_version": "2.0.0",
                "os_type": "Windows"
            }
        )

        self.assertEqual(attrs.service_name, "new_service")
        self.assertEqual(attrs.service_version, "2.0.0")
        self.assertEqual(attrs.os_type, "Windows")

    # Test setattr behavior
    @patch('logging.getLogger')
    def test_set_attributes_readonly_warning(self, mock_logger):
        """Test that set_attributes warns for readonly fields"""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance

        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        attrs.set_attributes(client_sdk_version="modified")
        mock_logger_instance.warning.assert_called()

    @patch('logging.getLogger')
    def test_setattr_with_none_value(self, mock_logger):
        """Test that setting None values triggers a warning"""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance

        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        attrs.service_name = None
        mock_logger_instance.warning.assert_called()

    def test_setattr_converts_to_string(self):
        """Test that setattr converts values to strings"""
        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        attrs.service_name = 123
        attrs.service_version = 4.56

        self.assertEqual(attrs.service_name, "123")
        self.assertEqual(attrs.service_version, "4.56")
        self.assertIsInstance(attrs.service_name, str)
        self.assertIsInstance(attrs.service_version, str)

    # Test _get_attributes method
    def test_get_attributes(self):
        """Test _get_attributes returns all attributes except _readonly_fields"""
        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version,
            os_type="Linux",
            os_version="5.4.0"
        )

        attributes_dict = attrs._get_attributes()

        self.assertIn("service_name", attributes_dict)
        self.assertIn("service_version", attributes_dict)
        self.assertIn("os_type", attributes_dict)
        self.assertIn("os_version", attributes_dict)
        self.assertIn("python_version", attributes_dict)
        self.assertIn("hostname", attributes_dict)
        self.assertIn("client_sdk_version", attributes_dict)
        self.assertIn("schema_version", attributes_dict)
        self.assertNotIn("_readonly_fields", attributes_dict)

    # Test helper methods
    def test_get_os_info(self):
        """Test _get_os_info returns tuple of OS type and version"""
        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        os_type, os_version = attrs._get_os_info()

        self.assertIsInstance(os_type, str)
        self.assertIsInstance(os_version, str)
        self.assertTrue(len(os_type) > 0)
        self.assertTrue(len(os_version) > 0)

    def test_get_host_name(self):
        """Test _get_host_name returns hostname"""
        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        hostname = attrs._get_host_name()

        self.assertIsInstance(hostname, str)
        self.assertTrue(len(hostname) > 0)

    def test_invalid_environment(self):
        """Test that __post_init__ properly resets an invalid environment"""
        attrs = ResourceAttributes(
            service_name="test",
            service_version="v1",
            environment="hello"
        )
        self.assertEqual(attrs.environment, "")

        attrs = ResourceAttributes(
            service_name="test",
            service_version="v1",
            environment="tes"
        )
        self.assertEqual(attrs.environment, "")

    # Test regex cases
    def test_empty_string_values_rejection(self):
        """Test behavior with empty string values"""
        with pytest.raises(ValueError) as exc_info:
            attrs = ResourceAttributes(
                service_name="",
                service_version=""
            )

        error_message = str(exc_info.value)
        assert "service_name not set" in error_message
        assert " is invalid regex" in error_message
        assert "This is a required parameter" in error_message

    def test_unicode_values(self):
        """Test behavior with unicode values"""
        with pytest.raises(ValueError) as exc_info:
            _ = ResourceAttributes(
                service_name="测试",
                service_version="1.0.0"
            )

        error_message = str(exc_info.value)
        assert "service_name not set" in error_message
        assert "测试 is invalid regex" in error_message
        assert "This is a required parameter" in error_message

    def test_special_characters_in_values(self):
        """Test behavior with special characters"""
        with pytest.raises(ValueError) as exc_info:
            attrs = ResourceAttributes(
                service_name="test-service_v2///.0",
                service_version="1.0.0-beta+build123"
            )

        error_message = str(exc_info.value)
        assert "service_name not set" in error_message
        assert "test-service_v2///.0 is invalid regex" in error_message
        assert "This is a required parameter" in error_message

    def test_parameters_edit(self):
        """Tests attempted edit of parameters"""
        attrs = ResourceAttributes(
            service_name="test",
            service_version="v1"
        )

        # This should be a no-op with a warning logged
        attrs.parameters = {"foo": "test"}

        assert attrs.parameters == {}

    def test_full_lifecycle(self):
        """Test complete lifecycle of ResourceAttributes instance"""
        # Create instance
        attrs = ResourceAttributes(
            service_name=self.test_service_name,
            service_version=self.test_service_version
        )

        # Modify settable attributes
        attrs.service_name = "updated_service"
        attrs.set_attributes(os_type="Custom OS")

        # Modify dynamic parameters
        attrs.set_attributes(foo="test", foo2="test2")

        # Get all attributes
        all_attrs = attrs._get_attributes()

        # Verify state
        self.assertEqual(attrs.service_name, "updated_service")
        self.assertEqual(attrs.os_type, "Custom OS")
        self.assertIn("python_version", all_attrs)
        self.assertIn("hostname", all_attrs)
        self.assertNotIn('foo', all_attrs)
        self.assertNotIn('foo2', all_attrs)
        self.assertEqual(attrs.parameters['foo'], 'test')
        self.assertEqual(attrs.parameters['foo2'], 'test2')

        # Verify readonly fields unchanged
        self.assertEqual(attrs.client_sdk_version, __SDK_VERSION__)
        self.assertEqual(attrs.schema_version, __TELEMETRY_SCHEMA_VERSION__)
