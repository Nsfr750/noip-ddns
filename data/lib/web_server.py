#!/usr/bin/env python3
"""
No-IP DDNS Web Server
© Copyright 2024-2026 Nsfr750 - All rights reserved.
"""

import json
import logging
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import subprocess

# Configuration
CONFIG_DIR = "/usr/local/AppCentral/noip-ddns/etc"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
LOG_FILE = "/var/log/noip-ddns.log"
WEBAPP_DIR = "/usr/local/AppCentral/noip-ddns/data/webapp"
PORT = 7777

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


class DDNSWebHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for DDNS web interface."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBAPP_DIR, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        # API endpoints
        if parsed_path.path == '/api/hosts':
            self.send_json_response(self.get_hosts())
        elif parsed_path.path == '/api/public-ip':
            self.send_json_response(self.get_public_ip())
        elif parsed_path.path == '/api/logs':
            self.send_json_response(self.get_logs())
        else:
            # Serve static files
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if parsed_path.path == '/api/hosts':
            try:
                data = json.loads(post_data.decode('utf-8'))
                if data.get('action') == 'add':
                    result = self.add_host(data)
                elif data.get('action') == 'remove':
                    result = self.remove_host(data)
                elif data.get('action') == 'update':
                    result = self.update_host(data)
                else:
                    result = {'success': False, 'error': 'Invalid action'}
                self.send_json_response(result)
            except Exception as e:
                self.send_json_response({'success': False, 'error': str(e)})
        elif parsed_path.path == '/api/update':
            result = self.trigger_update()
            self.send_json_response(result)
        else:
            self.send_error(404)
    
    def send_json_response(self, data):
        """Send JSON response."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def get_hosts(self):
        """Get configured hosts."""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                return {'success': True, 'hosts': config.get('hosts', [])}
            else:
                return {'success': True, 'hosts': []}
        except Exception as e:
            logger.error(f"Error getting hosts: {e}")
            return {'success': False, 'error': str(e)}
    
    def add_host(self, data):
        """Add a new host."""
        try:
            # Load existing config
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
            else:
                config = {'hosts': [], 'update_interval': 300, 'last_update': None, 'last_ip': None}
            
            # Add new host
            new_host = {
                'hostname': data.get('hostname'),
                'username': data.get('username'),
                'password': data.get('password')
            }
            config['hosts'].append(new_host)
            
            # Save config
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Added host: {new_host['hostname']}")
            return {'success': True}
        except Exception as e:
            logger.error(f"Error adding host: {e}")
            return {'success': False, 'error': str(e)}
    
    def remove_host(self, data):
        """Remove a host."""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                
                # Remove host by hostname
                hostname = data.get('hostname')
                config['hosts'] = [h for h in config['hosts'] if h.get('hostname') != hostname]
                
                # Save config
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(config, f, indent=2)
                
                logger.info(f"Removed host: {hostname}")
                return {'success': True}
            else:
                return {'success': False, 'error': 'Config file not found'}
        except Exception as e:
            logger.error(f"Error removing host: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_host(self, data):
        """Update a host."""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                
                # Update host by hostname
                hostname = data.get('hostname')
                for host in config['hosts']:
                    if host.get('hostname') == hostname:
                        host['username'] = data.get('username', host['username'])
                        host['password'] = data.get('password', host['password'])
                        break
                
                # Save config
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(config, f, indent=2)
                
                logger.info(f"Updated host: {hostname}")
                return {'success': True}
            else:
                return {'success': False, 'error': 'Config file not found'}
        except Exception as e:
            logger.error(f"Error updating host: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_public_ip(self):
        """Get current public IP."""
        try:
            import urllib.request
            with urllib.request.urlopen('https://api.ipify.org', timeout=10) as response:
                ip = response.read().decode('utf-8').strip()
                return {'success': True, 'ip': ip}
        except Exception as e:
            logger.error(f"Error getting public IP: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_logs(self):
        """Get recent log entries."""
        try:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r') as f:
                    logs = f.readlines()
                # Return last 50 lines
                return {'success': True, 'logs': logs[-50:]}
            else:
                return {'success': True, 'logs': []}
        except Exception as e:
            logger.error(f"Error getting logs: {e}")
            return {'success': False, 'error': str(e)}
    
    def trigger_update(self):
        """Trigger manual DDNS update."""
        try:
            # Run the ddns_updater script with --once flag
            result = subprocess.run(
                ['/usr/local/bin/python3', '/usr/local/AppCentral/noip-ddns/data/lib/ddns_updater.py', '--once'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return {'success': True, 'output': result.stdout}
            else:
                return {'success': False, 'error': result.stderr}
        except Exception as e:
            logger.error(f"Error triggering update: {e}")
            return {'success': False, 'error': str(e)}
    
    def log_message(self, format, *args):
        """Custom log message handler."""
        logger.info(f"{self.address_string()} - {format % args}")


def main():
    """Main entry point."""
    # Change to webapp directory
    if os.path.exists(WEBAPP_DIR):
        os.chdir(WEBAPP_DIR)
    else:
        logger.error(f"Webapp directory not found: {WEBAPP_DIR}")
        sys.exit(1)
    
    # Create server
    server = HTTPServer(('0.0.0.0', PORT), DDNSWebHandler)
    logger.info(f"Starting DDNS web server on port {PORT}")
    logger.info(f"Serving files from: {WEBAPP_DIR}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down web server")
        server.shutdown()


if __name__ == '__main__':
    main()
