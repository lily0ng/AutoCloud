import pytest
from unittest.mock import Mock, patch
import yaml
from src.azure.azure_api import AzureIntegration

@pytest.fixture
def config():
    with open('tests/test_config.yaml', 'r') as f:
        return yaml.safe_load(f)['test_azure']

@pytest.fixture
def azure_client(config):
    with patch('src.azure.azure_api.ComputeManagementClient') as mock_compute, \
         patch('src.azure.azure_api.NetworkManagementClient') as mock_network, \
         patch('src.azure.azure_api.ResourceManagementClient') as mock_resource:
        
        client = AzureIntegration('tests/test_config.yaml')
        return client, mock_compute, mock_network, mock_resource

def test_list_virtual_machines(azure_client, config):
    client, mock_compute, _, _ = azure_client
    mock_vm = Mock()
    mock_vm.name = 'test-vm'
    mock_compute.return_value.virtual_machines.list.return_value = [mock_vm]
    
    vms = client.list_virtual_machines(config['test_resource_group'])
    assert len(list(vms)) == 1
    assert next(vms).name == 'test-vm'

def test_create_vm(azure_client, config):
    client, mock_compute, _, _ = azure_client
    mock_operation = Mock()
    mock_compute.return_value.virtual_machines.begin_create_or_update.return_value = mock_operation
    
    image_reference = {
        'publisher': 'Canonical',
        'offer': 'UbuntuServer',
        'sku': '18.04-LTS',
        'version': 'latest'
    }
    
    result = client.create_vm(
        config['test_resource_group'],
        config['test_vm_name'],
        config['test_location'],
        config['test_vm_size'],
        image_reference
    )
    
    assert result == mock_operation
    mock_compute.return_value.virtual_machines.begin_create_or_update.assert_called_once()

def test_start_vm(azure_client, config):
    client, mock_compute, _, _ = azure_client
    mock_operation = Mock()
    mock_compute.return_value.virtual_machines.begin_start.return_value = mock_operation
    
    result = client.start_vm(config['test_resource_group'], config['test_vm_name'])
    assert result == mock_operation

def test_stop_vm(azure_client, config):
    client, mock_compute, _, _ = azure_client
    mock_operation = Mock()
    mock_compute.return_value.virtual_machines.begin_deallocate.return_value = mock_operation
    
    result = client.stop_vm(config['test_resource_group'], config['test_vm_name'])
    assert result == mock_operation

def test_get_vm_status(azure_client, config):
    client, mock_compute, _, _ = azure_client
    mock_status = Mock()
    mock_status.statuses = [Mock(display_status='VM running')]
    mock_compute.return_value.virtual_machines.instance_view.return_value = mock_status
    
    result = client.get_vm_status(config['test_resource_group'], config['test_vm_name'])
    assert result.statuses[0].display_status == 'VM running'
