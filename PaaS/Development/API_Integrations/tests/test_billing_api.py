import pytest
from unittest.mock import Mock, patch
import yaml
from datetime import datetime, timedelta
from src.billing.billing_api import CloudBillingIntegration

@pytest.fixture
def config():
    with open('tests/test_config.yaml', 'r') as f:
        return yaml.safe_load(f)

@pytest.fixture
def billing_client():
    with patch('src.billing.billing_api.boto3') as mock_boto3, \
         patch('src.billing.billing_api.ConsumptionManagementClient') as mock_azure:
        client = CloudBillingIntegration('tests/test_config.yaml')
        return client, mock_boto3, mock_azure

def test_get_aws_costs(billing_client):
    client, mock_boto3, _ = billing_client
    mock_ce = Mock()
    mock_boto3.client.return_value = mock_ce
    
    start_date = '2024-01-01'
    end_date = '2024-01-31'
    
    mock_response = {
        'ResultsByTime': [
            {
                'TimePeriod': {'Start': start_date, 'End': end_date},
                'Groups': [
                    {
                        'Keys': ['AWS Lambda', 'Lambda-GB-Second'],
                        'Metrics': {'UnblendedCost': {'Amount': '10.0', 'Unit': 'USD'}}
                    }
                ]
            }
        ]
    }
    mock_ce.get_cost_and_usage.return_value = mock_response
    
    result = client.get_aws_costs(start_date, end_date)
    assert result == mock_response['ResultsByTime']
    mock_ce.get_cost_and_usage.assert_called_once()

def test_get_azure_costs(billing_client):
    client, _, mock_azure = billing_client
    mock_consumption = Mock()
    mock_azure.return_value = mock_consumption
    
    start_date = '2024-01-01'
    end_date = '2024-01-31'
    
    mock_costs = [
        {'id': 'cost1', 'name': 'VM Usage', 'type': 'Usage', 'properties': {'cost': 100.0}},
        {'id': 'cost2', 'name': 'Storage', 'type': 'Usage', 'properties': {'cost': 50.0}}
    ]
    mock_consumption.usage_details.list.return_value = mock_costs
    
    result = client.get_azure_costs(start_date, end_date)
    assert result == mock_costs
    mock_consumption.usage_details.list.assert_called_once()

def test_get_consolidated_billing(billing_client):
    client, mock_boto3, mock_azure = billing_client
    
    # Mock AWS costs
    mock_ce = Mock()
    mock_boto3.client.return_value = mock_ce
    mock_aws_response = {
        'ResultsByTime': [
            {
                'TimePeriod': {'Start': '2024-01-01', 'End': '2024-01-31'},
                'Groups': [
                    {
                        'Keys': ['AWS Lambda'],
                        'Metrics': {'UnblendedCost': {'Amount': '10.0', 'Unit': 'USD'}}
                    }
                ]
            }
        ]
    }
    mock_ce.get_cost_and_usage.return_value = mock_aws_response
    
    # Mock Azure costs
    mock_consumption = Mock()
    mock_azure.return_value = mock_consumption
    mock_azure_costs = [
        {'id': 'cost1', 'name': 'VM Usage', 'properties': {'cost': 100.0}}
    ]
    mock_consumption.usage_details.list.return_value = mock_azure_costs
    
    result = client.get_consolidated_billing()
    assert 'aws' in result
    assert 'azure' in result
    assert result['aws'] == mock_aws_response['ResultsByTime']
    assert result['azure'] == mock_azure_costs
