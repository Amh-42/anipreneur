import sys
import os

# Add the application directory to the Python path
INTERP = os.path.expanduser("/home/YOUR_CPANEL_USERNAME/virtualenv/anipreneur/3.9/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Import the Flask app
from app import app as application

# For debugging (optional)
if __name__ == "__main__":
    application.run() 