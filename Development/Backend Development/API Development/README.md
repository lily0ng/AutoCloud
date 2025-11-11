# Cloud API Service

A comprehensive API service for cloud and web applications, built with FastAPI.

## Features

- EC2 instance management
- S3 bucket operations
- RDS backup functionality
- Health monitoring
- Secure authentication
- Cross-origin resource sharing (CORS) support

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual configuration
```

4. Run the application:
```bash
uvicorn app.main:app --reload --port 8000
```

## API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check
- GET `/health` - Check API health status

### Cloud Operations
- GET `/cloud/ec2/instances` - List EC2 instances
- GET `/cloud/s3/buckets` - List S3 buckets
- POST `/cloud/backup/{resource_type}/{resource_id}` - Create backup

## Security

- JWT authentication
- Environment variable configuration
- AWS IAM role-based access

## Development

To contribute to this project:

1. Create a new branch
2. Make your changes
3. Submit a pull request

## License

MIT License
