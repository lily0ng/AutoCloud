# Service Restarts and Maintenance Automation

An automated service management and monitoring system that handles process restarts, maintenance, and health checks.

## Features

1. Automated service monitoring and restart
2. Health check system
3. Detailed logging with rotation
4. Email notifications for critical events
5. Custom restart policies
6. Service dependency management
7. Maintenance window scheduling
8. Performance metrics collection
9. Multi-OS support (Linux, Windows, macOS)
10. REST API for remote management

## Supported Services

<div align="center">
  <img src="https://img.shields.io/badge/Apache-D22128?style=for-the-badge&logo=Apache&logoColor=white" alt="Apache"/>
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx"/>
  <img src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white" alt="Redis"/>
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB"/>
  <img src="https://img.shields.io/badge/rabbitmq-%23FF6600.svg?&style=for-the-badge&logo=rabbitmq&logoColor=white" alt="RabbitMQ"/>
  <img src="https://img.shields.io/badge/Elastic_Search-005571?style=for-the-badge&logo=elasticsearch&logoColor=white" alt="Elasticsearch"/>
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=Jenkins&logoColor=white" alt="Jenkins"/>
  <img src="https://img.shields.io/badge/kubernetes-326ce5.svg?&style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes"/>
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white" alt="Prometheus"/>
  <img src="https://img.shields.io/badge/Grafana-F2F4F9?style=for-the-badge&logo=grafana&logoColor=orange" alt="Grafana"/>
  <img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white" alt="Kafka"/>
  <img src="https://img.shields.io/badge/Apache_Tomcat-F8DC75?style=for-the-badge&logo=apache-tomcat&logoColor=black" alt="Tomcat"/>
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js"/>
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python"/>
  <img src="https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white" alt="Java"/>
</div>

1. Apache Web Server
2. Nginx
3. MySQL/MariaDB
4. PostgreSQL
5. Redis
6. MongoDB
7. RabbitMQ
8. Elasticsearch
9. Docker daemon
10. Jenkins
11. Kubernetes services
12. Prometheus
13. Grafana
14. Zookeeper
15. Kafka
16. Tomcat
17. Node.js applications
18. Python web services
19. Java applications
20. Custom user-defined services

## Supported Operating Systems

<div align="center">
  <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu"/>
  <img src="https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white" alt="Debian"/>
  <img src="https://img.shields.io/badge/Red%20Hat-EE0000?style=for-the-badge&logo=redhat&logoColor=white" alt="Red Hat"/>
  <img src="https://img.shields.io/badge/Cent%20OS-262577?style=for-the-badge&logo=CentOS&logoColor=white" alt="CentOS"/>
  <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows"/>
  <img src="https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white" alt="macOS"/>
</div>

- Linux (Ubuntu, CentOS, RHEL, Debian)
- Windows Server
- macOS

## Requirements

- Python 3.8+
- psutil
- systemd (for Linux)
- supervisor
- requests
- pyyaml
- schedule

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit the `config.yaml` file to set up your services and notification preferences.

## Usage

```bash
python service_monitor.py
```

## Logging

Logs are stored in `/var/log/service-monitor/` with automatic rotation.

## Contributing

Contributions are welcome! Please read our contributing guidelines.
