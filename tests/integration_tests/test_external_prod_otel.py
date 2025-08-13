import subprocess

def test_otel_metric_export_silent():
    """Test that metric export produces no output when successful"""
    
    result = subprocess.run(
        [
            'python', '-c', '''from tests.integration_tests.test_files.integration_test_app import IntegrationTestApp
app = IntegrationTestApp()'''
        ],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    # Success = absolutely no output
    assert result.stdout == "", f"Unexpected stdout: {result.stdout}"
    assert result.stderr == "", f"Unexpected stderr: {result.stderr}"
    assert result.returncode == 0