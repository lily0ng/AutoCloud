import azure.functions as func
import json
from datetime import datetime

app = func.FunctionApp()

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure HTTP triggered function
    """
    try:
        req_body = req.get_json()
        message = req_body.get('message', 'No message provided')
        
        response_data = {
            'message': f'Processed message: {message}',
            'timestamp': datetime.utcnow().isoformat(),
            'provider': 'Azure Functions'
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({'error': str(e)}),
            status_code=500
        )

@app.blob_trigger(arg_name="myblob", 
                 path="samples-workitems/{name}",
                 connection="AzureStorageConnectionString")
def blob_trigger(myblob: func.InputStream):
    """
    Azure Blob Storage triggered function
    """
    try:
        print(f"Python blob trigger function processed blob \n"
              f"Name: {myblob.name}\n"
              f"Size: {myblob.length} bytes")
    except Exception as e:
        print(f"Error processing blob: {str(e)}")
