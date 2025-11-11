"""
Configuration loader and manager
"""
import os
import yaml
import json
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Load and manage application configuration"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.getenv('CONFIG_PATH', 'config.yml')
        self._config = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_path.endswith('.yml') or self.config_path.endswith('.yaml'):
                with open(self.config_path, 'r') as f:
                    self._config = yaml.safe_load(f)
            elif self.config_path.endswith('.json'):
                with open(self.config_path, 'r') as f:
                    self._config = json.load(f)
            else:
                raise ValueError(f"Unsupported config format: {self.config_path}")
            
            # Override with environment variables
            self._override_with_env()
            
            logger.info(f"Configuration loaded from {self.config_path}")
            
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}, using defaults")
            self._config = self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise
    
    def _override_with_env(self):
        """Override config values with environment variables"""
        env_prefix = 'AUTOCLOUD_'
        
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower()
                self._config[config_key] = value
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'app': {
                'name': 'AutoCloud',
                'version': '1.0.0',
                'environment': 'development',
                'debug': True
            },
            'server': {
                'host': '0.0.0.0',
                'port': 8000,
                'workers': 4
            },
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'autocloud',
                'user': 'postgres',
                'pool_size': 10
            },
            'redis': {
                'host': 'localhost',
                'port': 6379,
                'db': 0
            },
            'logging': {
                'level': 'INFO',
                'format': 'json',
                'file': 'app.log'
            },
            'security': {
                'jwt_secret': 'change-me-in-production',
                'jwt_expiry': 3600,
                'cors_origins': ['*']
            },
            'cloud_providers': {
                'aws': {
                    'enabled': True,
                    'region': 'us-east-1'
                },
                'azure': {
                    'enabled': False
                },
                'gcp': {
                    'enabled': False
                }
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_all(self) -> Dict:
        """Get all configuration"""
        return self._config.copy()
    
    def reload(self):
        """Reload configuration from file"""
        self.load_config()
    
    def save(self, path: str = None):
        """Save configuration to file"""
        save_path = path or self.config_path
        
        try:
            if save_path.endswith('.yml') or save_path.endswith('.yaml'):
                with open(save_path, 'w') as f:
                    yaml.dump(self._config, f, default_flow_style=False)
            elif save_path.endswith('.json'):
                with open(save_path, 'w') as f:
                    json.dump(self._config, f, indent=2)
            
            logger.info(f"Configuration saved to {save_path}")
            
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")
            raise
    
    def validate(self) -> bool:
        """Validate configuration"""
        required_keys = [
            'app.name',
            'server.host',
            'server.port',
            'database.host'
        ]
        
        for key in required_keys:
            if self.get(key) is None:
                logger.error(f"Missing required config: {key}")
                return False
        
        return True


# Global config instance
config = ConfigLoader()
