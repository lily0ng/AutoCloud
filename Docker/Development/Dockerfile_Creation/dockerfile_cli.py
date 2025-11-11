#!/usr/bin/env python3

import click
import os
import sys
from typing import Dict, List, Optional

class DockerfileGenerator:
    def __init__(self):
        self.instructions: List[str] = []
        self.base_images = {
            'python': ['python:3.9', 'python:3.8-slim', 'python:3.9-alpine'],
            'node': ['node:16', 'node:16-alpine', 'node:14-slim'],
            'golang': ['golang:1.17', 'golang:1.17-alpine'],
            'java': ['openjdk:11', 'openjdk:11-slim', 'openjdk:8']
        }

    def add_base_image(self, image: str) -> None:
        self.instructions.append(f"FROM {image}")

    def add_workdir(self, directory: str) -> None:
        self.instructions.append(f"WORKDIR {directory}")

    def add_copy(self, src: str, dest: str) -> None:
        self.instructions.append(f"COPY {src} {dest}")

    def add_run(self, command: str) -> None:
        self.instructions.append(f"RUN {command}")

    def add_env(self, key: str, value: str) -> None:
        self.instructions.append(f"ENV {key}={value}")

    def add_expose(self, port: int) -> None:
        self.instructions.append(f"EXPOSE {port}")

    def add_cmd(self, command: str) -> None:
        self.instructions.append(f"CMD {command}")

    def generate(self) -> str:
        return "\n".join(self.instructions)

@click.group()
def cli():
    """Docker File Generator CLI - Create Dockerfiles interactively"""
    pass

@cli.command()
@click.option('--type', 'app_type', type=click.Choice(['python', 'node', 'golang', 'java']), 
              prompt='Select application type', help='Type of application')
@click.option('--port', type=int, prompt='Port to expose', help='Port number to expose')
@click.option('--cmd', prompt='Command to run', help='Command to run the application')
@click.option('--output', default='Dockerfile', help='Output file name')
def create(app_type: str, port: int, cmd: str, output: str):
    """Create a new Dockerfile interactively"""
    generator = DockerfileGenerator()
    
    # Select base image
    click.echo("\nAvailable base images:")
    for idx, image in enumerate(generator.base_images[app_type], 1):
        click.echo(f"{idx}. {image}")
    
    image_choice = click.prompt(
        "Select base image number",
        type=click.IntRange(1, len(generator.base_images[app_type]))
    )
    base_image = generator.base_images[app_type][image_choice - 1]
    
    # Generate Dockerfile
    generator.add_base_image(base_image)
    generator.add_workdir("/app")
    generator.add_copy(".", ".")
    
    # Add language-specific commands
    if app_type == 'python':
        generator.add_run("pip install -r requirements.txt")
    elif app_type == 'node':
        generator.add_run("npm install")
    elif app_type == 'golang':
        generator.add_run("go mod download")
    elif app_type == 'java':
        generator.add_run("mvn package")
    
    generator.add_expose(port)
    generator.add_cmd(cmd)
    
    # Write to file
    dockerfile_content = generator.generate()
    with open(output, 'w') as f:
        f.write(dockerfile_content)
    
    click.echo(f"\nDockerfile has been generated at: {output}")
    click.echo("\nContent:")
    click.echo(dockerfile_content)

@cli.command()
@click.argument('dockerfile', type=click.Path(exists=True))
def validate(dockerfile: str):
    """Validate an existing Dockerfile"""
    with open(dockerfile, 'r') as f:
        content = f.read()
    
    required_instructions = ['FROM', 'WORKDIR', 'CMD']
    for instruction in required_instructions:
        if instruction not in content:
            click.echo(f"Warning: Missing {instruction} instruction")
    
    click.echo("Validation complete!")

if __name__ == '__main__':
    cli()
