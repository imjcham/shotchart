"""
NBA Shot Chart Backend Application
Flask application factory and configuration
"""

import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """
    Application factory function
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'development')
    configure_app(app, config_name)
    
    # Initialize extensions
    initialize_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    logger.info(f"Flask app created with config: {config_name}")
    return app

def configure_app(app, config_name):
    """Configure the Flask application"""
    
    # Base configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = config_name == 'development'
    
    # Cache configuration
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    
    # CORS configuration
    app.config['CORS_ORIGINS'] = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # NBA API configuration
    app.config['NBA_API_TIMEOUT'] = int(os.getenv('NBA_API_TIMEOUT', '30'))
    app.config['NBA_API_RETRIES'] = int(os.getenv('NBA_API_RETRIES', '3'))
    
    # Logging configuration
    if config_name == 'production':
        app.config['LOG_LEVEL'] = logging.WARNING
    else:
        app.config['LOG_LEVEL'] = logging.INFO
    
    logging.getLogger().setLevel(app.config['LOG_LEVEL'])

def initialize_extensions(app):
    """Initialize Flask extensions"""
    
    # Initialize CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    logger.info(f"CORS configured for origins: {app.config['CORS_ORIGINS']}")
    
    # Initialize Cache
    cache = Cache(app)
    app.cache = cache
    logger.info("Cache initialized")

def register_blueprints(app):
    """Register application blueprints"""
    
    from app.routes.players import players_bp
    
    # Register API blueprints with prefix
    app.register_blueprint(players_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Application health check endpoint"""
        return {
            'status': 'healthy',
            'service': 'nba-shotchart-backend',
            'version': '1.0.0'
        }, 200
    
    logger.info("Blueprints registered")

def register_error_handlers(app):
    """Register global error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return {
            'error': {
                'code': 'NOT_FOUND',
                'message': 'The requested resource was not found'
            }
        }, 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return {
            'error': {
                'code': 'METHOD_NOT_ALLOWED',
                'message': 'The requested method is not allowed for this resource'
            }
        }, 405
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return {
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An internal server error occurred'
            }
        }, 500
    
    logger.info("Error handlers registered")