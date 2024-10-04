#!/usr/bin/env python3

from app import create_app
from config import Config

# Initialize the app with the configuration settings
app = create_app(Config)

if __name__ == "__main__":
    # Run the app in debug mode for development purposes
    app.run(debug=True, host='0.0.0.0', port=5000)
