#!/usr/bin/env python3

import boto3
from azure.mgmt.consumption import ConsumptionManagementClient
from datetime import datetime, timedelta
import yaml

class CloudBillingIntegration:
    def __init__(self, config_path='config/credentials.yaml'):
        """Initialize billing clients for different cloud providers"""
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # AWS Cost Explorer
        self.aws_ce = boto3.client(
            'ce',
            aws_access_key_id=config['aws']['access_key'],
            aws_secret_access_key=config['aws']['secret_key'],
            region_name=config['aws']['region']
        )
        
        # Azure Consumption
        azure_credentials = config['azure']
        self.azure_consumption = ConsumptionManagementClient(
            credentials=azure_credentials['credentials'],
            subscription_id=azure_credentials['subscription_id']
        )

    def get_aws_costs(self, start_date, end_date):
        """Get AWS costs for a specific time period"""
        try:
            response = self.aws_ce.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='MONTHLY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                    {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}
                ]
            )
            return response['ResultsByTime']
        except Exception as e:
            print(f"Error getting AWS costs: {e}")
            return None

    def get_azure_costs(self, start_date, end_date):
        """Get Azure costs for a specific time period"""
        try:
            costs = self.azure_consumption.usage_details.list(
                scope=f"/subscriptions/{self.azure_subscription_id}",
                filter=f"usageStart ge '{start_date}' and usageEnd le '{end_date}'"
            )
            return list(costs)
        except Exception as e:
            print(f"Error getting Azure costs: {e}")
            return None

    def get_consolidated_billing(self, start_date=None, end_date=None):
        """Get consolidated billing across all cloud providers"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        billing_data = {
            'aws': self.get_aws_costs(start_date, end_date),
            'azure': self.get_azure_costs(start_date, end_date)
        }

        return billing_data

    def get_resource_costs(self, resource_id, provider):
        """Get costs for a specific resource"""
        if provider.lower() == 'aws':
            try:
                response = self.aws_ce.get_cost_and_usage(
                    TimePeriod={
                        'Start': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                        'End': datetime.now().strftime('%Y-%m-%d')
                    },
                    Granularity='DAILY',
                    Metrics=['UnblendedCost'],
                    Filter={
                        'Dimensions': {
                            'Key': 'RESOURCE_ID',
                            'Values': [resource_id]
                        }
                    }
                )
                return response['ResultsByTime']
            except Exception as e:
                print(f"Error getting AWS resource costs: {e}")
                return None
        
        elif provider.lower() == 'azure':
            try:
                costs = self.azure_consumption.usage_details.list(
                    scope=f"/subscriptions/{self.azure_subscription_id}",
                    filter=f"resourceId eq '{resource_id}'"
                )
                return list(costs)
            except Exception as e:
                print(f"Error getting Azure resource costs: {e}")
                return None
        
        return None
