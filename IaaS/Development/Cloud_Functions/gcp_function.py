import functions_framework
from datetime import datetime
import json
from google.cloud import storage

@functions_framework.http
def http_function(request):
    """
    HTTP Cloud Function.
    """
    try:
        request_json = request.get_json(silent=True)
        
        if request_json and 'message' in request_json:
            message = request_json['message']
        else:
            message = 'No message provided'
            
        response_data = {
            'message': f'Processed message: {message}',
            'timestamp': datetime.utcnow().isoformat(),
            'provider': 'Google Cloud Functions'
        }
        
        return json.dumps(response_data), 200, {'Content-Type': 'application/json'}
        
    except Exception as e:
        return json.dumps({'error': str(e)}), 500, {'Content-Type': 'application/json'}

@functions_framework.cloud_event
def process_storage_event(cloud_event):
    """
    Process Google Cloud Storage events
    """
    data = cloud_event.data

    event_type = cloud_event["type"]
    bucket_name = data["bucket"]
    file_name = data["name"]

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    try:
        print(f"Processing file {file_name} from bucket {bucket_name}")
        # Add your processing logic here
    except Exception as e:
        print(f"Error processing file: {str(e)}")
