#!/usr/bin/env python3
"""
No-IP DDNS Updater
© Copyright 2024-2026 Nsfr750 - All rights reserved.
"""

import argparse
import json
import logging
import os
import sys
import time
import urllib.request
import urllib.error
from http.client import HTTPConnection
from typing import Dict, Optional

# Configuration
CONFIG_DIR = "/usr/local/AppCentral/noip-ddns/etc"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
LOG_FILE = "/var/log/noip-ddns.log"
NOIP_UPDATE_URL = "https://dynupdate.no-ip.com/nic/update"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class NoIPDDNSUpdater:
    """No-IP DDNS updater class."""
    
    def __init__(self, config_path: str = CONFIG_FILE):
        """Initialize the DDNS updater."""
        self.config_path = config_path
        self.config: Dict = {}
        self.last_ip: Optional[str] = None
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logger.info("Configuration loaded successfully")
            else:
                logger.warning(f"Config file not found: {self.config_path}")
                self.config = {}
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self.config = {}
    
    def save_config(self) -> None:
        """Save configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def get_public_ip(self) -> Optional[str]:
        """Get current public IP address."""
        try:
            with urllib.request.urlopen('https://api.ipify.org', timeout=10) as response:
                ip = response.read().decode('utf-8').strip()
                logger.info(f"Current public IP: {ip}")
                return ip
        except Exception as e:
            logger.error(f"Error getting public IP: {e}")
            return None
    
    def update_ddns(self, hostname: str, username: str, password: str) -> bool:
        """Update DDNS record for hostname."""
        try:
            # Create basic auth header
            auth_str = f"{username}:{password}"
            auth_b64 = __import__('base64').b64encode(auth_str.encode()).decode()
            
            # Build request
            url = f"{NOIP_UPDATE_URL}?hostname={hostname}"
            req = urllib.request.Request(url)
            req.add_header('Authorization', f'Basic {auth_b64}')
            req.add_header('User-Agent', 'NoIP-DDNS-Manager/1.0')
            
            # Send request
            with urllib.request.urlopen(req, timeout=30) as response:
                result = response.read().decode('utf-8').strip()
                logger.info(f"DDNS update response: {result}")
                
                # Parse response
                if result.startswith('good') or result.startswith('nochg'):
                    return True
                else:
                    logger.error(f"DDNS update failed: {result}")
                    return False
                    
        except urllib.error.HTTPError as e:
            logger.error(f"HTTP Error updating DDNS: {e.code} - {e.reason}")
            return False
        except Exception as e:
            logger.error(f"Error updating DDNS: {e}")
            return False
    
    def update_all_hosts(self) -> None:
        """Update all configured hosts."""
        if not self.config.get('hosts'):
            logger.warning("No hosts configured")
            return
        
        current_ip = self.get_public_ip()
        if not current_ip:
            logger.error("Could not get public IP")
            return
        
        if self.last_ip == current_ip:
            logger.info(f"IP unchanged ({current_ip}), skipping update")
            return
        
        logger.info(f"IP changed from {self.last_ip} to {current_ip}, updating DDNS")
        
        success_count = 0
        for host in self.config['hosts']:
            hostname = host.get('hostname')
            username = host.get('username')
            password = host.get('password')
            
            if not all([hostname, username, password]):
                logger.warning(f"Invalid host configuration: {hostname}")
                continue
            
            if self.update_ddns(hostname, username, password):
                success_count += 1
                logger.info(f"Successfully updated {hostname}")
            else:
                logger.error(f"Failed to update {hostname}")
        
        if success_count == len(self.config['hosts']):
            self.last_ip = current_ip
            logger.info(f"All hosts updated successfully")
    
    def run_daemon(self, interval: int = 300) -> None:
        """Run as daemon with periodic updates."""
        logger.info(f"Starting DDNS updater daemon (interval: {interval}s)")
        
        while True:
            try:
                self.load_config()
                self.update_all_hosts()
            except Exception as e:
                logger.error(f"Error in daemon loop: {e}")
            
            time.sleep(interval)
    
    def run_once(self) -> None:
        """Run a single update."""
        logger.info("Running single DDNS update")
        self.load_config()
        self.update_all_hosts()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='No-IP DDNS Updater')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    parser.add_argument('--interval', type=int, default=300, 
                       help='Update interval in seconds (default: 300)')
    parser.add_argument('--once', action='store_true', help='Run single update')
    parser.add_argument('--config', type=str, default=CONFIG_FILE,
                       help='Path to config file')
    
    args = parser.parse_args()
    
    updater = NoIPDDNSUpdater(args.config)
    
    if args.daemon:
        updater.run_daemon(args.interval)
    elif args.once:
        updater.run_once()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
