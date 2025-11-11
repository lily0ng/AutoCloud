import pytest
import os
import yaml

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment variables and configurations"""
    # Ensure we're using test configurations
    os.environ['TESTING'] = 'true'
    
    # Load test configuration
    with open('tests/test_config.yaml', 'r') as f:
        test_config = yaml.safe_load(f)
    
    # Set up mock environment variables
    os.environ['AWS_ACCESS_KEY_ID'] = test_config['test_aws']['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = test_config['test_aws']['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = test_config['test_aws']['region']
    
    os.environ['AZURE_SUBSCRIPTION_ID'] = test_config['test_azure']['subscription_id']
    os.environ['AZURE_TENANT_ID'] = test_config['test_azure']['tenant_id']
    os.environ['AZURE_CLIENT_ID'] = test_config['test_azure']['client_id']
    os.environ['AZURE_CLIENT_SECRET'] = test_config['test_azure']['client_secret']
    
    yield
    
    # Clean up environment variables
    os.environ.pop('TESTING', None)
    os.environ.pop('AWS_ACCESS_KEY_ID', None)
    os.environ.pop('AWS_SECRET_ACCESS_KEY', None)
    os.environ.pop('AWS_DEFAULT_REGION', None)
    os.environ.pop('AZURE_SUBSCRIPTION_ID', None)
    os.environ.pop('AZURE_TENANT_ID', None)
    os.environ.pop('AZURE_CLIENT_ID', None)
    os.environ.pop('AZURE_CLIENT_SECRET', None)
