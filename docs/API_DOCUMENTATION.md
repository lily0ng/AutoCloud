# AutoCloud API Documentation

## Overview
AutoCloud REST API for managing cloud deployments across multiple providers.

## Base URL
```
https://api.autocloud.io/v1
```

## Authentication
All API requests require authentication using Bearer tokens:
```
Authorization: Bearer YOUR_API_TOKEN
```

## Endpoints

### Deployments

#### List Deployments
```http
GET /deployments
```

**Query Parameters:**
- `environment` (optional): Filter by environment (dev, staging, prod)
- `status` (optional): Filter by status
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20)

**Response:**
```json
{
  "deployments": [...],
  "total": 100,
  "page": 1,
  "limit": 20
}
```

#### Create Deployment
```http
POST /deployments
```

**Request Body:**
```json
{
  "name": "my-deployment",
  "environment": "production",
  "provider": "aws",
  "region": "us-east-1",
  "config": {}
}
```

#### Get Deployment
```http
GET /deployments/{id}
```

#### Update Deployment
```http
PUT /deployments/{id}
```

#### Delete Deployment
```http
DELETE /deployments/{id}
```

#### Scale Deployment
```http
POST /deployments/{id}/scale
```

**Request Body:**
```json
{
  "replicas": 5
}
```

## Error Responses

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {}
}
```

## Rate Limiting
- 1000 requests per hour per API key
- Rate limit headers included in responses

## Webhooks
Configure webhooks to receive deployment events.

## SDKs
- Python: `pip install autocloud-sdk`
- Node.js: `npm install @autocloud/sdk`
- Go: `go get github.com/autocloud/sdk-go`
