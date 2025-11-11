#!/usr/bin/env python3

from netmiko import ConnectHandler
import json
import logging
from datetime import datetime

logging.basicConfig(filename='firewall_config.log', level=logging.INFO)

class FirewallAutomation:
    def __init__(self):
        self.devices = []
        self.load_firewall_config()

    def load_firewall_config(self):
        with open('firewall_devices.json', 'r') as f:
            config = json.load(f)
            self.devices = config['firewalls']

    def configure_firewall(self, device):
        try:
            print(f"Configuring firewall {device['host']}...")
            connection = ConnectHandler(**device)

            # Basic security configuration
            base_config = [
                'service password-encryption',
                'service timestamps debug datetime msec',
                'service timestamps log datetime msec',
                'logging buffered 16384',
                'no ip source-route',
                'no ip http server',
                'no ip http secure-server',
                'ip inspect audit-trail',
                'ip inspect max-incomplete high 1000',
                'ip inspect max-incomplete low 800',
                'ip inspect tcp max-incomplete host 50 block-time 0'
            ]

            # Zone-based firewall configuration
            zone_config = [
                'zone security INSIDE',
                'zone security OUTSIDE',
                'zone security DMZ',
                'zone-pair security IN-OUT source INSIDE destination OUTSIDE',
                'zone-pair security OUT-IN source OUTSIDE destination INSIDE',
                'zone-pair security DMZ-OUT source DMZ destination OUTSIDE'
            ]

            # Access Control Lists
            acl_config = [
                'ip access-list extended INSIDE-OUT',
                'permit tcp any any established',
                'permit udp any any eq domain',
                'permit icmp any any echo-reply',
                'deny ip any any log',
                'ip access-list extended OUTSIDE-IN',
                'deny ip any any log',
                'ip access-list extended DMZ-RULES',
                'permit tcp any any eq www',
                'permit tcp any any eq 443',
                'deny ip any any log'
            ]

            # Interface Security
            interface_config = [
                'interface GigabitEthernet0/0',
                'description INSIDE',
                'zone-member security INSIDE',
                'ip address dhcp',
                'no shutdown',
                'interface GigabitEthernet0/1',
                'description OUTSIDE',
                'zone-member security OUTSIDE',
                'ip address dhcp',
                'no shutdown'
            ]

            # Security Policies
            security_policies = [
                'policy-map type inspect IN-OUT-POLICY',
                'class type inspect INSIDE-OUT-CLASS',
                'inspect',
                'class class-default',
                'drop log'
            ]

            # IPS Configuration
            ips_config = [
                'ip ips name IPS-POLICY',
                'ip ips signature-category',
                'category all',
                'retired true',
                'category ios_ips basic',
                'retired false',
                'exit',
                'ip ips signature-definition',
                'exit'
            ]

            # Combine all configurations
            all_configs = (base_config + zone_config + acl_config + 
                         interface_config + security_policies + ips_config)

            # Send configuration
            output = connection.send_config_set(all_configs)
            connection.save_config()
            
            # Log the configuration
            logging.info(f"{datetime.now()} - Successfully configured {device['host']}")
            print(f"Successfully configured {device['host']}")
            
            return True

        except Exception as e:
            logging.error(f"{datetime.now()} - Error configuring {device['host']}: {str(e)}")
            print(f"Error configuring {device['host']}: {str(e)}")
            return False

    def configure_all_firewalls(self):
        success_count = 0
        for device in self.devices:
            if self.configure_firewall(device):
                success_count += 1
        
        print(f"\nConfiguration Summary:")
        print(f"Successfully configured: {success_count} devices")
        print(f"Failed configurations: {len(self.devices) - success_count} devices")

    def verify_firewall_status(self):
        for device in self.devices:
            try:
                connection = ConnectHandler(**device)
                print(f"\nVerifying {device['host']} status:")
                
                # Check security status
                commands = [
                    'show zone security',
                    'show policy-map type inspect',
                    'show ip access-lists',
                    'show ip ips statistics'
                ]
                
                for cmd in commands:
                    output = connection.send_command(cmd)
                    print(f"\n{cmd}:")
                    print(output)
                    
                connection.disconnect()
                
            except Exception as e:
                print(f"Error verifying {device['host']}: {str(e)}")

if __name__ == "__main__":
    firewall = FirewallAutomation()
    firewall.configure_all_firewalls()
    firewall.verify_firewall_status()
