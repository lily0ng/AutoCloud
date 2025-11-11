# Multi-Cloud Functions

This project contains serverless function implementations for multiple cloud providers:
- AWS Lambda
- Google Cloud Functions
- Azure Functions
- Alibaba Cloud Function Compute

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
- Copy `.env.example` to `.env`
- Fill in your cloud provider credentials

## Cloud Provider Specific Setup

### AWS Lambda
- Create a new Lambda function in AWS Console
- Upload the `aws_lambda.py` code
- Configure IAM roles and permissions
- Set environment variables

### Google Cloud Functions
- Enable Cloud Functions API
- Deploy using gcloud CLI:
```bash
gcloud functions deploy http_function --runtime python39 --trigger-http
```

### Azure Functions
- Create a Function App in Azure Portal
- Deploy using Azure Functions Core Tools:
```bash
func azure functionapp publish YOUR_FUNCTION_APP_NAME
```

### Alibaba Cloud Function Compute
- Create a service in Function Compute Console
- Create a function and upload `aliyun_function.py`
- Configure triggers and permissions

## Function Endpoints

Each function provides an HTTP endpoint that:
- Accepts JSON payload with a "message" field
- Returns processed message with timestamp
- Includes cloud provider identification

## Storage Event Triggers

Each implementation includes handlers for cloud storage events:
- AWS: S3 event processing
- GCP: Cloud Storage event processing
- Azure: Blob Storage triggers
- Alibaba: OSS event triggers

## Security

- Never commit `.env` file with actual credentials
- Use appropriate IAM roles and permissions
- Regularly rotate access keys
- Monitor function execution and set up logging

## Error Handling

All functions include:
- JSON payload validation
- Error response formatting
- Exception handling
- Logging capabilities
