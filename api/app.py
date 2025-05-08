# Flask app initialization and basic configuration

from flask import Flask

app = Flask(__name__)

# Load routes
from . import routes

# Placeholder for further app configuration 