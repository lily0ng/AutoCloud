#!/usr/bin/env python3

import docker
import json
import subprocess
import os
import logging
from datetime import datetime
import requests
import yaml
from typing import Dict, List, Any

class DockerSecurityAnalyzer:
    def __init__(self):
        self.client = docker.from_env()
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('docker_security_analysis.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def analyze_container_security(self) -> Dict[str, Any]:
        """
        Method 1: Analyze running containers for security configurations
        Checks for:
        - Root user usage
        - Privileged containers
        - Port mappings
        - Mount points
        - Security options
        """
        security_report = {}
        try:
            containers = self.client.containers.list()
            for container in containers:
                container_info = container.attrs
                security_report[container.name] = {
                    'running_as_root': container_info['Config']['User'] == '' or container_info['Config']['User'] == 'root',
                    'privileged': container_info['HostConfig']['Privileged'],
                    'port_bindings': container_info['HostConfig']['PortBindings'],
                    'mount_points': container_info['Mounts'],
                    'security_opts': container_info['HostConfig']['SecurityOpt'],
                    'capabilities': container_info['HostConfig']['CapAdd'],
                    'read_only_root_fs': container_info['HostConfig']['ReadonlyRootfs']
                }
        except Exception as e:
            self.logger.error(f"Error analyzing container security: {str(e)}")
        return security_report

    def analyze_image_vulnerabilities(self, image_name: str) -> Dict[str, Any]:
        """
        Method 2: Analyze Docker images for vulnerabilities
        Uses Trivy (if installed) for scanning
        """
        try:
            # Check if Trivy is installed
            subprocess.run(['trivy', '--version'], check=True, capture_output=True)
            
            # Run Trivy scan
            result = subprocess.run(
                ['trivy', 'image', '--format', 'json', image_name],
                capture_output=True,
                text=True
            )
            
            return json.loads(result.stdout)
        except subprocess.CalledProcessError:
            self.logger.error("Trivy is not installed or encountered an error")
            return {"error": "Trivy scanner not available"}
        except Exception as e:
            self.logger.error(f"Error scanning image: {str(e)}")
            return {"error": str(e)}

    def analyze_docker_compose(self, compose_file: str) -> Dict[str, Any]:
        """
        Method 3: Analyze Docker Compose file for security configurations
        Checks for:
        - Security options
        - Network configurations
        - Volume mounts
        - Environment variables
        """
        security_issues = {
            'services': {},
            'networks': {},
            'volumes': {}
        }

        try:
            with open(compose_file, 'r') as f:
                compose_config = yaml.safe_load(f)

            for service_name, service_config in compose_config.get('services', {}).items():
                security_issues['services'][service_name] = {
                    'privileged': service_config.get('privileged', False),
                    'ports_exposed': service_config.get('ports', []),
                    'volumes': service_config.get('volumes', []),
                    'security_opt': service_config.get('security_opt', []),
                    'environment': bool(service_config.get('environment', {})),
                    'capabilities': service_config.get('cap_add', [])
                }

        except Exception as e:
            self.logger.error(f"Error analyzing docker-compose file: {str(e)}")
        
        return security_issues

    def analyze_docker_daemon_config(self) -> Dict[str, Any]:
        """
        Method 4: Analyze Docker daemon configuration
        Checks for:
        - TLS configuration
        - Authorization plugins
        - Logging configuration
        - Security options
        """
        daemon_config_path = '/etc/docker/daemon.json'
        security_config = {}

        try:
            if os.path.exists(daemon_config_path):
                with open(daemon_config_path, 'r') as f:
                    config = json.load(f)
                    
                security_config = {
                    'tls_enabled': bool(config.get('tls', False)),
                    'userns_remap': config.get('userns-remap', 'none'),
                    'seccomp_profile': bool(config.get('seccomp-profile', False)),
                    'selinux_enabled': bool(config.get('selinux-enabled', False)),
                    'live_restore': bool(config.get('live-restore', False)),
                    'debug': bool(config.get('debug', False)),
                    'authorization_plugins': config.get('authorization-plugins', [])
                }
        except Exception as e:
            self.logger.error(f"Error analyzing daemon configuration: {str(e)}")

        return security_config

    def analyze_network_security(self) -> Dict[str, Any]:
        """
        Method 5: Analyze Docker network security
        Checks for:
        - Network isolation
        - Network encryption
        - Open ports
        - Network policies
        """
        network_security = {}
        
        try:
            networks = self.client.networks.list()
            for network in networks:
                network_info = network.attrs
                network_security[network.name] = {
                    'driver': network_info['Driver'],
                    'internal': network_info['Internal'],
                    'enable_ipv6': network_info['EnableIPv6'],
                    'encrypted': network_info.get('Options', {}).get('encrypted', 'false'),
                    'containers': list(network_info.get('Containers', {}).keys()),
                    'ipam_config': network_info['IPAM']['Config']
                }
        except Exception as e:
            self.logger.error(f"Error analyzing network security: {str(e)}")

        return network_security

    def generate_security_report(self, output_file: str = 'security_report.json'):
        """
        Generate a comprehensive security report combining all analyses
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'container_security': self.analyze_container_security(),
            'daemon_config': self.analyze_docker_daemon_config(),
            'network_security': self.analyze_network_security()
        }

        # Add compose file analysis if exists
        if os.path.exists('docker-compose.yml'):
            report['compose_security'] = self.analyze_docker_compose('docker-compose.yml')

        # Save report
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=4)
            self.logger.info(f"Security report generated: {output_file}")
        except Exception as e:
            self.logger.error(f"Error saving security report: {str(e)}")

def main():
    analyzer = DockerSecurityAnalyzer()
    
    # Generate comprehensive security report
    analyzer.generate_security_report()
    
    # Example of scanning a specific image
    if len(analyzer.client.images.list()) > 0:
        image_name = analyzer.client.images.list()[0].tags[0]
        vulnerabilities = analyzer.analyze_image_vulnerabilities(image_name)
        print(f"Vulnerabilities for {image_name}:", json.dumps(vulnerabilities, indent=2))

if __name__ == "__main__":
    main()
