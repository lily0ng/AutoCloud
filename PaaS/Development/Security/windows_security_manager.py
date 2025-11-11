import winrm
import logging
from typing import Dict, List, Optional

class WindowsSecurityManager:
    def __init__(self, hostname: str, username: str, password: str):
        self.hostname = hostname
        self.session = winrm.Session(
            hostname,
            auth=(username, password),
            transport='ntlm',
            server_cert_validation='ignore'
        )
        self.logger = logging.getLogger('WindowsSecurityManager')

    def run_powershell(self, script: str) -> tuple:
        try:
            result = self.session.run_ps(script)
            return result.std_out.decode(), result.std_err.decode(), result.status_code
        except Exception as e:
            self.logger.error(f"Error running PowerShell command: {str(e)}")
            return "", str(e), 1

    def check_windows_security(self) -> Dict:
        security_status = {
            'windows_updates': self._check_windows_updates(),
            'firewall_status': self._check_firewall(),
            'antivirus_status': self._check_antivirus(),
            'bitlocker_status': self._check_bitlocker(),
            'user_audit': self._audit_users()
        }
        return security_status

    def _check_windows_updates(self) -> Dict:
        script = '''
        Get-WUHistory | Where-Object {
            $_.Result -eq "Succeeded"
        } | Select-Object -First 10 | ForEach-Object {
            @{
                Title = $_.Title
                Date = $_.Date
            }
        } | ConvertTo-Json
        '''
        stdout, _, _ = self.run_powershell(script)
        return {'recent_updates': stdout}

    def _check_firewall(self) -> Dict:
        script = '''
        Get-NetFirewallProfile | Select-Object Name, Enabled | ConvertTo-Json
        '''
        stdout, _, _ = self.run_powershell(script)
        return {'firewall_profiles': stdout}

    def _check_antivirus(self) -> Dict:
        script = '''
        Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, 
        IoavProtectionEnabled, AntispywareEnabled | ConvertTo-Json
        '''
        stdout, _, _ = self.run_powershell(script)
        return {'defender_status': stdout}

    def _check_bitlocker(self) -> Dict:
        script = '''
        Get-BitLockerVolume | Select-Object MountPoint, EncryptionMethod, 
        VolumeStatus, ProtectionStatus | ConvertTo-Json
        '''
        stdout, _, _ = self.run_powershell(script)
        return {'bitlocker_status': stdout}

    def _audit_users(self) -> Dict:
        script = '''
        Get-LocalUser | Select-Object Name, Enabled, LastLogon, 
        PasswordRequired, PasswordLastSet | ConvertTo-Json
        '''
        stdout, _, _ = self.run_powershell(script)
        return {'local_users': stdout}

    def harden_windows(self) -> bool:
        try:
            # Enable Windows Defender
            self.run_powershell('Set-MpPreference -DisableRealtimeMonitoring $false')

            # Enable Windows Firewall
            self.run_powershell('Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True')

            # Enable UAC
            self.run_powershell('Set-ItemProperty -Path REGISTRY::HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System -Name EnableLUA -Value 1')

            # Configure Windows Update
            self.run_powershell('''
            Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update" -Name AUOptions -Value 4
            ''')

            # Enable BitLocker
            self.run_powershell('''
            Enable-BitLocker -MountPoint "C:" -EncryptionMethod Aes256 -UsedSpaceOnly -RecoveryPasswordProtector
            ''')

            return True
        except Exception as e:
            self.logger.error(f"Error hardening Windows: {str(e)}")
            return False

    def configure_password_policy(self) -> bool:
        try:
            script = '''
            Net Accounts /MINPWLEN:12 /MAXPWAGE:30 /UNIQUEPW:5 /LOCKOUTTHRESHOLD:5 /LOCKOUTDURATION:30
            '''
            _, _, status = self.run_powershell(script)
            return status == 0
        except Exception as e:
            self.logger.error(f"Error configuring password policy: {str(e)}")
            return False
