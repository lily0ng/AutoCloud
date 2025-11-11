#!/usr/bin/env python3

from netmiko import ConnectHandler
import json
import time

class NetworkAutomation:
    def __init__(self):
        self.devices = []
        self.load_device_config()

    def load_device_config(self):
        # Load switch configurations from config file
        with open('device_config.json', 'r') as f:
            self.devices = json.load(f)

    def configure_switches(self):
        for device in self.devices:
            try:
                print(f"Configuring {device['hostname']}...")
                connection = ConnectHandler(**device)
                
                # Basic configuration commands
                config_commands = [
                    'service password-encryption',
                    'service timestamps debug datetime msec',
                    'service timestamps log datetime msec',
                    'service autoconfig',
                    'ip forward-protocol nd',
                    'ip http server',
                    'ip http secure-server',
                ]

                # Configure VLANs
                for vlan_id in range(10, 30):
                    config_commands.extend([
                        f'vlan {vlan_id}',
                        f'name VLAN_{vlan_id}'
                    ])

                # Configure Port Channels
                port_channel_config = [
                    'interface port-channel 1',
                    'description Auto-LAG',
                    'switchport mode trunk',
                    'switchport trunk allowed vlan all',
                    'spanning-tree portfast'
                ]
                config_commands.extend(port_channel_config)

                # Configure interfaces for port channel
                for interface in range(1, 5):
                    interface_config = [
                        f'interface GigabitEthernet0/{interface}',
                        'channel-group 1 mode active',
                        'negotiation auto'
                    ]
                    config_commands.extend(interface_config)

                # Send configuration to device
                connection.send_config_set(config_commands)
                connection.save_config()
                connection.disconnect()
                print(f"Successfully configured {device['hostname']}")

            except Exception as e:
                print(f"Error configuring {device['hostname']}: {str(e)}")

    def monitor_ports(self):
        for device in self.devices:
            try:
                connection = ConnectHandler(**device)
                output = connection.send_command('show interfaces status')
                print(f"\nPort Status for {device['hostname']}:")
                print(output)
                connection.disconnect()
            except Exception as e:
                print(f"Error monitoring {device['hostname']}: {str(e)}")

if __name__ == "__main__":
    network = NetworkAutomation()
    network.configure_switches()
    network.monitor_ports()
