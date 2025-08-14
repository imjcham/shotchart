"""
NBA Shot Chart Visualizer - Flask Backend Application
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern for Flask app creation"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'
    
    # Cache configuration
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes default
    
    # Initialize extensions
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    CORS(app, origins=cors_origins)
    
    cache = Cache(app)
    
    # Store cache instance in app for access in routes
    app.cache = cache
    
    # Register blueprints
    from app.routes.health import health_bp
    from app.routes.players import players_bp
    
    app.register_blueprint(health_bp, url_prefix='/api/health')
    app.register_blueprint(players_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': {'code': 'NOT_FOUND', 'message': 'Endpoint not found'}}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': {'code': 'INTERNAL_ERROR', 'message': 'Internal server error'}}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': {'code': 'BAD_REQUEST', 'message': 'Bad request'}}, 400
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)