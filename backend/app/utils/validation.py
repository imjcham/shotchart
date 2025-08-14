"""
Input validation utilities for API endpoints
"""

from typing import Optional, Dict, Any

def validate_player_search(query: str, limit: int) -> Optional[Dict[str, Any]]:
    """
    Validate player search parameters
    
    Args:
        query: Search query string
        limit: Maximum number of results
        
    Returns:
        Error dict if validation fails, None if valid
    """
    if not query:
        return {
            'code': 'MISSING_QUERY',
            'message': 'Search query parameter "q" is required'
        }
    
    if len(query) < 2:
        return {
            'code': 'QUERY_TOO_SHORT',
            'message': 'Search query must be at least 2 characters long'
        }
    
    if len(query) > 100:
        return {
            'code': 'QUERY_TOO_LONG',
            'message': 'Search query must be less than 100 characters'
        }
    
    if limit < 1 or limit > 50:
        return {
            'code': 'INVALID_LIMIT',
            'message': 'Limit must be between 1 and 50'
        }
    
    return None

def validate_player_id(player_id: int) -> Optional[Dict[str, Any]]:
    """
    Validate NBA player ID
    
    Args:
        player_id: NBA player ID
        
    Returns:
        Error dict if validation fails, None if valid
    """
    if not isinstance(player_id, int):
        return {
            'code': 'INVALID_PLAYER_ID_TYPE',
            'message': 'Player ID must be an integer'
        }
    
    if player_id <= 0:
        return {
            'code': 'INVALID_PLAYER_ID',
            'message': 'Player ID must be a positive integer'
        }
    
    # NBA player IDs can range from 3 digits to 7 digits
    if player_id < 1 or player_id > 9999999:
        return {
            'code': 'INVALID_PLAYER_ID_RANGE',
            'message': 'Player ID must be between 1 and 9999999'
        }
    
    return None

def validate_season(season: str) -> Optional[Dict[str, Any]]:
    """
    Validate NBA season format
    
    Args:
        season: Season string (e.g., "2023-24")
        
    Returns:
        Error dict if validation fails, None if valid
    """
    if not season:
        return {
            'code': 'MISSING_SEASON',
            'message': 'Season parameter is required'
        }
    
    # Season format: YYYY-YY (e.g., "2023-24")
    if len(season) != 7 or season[4] != '-':
        return {
            'code': 'INVALID_SEASON_FORMAT',
            'message': 'Season must be in format YYYY-YY (e.g., "2023-24")'
        }
    
    try:
        start_year = int(season[:4])
        end_year = int(season[5:7])
        
        # Validate year range (NBA started in 1946)
        if start_year < 1946 or start_year > 2030:
            return {
                'code': 'INVALID_SEASON_YEAR',
                'message': 'Season year must be between 1946 and 2030'
            }
        
        # End year should be start year + 1 (last 2 digits)
        expected_end = (start_year + 1) % 100
        if end_year != expected_end:
            return {
                'code': 'INVALID_SEASON_SEQUENCE',
                'message': f'Invalid season sequence. Expected {start_year}-{expected_end:02d}'
            }
        
    except ValueError:
        return {
            'code': 'INVALID_SEASON_FORMAT',
            'message': 'Season must contain valid years'
        }
    
    return None