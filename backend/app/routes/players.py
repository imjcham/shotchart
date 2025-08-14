"""
Player-related API endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from app.services.player_service import PlayerService
from app.utils.validation import validate_player_search, validate_player_id
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

players_bp = Blueprint('players', __name__)

# Initialize player service
player_service = PlayerService()

@players_bp.route('/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint to verify the API is working"""
    return jsonify({
        'status': 'success',
        'message': 'NBA Shot Chart API is working',
        'timestamp': int(time.time())
    }), 200

@players_bp.route('/players/search', methods=['GET'])
def search_players():
    """
    Search for NBA players by name
    Query parameters:
    - q: search query string (required)
    - limit: maximum number of results (optional, default: 10)
    """
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 10, type=int)
        
        logger.info(f"Player search request: query='{query}', limit={limit}")
        
        # Validate input
        validation_error = validate_player_search(query, limit)
        if validation_error:
            logger.warning(f"Validation error: {validation_error}")
            return jsonify({'error': validation_error}), 400
        
        # Search players
        players = player_service.search_players(query, limit)
        
        logger.info(f"Found {len(players)} players for query '{query}'")
        
        return jsonify({
            'data': players,
            'query': query,
            'count': len(players)
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching players: {str(e)}", exc_info=True)
        return jsonify({
            'error': {
                'code': 'SEARCH_ERROR',
                'message': 'Failed to search players',
                'details': str(e) if current_app.debug else None
            }
        }), 500

@players_bp.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    """
    Get detailed information for a specific player
    Path parameters:
    - player_id: NBA player ID (required)
    """
    try:
        # Validate input
        validation_error = validate_player_id(player_id)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        # Get player info
        player = player_service.get_player_info(player_id)
        
        if not player:
            return jsonify({
                'error': {
                    'code': 'PLAYER_NOT_FOUND',
                    'message': f'Player with ID {player_id} not found'
                }
            }), 404
        
        return jsonify({'data': player}), 200
        
    except Exception as e:
        logger.error(f"Error getting player {player_id}: {str(e)}")
        return jsonify({
            'error': {
                'code': 'PLAYER_ERROR',
                'message': 'Failed to get player information',
                'details': str(e) if current_app.debug else None
            }
        }), 500

@players_bp.route('/players/<int:player_id>/shots', methods=['GET'])
def get_player_shots(player_id):
    """
    Get shot chart data for a specific player
    Path parameters:
    - player_id: NBA player ID (required)
    Query parameters:
    - season: NBA season (optional, default: current season)
    - season_type: Regular Season or Playoffs (optional, default: Regular Season)
    """
    try:
        # Validate input
        validation_error = validate_player_id(player_id)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        season = request.args.get('season', '2023-24')
        season_type = request.args.get('season_type', 'Regular Season')
        
        # Get shot data
        shots = player_service.get_player_shots(player_id, season, season_type)
        
        return jsonify({
            'data': shots,
            'player_id': player_id,
            'season': season,
            'season_type': season_type,
            'count': len(shots)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting shots for player {player_id}: {str(e)}")
        return jsonify({
            'error': {
                'code': 'SHOTS_ERROR',
                'message': 'Failed to get shot chart data',
                'details': str(e) if current_app.debug else None
            }
        }), 500

@players_bp.route('/players/<int:player_id>/stats', methods=['GET'])
def get_player_stats(player_id):
    """
    Get shooting statistics for a specific player
    Path parameters:
    - player_id: NBA player ID (required)
    Query parameters:
    - season: NBA season (optional, default: current season)
    """
    try:
        # Validate input
        validation_error = validate_player_id(player_id)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        season = request.args.get('season', '2023-24')
        
        # Get player stats
        stats = player_service.get_player_stats(player_id, season)
        
        return jsonify({
            'data': stats,
            'player_id': player_id,
            'season': season
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting stats for player {player_id}: {str(e)}")
        return jsonify({
            'error': {
                'code': 'STATS_ERROR',
                'message': 'Failed to get player statistics',
                'details': str(e) if current_app.debug else None
            }
        }), 500

@players_bp.route('/seasons', methods=['GET'])
def get_seasons():
    """
    Get list of available NBA seasons
    """
    try:
        seasons = player_service.get_available_seasons()
        
        return jsonify({
            'data': seasons,
            'count': len(seasons)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting seasons: {str(e)}")
        return jsonify({
            'error': {
                'code': 'SEASONS_ERROR',
                'message': 'Failed to get available seasons',
                'details': str(e) if current_app.debug else None
            }
        }), 500