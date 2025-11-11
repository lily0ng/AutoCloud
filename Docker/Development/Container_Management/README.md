# Container Management Tool

A comprehensive Python-based tool for managing both Docker containers locally and AWS container services (ECS/ECR).

## Features

- Local Docker container management
- AWS ECS cluster management
- ECR image pushing
- Container resource monitoring
- Command-line interface for easy interaction

## Installation

1. Clone the repository
2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Copy `.env.template` to `.env` and fill in your AWS credentials:

```bash
cp .env.template .env
```

## Usage

### List Local Containers

```bash
python container_manager.py list-containers
```

### List ECS Clusters

```bash
python container_manager.py list-clusters

```

### Manage Local Container

```bash
python container_manager.py container [start|stop|remove] CONTAINER_ID
```

### Deploy to ECS

```bash
python container_manager.py deploy-ecs TASK_DEFINITION CLUSTER_NAME
```

### Push Image to ECR

```bash
python container_manager.py push-ecr IMAGE_NAME REPOSITORY_NAME
```

### Monitor Container Resources

```bash
python container_manager.py monitor
```

## Environment Variables

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: AWS region (default: us-east-1)
- `AWS_SUBNET_ID`: Subnet ID for ECS tasks
- `AWS_SECURITY_GROUP`: Security group for ECS tasks
- `DOCKER_HOST`: Docker daemon socket

## Security Notes

- Never commit your `.env` file with real credentials
- Use IAM roles and policies with least privilege
- Regularly rotate AWS credentials
- Monitor container resource usage

## Error Handling

The tool includes comprehensive error handling for:
- Docker daemon connection issues
- AWS API errors
- Network connectivity problems
- Resource constraints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
