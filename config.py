import os

# Admin Access Configuration
ADMIN_ALLOWED_IPS = os.environ.get('ADMIN_ALLOWED_IPS', '127.0.0.1,::1,196.189.29.152').split(',')
ADMIN_ALLOWED_IPS = [ip.strip() for ip in ADMIN_ALLOWED_IPS if ip.strip()]

# Debug mode - set to True to temporarily bypass IP restrictions
ADMIN_DEBUG_MODE = os.environ.get('ADMIN_DEBUG_MODE', 'False').lower() == 'true'

# Database Configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///anipreneur.db')

# Flask Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

print(f"🔐 Admin IPs configured: {ADMIN_ALLOWED_IPS}")
print(f"🐛 Debug mode: {ADMIN_DEBUG_MODE}") 