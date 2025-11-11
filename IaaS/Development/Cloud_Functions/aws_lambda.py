import json
import boto3
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    AWS Lambda function handler
    """
    try:
        # Parse the incoming event
        body = json.loads(event.get('body', '{}'))
        
        # Process the request
        message = body.get('message', 'No message provided')
        
        # You can add your business logic here
        response_data = {
            'message': f'Processed message: {message}',
            'timestamp': datetime.utcnow().isoformat(),
            'provider': 'AWS Lambda'
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

# Example of working with AWS services
def process_s3_event(event, context):
    """
    Process S3 events
    """
    s3_client = boto3.client('s3')
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Process the S3 object
        try:
            response = s3_client.get_object(Bucket=bucket, Key=key)
            print(f"Processing file {key} from bucket {bucket}")
        except Exception as e:
            print(f"Error processing S3 object: {str(e)}")
