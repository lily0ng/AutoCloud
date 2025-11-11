#!/usr/bin/env python3

import yaml
import logging
import argparse
from datetime import datetime
import json
from pathlib import Path
from user_manager import UserManager

class OnboardingAutomation:
    def __init__(self, config_path='config/config.yaml'):
        self.user_manager = UserManager(config_path)
        self.load_config(config_path)
        self.setup_logging()

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def setup_logging(self):
        self.logger = logging.getLogger('onboarding')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('logs/onboarding.log')
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def process_onboarding(self, template_file):
        """Process onboarding based on template file."""
        try:
            with open(template_file, 'r') as f:
                template = yaml.safe_load(f)

            results = {
                'success': [],
                'failed': []
            }

            for user in template['users']:
                try:
                    self.logger.info(f"Starting onboarding process for {user['username']}")
                    
                    # Create user account
                    success, password = self.user_manager.create_user(
                        username=user['username'],
                        role=user.get('role', 'staff'),
                        full_name=user.get('full_name')
                    )

                    if success:
                        # Provision additional resources
                        self._provision_resources(user['username'])
                        
                        results['success'].append({
                            'username': user['username'],
                            'password': password,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        self.logger.info(f"Successfully onboarded {user['username']}")
                    else:
                        results['failed'].append({
                            'username': user['username'],
                            'reason': 'User creation failed'
                        })
                        self.logger.error(f"Failed to onboard {user['username']}")

                except Exception as e:
                    results['failed'].append({
                        'username': user['username'],
                        'reason': str(e)
                    })
                    self.logger.error(f"Error onboarding {user['username']}: {str(e)}")

            # Save results
            self._save_results(results)
            return results

        except Exception as e:
            self.logger.error(f"Failed to process onboarding template: {str(e)}")
            raise

    def _provision_resources(self, username):
        """Provision additional resources for user."""
        config = self.config['onboarding']
        
        if config['resource_provisioning']['email_setup']:
            self._setup_email(username)
            
        if config['resource_provisioning']['vpn_access']:
            self._setup_vpn(username)

    def _setup_email(self, username):
        """Setup email account for user."""
        self.logger.info(f"Setting up email for {username}")
        # Implement email setup logic here
        pass

    def _setup_vpn(self, username):
        """Setup VPN access for user."""
        self.logger.info(f"Setting up VPN access for {username}")
        # Implement VPN setup logic here
        pass

    def _save_results(self, results):
        """Save onboarding results to file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'logs/onboarding_results_{timestamp}.json'
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.info(f"Saved onboarding results to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='User Onboarding Automation')
    parser.add_argument('--template', required=True,
                      help='Path to onboarding template YAML file')
    parser.add_argument('--config', default='config/config.yaml',
                      help='Path to configuration file')

    args = parser.parse_args()

    onboarding = OnboardingAutomation(args.config)
    results = onboarding.process_onboarding(args.template)

    # Print summary
    print("\nOnboarding Summary:")
    print(f"Successfully onboarded: {len(results['success'])} users")
    print(f"Failed to onboard: {len(results['failed'])} users")

    if results['failed']:
        print("\nFailed onboarding details:")
        for fail in results['failed']:
            print(f"- {fail['username']}: {fail['reason']}")

if __name__ == "__main__":
    main()
