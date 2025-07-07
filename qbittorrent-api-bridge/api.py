#!/usr/bin/env python3
"""
qBittorrent API Bridge
A middleware for managing qBittorrent downloads via command line
"""

import argparse
import json
import logging
import os
import sys
import requests
from pathlib import Path
from typing import Dict, Optional


class QBittorrentAPI:
    def __init__(self, config_file: str = "api-config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.session = requests.Session()
        self.setup_logging()

    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        default_config = {
            "ip_address": "127.0.0.1",
            "port": 8080,
            "username": "admin",
            "password": "adminpass",
            "enable_logging": True
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with defaults
                    default_config.update(config)
            except Exception as e:
                print(f"Error loading config: {e}")
                print("Using default configuration")
        else:
            # Create default config file
            self.save_config(default_config)
            print(f"Created default config file: {self.config_file}")

        return default_config

    def save_config(self, config: Dict):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def setup_logging(self):
        """Setup logging configuration"""
        if self.config.get("enable_logging", True):
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler('api-log.txt', encoding='utf-8'),
                    logging.StreamHandler(sys.stdout)
                ]
            )
        else:
            logging.basicConfig(level=logging.CRITICAL)

        self.logger = logging.getLogger(__name__)

    def get_base_url(self) -> str:
        """Get qBittorrent base URL"""
        return f"http://{self.config['ip_address']}:{self.config['port']}"

    def login(self) -> bool:
        """Login to qBittorrent"""
        try:
            login_url = f"{self.get_base_url()}/api/v2/auth/login"
            data = {
                'username': self.config['username'],
                'password': self.config['password']
            }

            response = self.session.post(login_url, data=data)

            if response.status_code == 200 and response.text == "Ok.":
                self.logger.info("Successfully logged in to qBittorrent")
                return True
            else:
                self.logger.error(f"Login failed: {response.text}")
                return False

        except Exception as e:
            self.logger.error(f"Login error: {e}")
            return False

    def add_magnet(self, magnet_link: str) -> bool:
        """Add magnet link to qBittorrent"""
        try:
            add_url = f"{self.get_base_url()}/api/v2/torrents/add"
            data = {
                'urls': magnet_link
            }

            response = self.session.post(add_url, data=data)

            if response.status_code == 200:
                if response.text == "Ok.":
                    self.logger.info(f"Successfully added magnet link: {magnet_link}")
                    return True
                else:
                    self.logger.warning(f"Magnet link may already exist: {response.text}")
                    return True
            else:
                self.logger.error(f"Failed to add magnet link: {response.text}")
                return False

        except Exception as e:
            self.logger.error(f"Error adding magnet link: {e}")
            return False

    def add_torrent_file(self, file_path: str) -> bool:
        """Add torrent file to qBittorrent"""
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"Torrent file not found: {file_path}")
                return False

            add_url = f"{self.get_base_url()}/api/v2/torrents/add"

            with open(file_path, 'rb') as f:
                files = {'torrents': f}
                response = self.session.post(add_url, files=files)

            if response.status_code == 200:
                if response.text == "Ok.":
                    self.logger.info(f"Successfully added torrent file: {file_path}")
                    return True
                else:
                    self.logger.warning(f"Torrent file may already exist: {response.text}")
                    return True
            else:
                self.logger.error(f"Failed to add torrent file: {response.text}")
                return False

        except Exception as e:
            self.logger.error(f"Error adding torrent file: {e}")
            return False

    def update_config(self, **kwargs):
        """Update configuration"""
        updated = False

        if 'ip_address' in kwargs:
            self.config['ip_address'] = kwargs['ip_address']
            updated = True

        if 'port' in kwargs:
            self.config['port'] = int(kwargs['port'])
            updated = True

        if 'username' in kwargs:
            self.config['username'] = kwargs['username']
            updated = True

        if 'password' in kwargs:
            self.config['password'] = kwargs['password']
            updated = True

        if 'enable_logging' in kwargs:
            self.config['enable_logging'] = kwargs['enable_logging'].lower() == 'true'
            updated = True

        if updated:
            self.save_config(self.config)
            self.logger.info("Configuration updated")


def main():
    parser = argparse.ArgumentParser(description='qBittorrent API Bridge')

    # Main actions
    parser.add_argument('--bittorrent-link', type=str,
                        help='Add magnet link to qBittorrent')
    parser.add_argument('--bittorrent-file', type=str,
                        help='Add torrent file to qBittorrent')

    # Configuration options
    parser.add_argument('--change-qbittorrent-ipaddress', type=str,
                        help='Set qBittorrent IP address')
    parser.add_argument('--change-qbittorrent-port', type=int,
                        help='Set qBittorrent port')
    parser.add_argument('--change-qbittorrent-user', type=str,
                        help='Set qBittorrent username')
    parser.add_argument('--change-qbittorrent-pass', type=str,
                        help='Set qBittorrent password')
    parser.add_argument('--change-qbittorrent-log', type=str,
                        choices=['true', 'false'],
                        help='Enable/disable logging')

    args = parser.parse_args()

    # Initialize API
    api = QBittorrentAPI()

    # Handle configuration changes
    config_changes = {}
    if args.change_qbittorrent_ipaddress:
        config_changes['ip_address'] = args.change_qbittorrent_ipaddress
    if args.change_qbittorrent_port:
        config_changes['port'] = args.change_qbittorrent_port
    if args.change_qbittorrent_user:
        config_changes['username'] = args.change_qbittorrent_user
    if args.change_qbittorrent_pass:
        config_changes['password'] = args.change_qbittorrent_pass
    if args.change_qbittorrent_log:
        config_changes['enable_logging'] = args.change_qbittorrent_log

    if config_changes:
        api.update_config(**config_changes)
        print("Configuration updated successfully")
        return

    # Handle torrent operations
    if args.bittorrent_link or args.bittorrent_file:
        if not api.login():
            print("Failed to login to qBittorrent")
            sys.exit(1)

        success = False

        if args.bittorrent_link:
            success = api.add_magnet(args.bittorrent_link)

        if args.bittorrent_file:
            success = api.add_torrent_file(args.bittorrent_file)

        if success:
            print("Operation completed successfully")
        else:
            print("Operation failed")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
