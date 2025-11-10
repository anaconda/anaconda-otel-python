# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

from test_files.integration_test_services import start_services, stop_services
import requests

def test_span_propogation():
    """Test that carrier propagates trace context through services A->B->C"""
    
    servers = start_services()
    
    try:
        # start nested spans
        response = requests.get('http://localhost:8001/')
        assert response.status_code == 200
        
        result = response.json()
        
        assert 'from' in result
        assert result['from'] == 'A'
        assert 'carrier' in result
        assert 'result' in result
        
        assert result['result']['from'] == 'B'
        assert result['result']['result']['from'] == 'C'
        assert result['result']['result']['done'] == True
        
        assert result['result']['result']['data'] == 'HELLO'
        
    finally:
        stop_services(servers)