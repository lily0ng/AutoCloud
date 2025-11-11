# Authentication System

This is a comprehensive authentication system that provides secure authentication mechanisms for AWS, Linux systems, Web Applications, and APIs.

## Components

1. **AWS Authentication (`aws_auth.py`)**
   - AWS credentials management
   - Session handling
   - Role assumption capabilities
   - Profile-based authentication

2. **Web Authentication (`web_auth.py`)**
   - JWT token-based authentication
   - Password hashing and verification
   - OAuth2 implementation
   - Token expiration and validation

3. **Linux Authentication (`linux_auth.py`)**
   - User management
   - Group management
   - Password management
   - Permission verification

4. **API Authentication (`api_auth.py`)**
   - API key generation and management
   - Request signature validation
   - Redis-based key storage
   - Rate limiting capabilities

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Environment Configuration:
Create a `.env` file with the following variables:
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Usage Examples

### AWS Authentication
```python
from aws_auth import AWSAuthManager

aws_auth = AWSAuthManager()
aws_auth.authenticate_with_credentials(access_key, secret_key)
```

### Web Authentication
```python
from web_auth import WebAuthManager

web_auth = WebAuthManager(secret_key="your-secret-key")
token = web_auth.create_access_token({"sub": "user@example.com"})
```

### Linux Authentication
```python
from linux_auth import LinuxAuthManager

linux_auth = LinuxAuthManager()
linux_auth.create_user("username", "password", ["sudo"])
```

### API Authentication
```python
from api_auth import APIAuthManager

api_auth = APIAuthManager()
keys = api_auth.generate_api_key("client123")
```

## Security Considerations

1. Always use environment variables for sensitive credentials
2. Implement rate limiting for API endpoints
3. Use strong password policies
4. Regularly rotate API keys and access tokens
5. Monitor and log authentication attempts
6. Keep dependencies updated

## Requirements

- Python 3.8+
- Redis server (for API authentication)
- Root privileges (for Linux authentication)
- AWS credentials (for AWS authentication)

## License

MIT License
