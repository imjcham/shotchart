"""
Health check endpoints for monitoring and deployment
"""

from flask import Blueprint, jsonify
import time
import os

health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
def health_check():
    """
    Health check endpoint for load balancers and monitoring
    Returns basic service status and metadata
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': int(time.time()),
        'service': 'nba-shotchart-backend',
        'version': '1.0.0',
        'environment': os.getenv('FLASK_ENV', 'development')
    }), 200

@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """
    Readiness check endpoint for Kubernetes deployments
    Verifies that the service is ready to accept traffic
    """
    try:
        # Test NBA API connectivity (basic check)
        from nba_api.stats.endpoints import commonplayerinfo
        # This is a lightweight check - just import the module
        
        return jsonify({
            'status': 'ready',
            'timestamp': int(time.time()),
            'checks': {
                'nba_api': 'available'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'timestamp': int(time.time()),
            'error': str(e)
        }), 503

@health_bp.route('/live', methods=['GET'])
def liveness_check():
    """
    Liveness check endpoint for Kubernetes deployments
    Simple check to verify the service is running
    """
    return jsonify({
        'status': 'alive',
        'timestamp': int(time.time())
    }), 200