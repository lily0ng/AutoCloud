import pytest
import boto3
from moto import mock_ec2, mock_pricing
from src.aws.aws_api import AWSIntegration
import yaml

@pytest.fixture
def config():
    with open('tests/test_config.yaml', 'r') as f:
        return yaml.safe_load(f)['test_aws']

@pytest.fixture
def aws_client(config):
    with mock_ec2():
        client = AWSIntegration('tests/test_config.yaml')
        return client

def test_list_instances(aws_client):
    instances = aws_client.list_instances()
    assert isinstance(instances, list)

@mock_ec2
def test_create_instance(aws_client, config):
    response = aws_client.create_instance(
        ami_id=config['test_ami_id'],
        instance_type='t2.micro',
        key_name=config['test_key_name'],
        subnet_id=config['test_subnet_id']
    )
    assert response is not None
    assert 'InstanceId' in response

@mock_ec2
def test_stop_instance(aws_client, config):
    # First create an instance
    instance = aws_client.create_instance(
        ami_id=config['test_ami_id'],
        instance_type='t2.micro',
        key_name=config['test_key_name']
    )
    instance_id = instance['InstanceId']
    
    # Then stop it
    result = aws_client.stop_instance(instance_id)
    assert result is True

@mock_ec2
def test_start_instance(aws_client, config):
    # First create and stop an instance
    instance = aws_client.create_instance(
        ami_id=config['test_ami_id'],
        instance_type='t2.micro',
        key_name=config['test_key_name']
    )
    instance_id = instance['InstanceId']
    aws_client.stop_instance(instance_id)
    
    # Then start it
    result = aws_client.start_instance(instance_id)
    assert result is True

@mock_pricing
def test_get_instance_price(aws_client):
    price_info = aws_client.get_instance_price('t2.micro')
    assert price_info is not None
