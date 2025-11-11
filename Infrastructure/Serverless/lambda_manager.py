"""
AWS Lambda function management
"""
import boto3
import zipfile
import os
from typing import Dict, List


class LambdaManager:
    """Manage Lambda functions"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.region = region
    
    def create_function(self, function_name: str, runtime: str, handler: str,
                       role_arn: str, code_path: str, environment_vars: Dict = None,
                       timeout: int = 30, memory_size: int = 512):
        """Create Lambda function"""
        try:
            # Create deployment package
            zip_path = self._create_deployment_package(code_path)
            
            with open(zip_path, 'rb') as f:
                zip_content = f.read()
            
            config = {
                'FunctionName': function_name,
                'Runtime': runtime,
                'Role': role_arn,
                'Handler': handler,
                'Code': {'ZipFile': zip_content},
                'Timeout': timeout,
                'MemorySize': memory_size
            }
            
            if environment_vars:
                config['Environment'] = {'Variables': environment_vars}
            
            response = self.lambda_client.create_function(**config)
            
            # Clean up zip file
            os.remove(zip_path)
            
            return response['FunctionArn']
        except Exception as e:
            raise Exception(f"Failed to create function: {str(e)}")
    
    def _create_deployment_package(self, code_path: str) -> str:
        """Create deployment package zip"""
        zip_path = '/tmp/lambda_deployment.zip'
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isfile(code_path):
                zipf.write(code_path, os.path.basename(code_path))
            else:
                for root, dirs, files in os.walk(code_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, code_path)
                        zipf.write(file_path, arcname)
        
        return zip_path
    
    def invoke_function(self, function_name: str, payload: Dict = None):
        """Invoke Lambda function"""
        try:
            import json
            
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload or {})
            )
            
            return json.loads(response['Payload'].read())
        except Exception as e:
            raise Exception(f"Failed to invoke function: {str(e)}")
    
    def update_function_code(self, function_name: str, code_path: str):
        """Update function code"""
        try:
            zip_path = self._create_deployment_package(code_path)
            
            with open(zip_path, 'rb') as f:
                zip_content = f.read()
            
            self.lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_content
            )
            
            os.remove(zip_path)
            return True
        except Exception as e:
            raise Exception(f"Failed to update function code: {str(e)}")
    
    def add_permission(self, function_name: str, statement_id: str,
                      principal: str, source_arn: str = None):
        """Add permission to Lambda function"""
        try:
            params = {
                'FunctionName': function_name,
                'StatementId': statement_id,
                'Action': 'lambda:InvokeFunction',
                'Principal': principal
            }
            
            if source_arn:
                params['SourceArn'] = source_arn
            
            self.lambda_client.add_permission(**params)
            return True
        except Exception as e:
            raise Exception(f"Failed to add permission: {str(e)}")
