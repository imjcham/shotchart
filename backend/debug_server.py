#!/usr/bin/env python3
"""
Debug server for NBA Shot Chart backend
Run this to test the backend independently
"""

import sys
import os
import logging

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_imports():
    """Test all imports to identify issues"""
    logger.info("Testing imports...")
    
    try:
        import flask
        logger.info(f"✓ Flask {flask.__version__}")
    except ImportError as e:
        logger.error(f"✗ Flask import failed: {e}")
        return False
    
    try:
        import flask_cors
        logger.info("✓ Flask-CORS")
    except ImportError as e:
        logger.error(f"✗ Flask-CORS import failed: {e}")
        return False
    
    try:
        import flask_caching
        logger.info("✓ Flask-Caching")
    except ImportError as e:
        logger.error(f"✗ Flask-Caching import failed: {e}")
        return False
    
    try:
        import nba_api
        logger.info(f"✓ NBA API")
    except ImportError as e:
        logger.error(f"✗ NBA API import failed: {e}")
        logger.warning("NBA API not available - will use fallback data")
    
    try:
        import pandas as pd
        logger.info(f"✓ Pandas {pd.__version__}")
    except ImportError as e:
        logger.error(f"✗ Pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        logger.info(f"✓ Numpy {np.__version__}")
    except ImportError as e:
        logger.error(f"✗ Numpy import failed: {e}")
        return False
    
    return True

def test_app_creation():
    """Test Flask app creation"""
    logger.info("Testing Flask app creation...")
    
    try:
        # Import from the root-level app.py file, not the app package
        import app as app_module
        flask_app = app_module.create_app()
        logger.info("✓ Flask app created successfully")
        return flask_app
    except Exception as e:
        logger.error(f"✗ Flask app creation failed: {e}")
        return None

def test_routes(app):
    """Test basic routes"""
    logger.info("Testing routes...")
    
    with app.test_client() as client:
        # Test health endpoint
        try:
            response = client.get('/api/health')
            if response.status_code == 200:
                logger.info("✓ Health endpoint working")
            else:
                logger.error(f"✗ Health endpoint failed: {response.status_code}")
        except Exception as e:
            logger.error(f"✗ Health endpoint error: {e}")
        
        # Test player search with fallback data
        try:
            response = client.get('/api/players/search?q=lebron')
            if response.status_code == 200:
                data = response.get_json()
                logger.info(f"✓ Player search working: found {data.get('count', 0)} players")
            else:
                logger.error(f"✗ Player search failed: {response.status_code}")
                logger.error(f"Response: {response.get_data(as_text=True)}")
        except Exception as e:
            logger.error(f"✗ Player search error: {e}")

def main():
    """Main debug function"""
    logger.info("=== NBA Shot Chart Backend Debug ===")
    
    # Test imports
    if not test_imports():
        logger.error("Import tests failed - check dependencies")
        return False
    
    # Test app creation
    app = test_app_creation()
    if not app:
        logger.error("App creation failed")
        return False
    
    # Test routes
    test_routes(app)
    
    logger.info("=== Debug Complete ===")
    
    # Start the server
    logger.info("Starting debug server on http://localhost:5000")
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        return False
    
    return True

if __name__ == '__main__':
    main()