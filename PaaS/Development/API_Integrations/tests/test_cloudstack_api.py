import pytest
from unittest.mock import Mock, patch
import yaml
from src.cloudstack.cloudstack_api import CloudStackIntegration

@pytest.fixture
def config():
    with open('tests/test_config.yaml', 'r') as f:
        return yaml.safe_load(f)['test_cloudstack']

@pytest.fixture
def cloudstack_client(config):
    with patch('src.cloudstack.cloudstack_api.get_driver') as mock_get_driver:
        mock_driver = Mock()
        mock_get_driver.return_value = mock_driver
        client = CloudStackIntegration('tests/test_config.yaml')
        return client, mock_driver

def test_list_virtual_machines(cloudstack_client):
    client, mock_driver = cloudstack_client
    mock_vm = Mock()
    mock_vm.id = 'test-vm-id'
    mock_vm.name = 'test-vm'
    mock_driver.list_nodes.return_value = [mock_vm]
    
    vms = client.list_virtual_machines()
    assert len(vms) == 1
    assert vms[0].id == 'test-vm-id'
    assert vms[0].name == 'test-vm'

def test_create_kvm_instance(cloudstack_client):
    client, mock_driver = cloudstack_client
    mock_size = Mock()
    mock_image = Mock()
    mock_vm = Mock()
    mock_vm.id = 'new-vm-id'
    
    mock_driver.create_node.return_value = mock_vm
    
    result = client.create_kvm_instance(
        name='test-vm',
        size=mock_size,
        image=mock_image
    )
    
    assert result.id == 'new-vm-id'
    mock_driver.create_node.assert_called_once_with(
        name='test-vm',
        size=mock_size,
        image=mock_image,
        location=None,
        ex_hypervisor='KVM'
    )

def test_get_instance_status(cloudstack_client):
    client, mock_driver = cloudstack_client
    mock_vm = Mock()
    mock_vm.id = 'test-vm-id'
    mock_vm.state = 'running'
    mock_driver.list_nodes.return_value = [mock_vm]
    
    status = client.get_instance_status('test-vm-id')
    assert status == 'running'
