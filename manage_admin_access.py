#!/usr/bin/env python3
"""
Admin Access Management Utility for Anipreneur

This script helps you manage IP-based access control for the admin panel.
"""

import os
import sys
import requests
from datetime import datetime

def get_current_ip():
    """Get the current device's public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return "Could not determine IP address"

def get_local_ip():
    """Get the local IP address"""
    import socket
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def show_current_settings():
    """Display current admin access settings"""
    print("🔒 Current Admin Access Settings")
    print("=" * 40)
    
    # Get current environment variable
    allowed_ips = os.environ.get('ADMIN_ALLOWED_IPS', '127.0.0.1,::1')
    current_ips = [ip.strip() for ip in allowed_ips.split(',') if ip.strip()]
    
    print(f"Allowed IPs: {', '.join(current_ips)}")
    print(f"Current device IP: {get_current_ip()}")
    print(f"Local IP: {get_local_ip()}")
    print()

def add_ip_to_whitelist(ip_address):
    """Add an IP address to the whitelist"""
    current_ips = os.environ.get('ADMIN_ALLOWED_IPS', '127.0.0.1,::1')
    ip_list = [ip.strip() for ip in current_ips.split(',') if ip.strip()]
    
    if ip_address not in ip_list:
        ip_list.append(ip_address)
        new_setting = ','.join(ip_list)
        
        print(f"✅ Added {ip_address} to admin whitelist")
        print(f"New setting: ADMIN_ALLOWED_IPS={new_setting}")
        print()
        print("To apply this change, set the environment variable:")
        print(f"export ADMIN_ALLOWED_IPS='{new_setting}'")
        print()
        print("Or add to your .env file:")
        print(f"ADMIN_ALLOWED_IPS={new_setting}")
    else:
        print(f"⚠️  {ip_address} is already in the whitelist")

def remove_ip_from_whitelist(ip_address):
    """Remove an IP address from the whitelist"""
    current_ips = os.environ.get('ADMIN_ALLOWED_IPS', '127.0.0.1,::1')
    ip_list = [ip.strip() for ip in current_ips.split(',') if ip.strip()]
    
    if ip_address in ip_list:
        ip_list.remove(ip_address)
        new_setting = ','.join(ip_list)
        
        print(f"✅ Removed {ip_address} from admin whitelist")
        print(f"New setting: ADMIN_ALLOWED_IPS={new_setting}")
        print()
        print("To apply this change, set the environment variable:")
        print(f"export ADMIN_ALLOWED_IPS='{new_setting}'")
        print()
        print("Or add to your .env file:")
        print(f"ADMIN_ALLOWED_IPS={new_setting}")
    else:
        print(f"⚠️  {ip_address} is not in the whitelist")

def show_help():
    """Display help information"""
    print("🔒 Anipreneur Admin Access Management")
    print("=" * 50)
    print()
    print("Usage:")
    print("  python manage_admin_access.py [command] [ip_address]")
    print()
    print("Commands:")
    print("  status                    - Show current settings")
    print("  add <ip>                 - Add IP to whitelist")
    print("  remove <ip>              - Remove IP from whitelist")
    print("  add-current              - Add current device IP to whitelist")
    print("  help                     - Show this help")
    print()
    print("Examples:")
    print("  python manage_admin_access.py status")
    print("  python manage_admin_access.py add 192.168.1.100")
    print("  python manage_admin_access.py add-current")
    print("  python manage_admin_access.py remove 192.168.1.100")
    print()
    print("Security Notes:")
    print("  - Only whitelisted IPs can access /admin routes")
    print("  - Changes require restarting the Flask app")
    print("  - Use environment variables for production deployment")
    print("  - Consider using a VPN for additional security")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'status':
        show_current_settings()
    
    elif command == 'add-current':
        current_ip = get_current_ip()
        if current_ip != "Could not determine IP address":
            add_ip_to_whitelist(current_ip)
        else:
            print("❌ Could not determine current IP address")
            print("Try using 'add' command with your IP manually")
    
    elif command == 'add':
        if len(sys.argv) < 3:
            print("❌ Please provide an IP address")
            print("Usage: python manage_admin_access.py add <ip_address>")
            return
        ip_address = sys.argv[2]
        add_ip_to_whitelist(ip_address)
    
    elif command == 'remove':
        if len(sys.argv) < 3:
            print("❌ Please provide an IP address")
            print("Usage: python manage_admin_access.py remove <ip_address>")
            return
        ip_address = sys.argv[2]
        remove_ip_from_whitelist(ip_address)
    
    elif command == 'help':
        show_help()
    
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main() 