import json
import oss2
from datetime import datetime
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException

def handler(event, context):
    """
    Alibaba Cloud Function Compute handler
    """
    try:
        evt = json.loads(event)
        message = evt.get('message', 'No message provided')
        
        response_data = {
            'message': f'Processed message: {message}',
            'timestamp': datetime.utcnow().isoformat(),
            'provider': 'Alibaba Cloud Function Compute'
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
            'body': json.dumps({'error': str(e)})
        }

def oss_trigger_handler(event, context):
    """
    Alibaba Cloud OSS trigger handler
    """
    try:
        evt = json.loads(event)
        for record in evt.get('events', []):
            bucket_name = record['oss']['bucket']['name']
            object_name = record['oss']['object']['key']
            
            # Initialize OSS client
            auth = oss2.Auth(context.credentials.access_key_id,
                           context.credentials.access_key_secret)
            bucket = oss2.Bucket(auth, 
                               f'https://{bucket_name}.{context.region}.aliyuncs.com',
                               bucket_name)
            
            print(f"Processing OSS object: {object_name} from bucket: {bucket_name}")
            
    except Exception as e:
        print(f"Error processing OSS event: {str(e)}")
