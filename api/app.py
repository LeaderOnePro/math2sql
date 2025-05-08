# Flask app initialization and basic configuration

import os
import sys

# Determine the absolute path to the project root directory
# api/app.py -> api/ -> project_root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add project root to sys.path to allow for correct relative imports
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask

app = Flask(
    __name__,
    template_folder=os.path.join(project_root, 'webapp', 'templates'),
    static_folder=os.path.join(project_root, 'webapp', 'static')
)

# Optional: Add configurations like a secret key if you plan to use sessions, etc.
# app.config['SECRET_KEY'] = 'your_secret_key_here'

# Import routes after app object is created and sys.path is modified
from . import routes

# You can add a main run block for direct execution if needed,
# but using `flask run`