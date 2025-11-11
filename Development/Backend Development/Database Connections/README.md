# Database Connections Configuration

This module provides a unified interface for connecting to various databases and cloud services.

## Supported Databases and Services

1. AWS S3
2. MySQL
3. Oracle
4. MongoDB
5. Cassandra
6. Neo4j
7. Redis

## Setup Instructions

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy the environment file and update with your credentials:
   ```bash
   cp .env.example .env
   ```

3. Update the `.env` file with your actual database credentials and connection details.

## Usage Example

```python
from database_config import DatabaseConfig

# Initialize connections
db_config = DatabaseConfig()

# Using MySQL
with db_config.get_mysql_connection() as mysql_conn:
    cursor = mysql_conn.cursor()
    cursor.execute("YOUR QUERY")
    results = cursor.fetchall()

# Upload to S3
db_config.upload_to_s3('your-bucket', 'path/to/local/file', 'destination/path')

# Always close connections when done
db_config.close_all_connections()
```

## Features

- Connection pooling for MySQL and Oracle
- Context managers for safe connection handling
- Automatic connection cleanup
- Environment-based configuration
- Support for multiple database types
- Error handling and logging

## Security Notes

- Never commit the `.env` file with real credentials
- Use appropriate IAM roles and security groups
- Regularly rotate database credentials
- Monitor connection pools and resource usage
