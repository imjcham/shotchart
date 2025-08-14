"""
Player service for handling NBA player data operations
"""

from typing import List, Dict, Any, Optional
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class PlayerService:
    """Service class for NBA player operations"""
    
    def __init__(self):
        """Initialize the player service"""
        from app.services.cache_service import CacheService
        self.cache_service = CacheService()
    
    def search_players(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for NBA players by name with caching
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of player dictionaries
        """
        # Try to get from cache first
        cached_result = self.cache_service.get_cached_response('player_search', query.lower(), limit)
        if cached_result:
            return cached_result
        
        try:
            from app.services.nba_api_service import NBAApiService
            nba_service = NBAApiService()
            
            players = nba_service.search_players(query, limit)
            
            # Cache the result
            self.cache_service.set_cached_response('player_search', players, query.lower(), limit)
            
            logger.info(f"Found {len(players)} players for query: {query}")
            return players
            
        except Exception as e:
            logger.error(f"Error searching players: {str(e)}")
            # Return empty list instead of sample data
            return []
    
    def get_player_info(self, player_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed player information with caching
        
        Args:
            player_id: NBA player ID
            
        Returns:
            Player information dictionary or None if not found
        """
        # Try to get from cache first
        cached_result = self.cache_service.get_cached_response('player_info', player_id)
        if cached_result:
            return cached_result
        
        try:
            from app.services.nba_api_service import NBAApiService
            nba_service = NBAApiService()
            
            player = nba_service.get_player_info(player_id)
            
            if player:
                # Cache the result
                self.cache_service.set_cached_response('player_info', player, player_id)
                
                logger.info(f"Retrieved player info for ID: {player_id}")
                return player
            else:
                logger.warning(f"Player not found: {player_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting player info: {str(e)}")
            # Return None instead of sample data
            return None
    
    def get_player_shots(self, player_id: int, season: str, season_type: str = 'Regular Season') -> List[Dict[str, Any]]:
        """
        Get shot chart data for a player with caching
        
        Args:
            player_id: NBA player ID
            season: NBA season (e.g., "2023-24")
            season_type: Type of season (Regular Season, Playoffs)
            
        Returns:
            List of shot dictionaries
        """
        # Try to get from cache first
        cached_result = self.cache_service.get_cached_response('player_shots', player_id, season, season_type)
        if cached_result:
            return cached_result
        
        try:
            from app.services.nba_api_service import NBAApiService
            nba_service = NBAApiService()
            
            shots = nba_service.get_shot_chart_data(player_id, season, season_type)
            
            # Cache the result
            self.cache_service.set_cached_response('player_shots', shots, player_id, season, season_type)
            
            logger.info(f"Retrieved {len(shots)} shots for player {player_id}")
            return shots
            
        except Exception as e:
            logger.error(f"Error getting player shots: {str(e)}")
            # Return empty list instead of sample data
            return []
    
    def get_player_stats(self, player_id: int, season: str) -> Dict[str, Any]:
        """
        Get shooting statistics for a player with caching
        
        Args:
            player_id: NBA player ID
            season: NBA season (e.g., "2023-24")
            
        Returns:
            Statistics dictionary
        """
        # Try to get from cache first
        cached_result = self.cache_service.get_cached_response('player_stats', player_id, season)
        if cached_result:
            return cached_result
        
        try:
            from app.services.nba_api_service import NBAApiService
            nba_service = NBAApiService()
            
            stats = nba_service.get_player_stats(player_id, season)
            
            # Cache the result
            self.cache_service.set_cached_response('player_stats', stats, player_id, season)
            
            logger.info(f"Retrieved stats for player {player_id}")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting player stats: {str(e)}")
            # Return empty stats instead of sample data
            return {
                'totalAttempts': 0,
                'totalMade': 0,
                'fieldGoalPercentage': 0.0,
                'threePointAttempts': 0,
                'threePointMade': 0,
                'threePointPercentage': 0.0,
                'averageShotDistance': 0.0
            }
    
    def get_available_seasons(self) -> List[str]:
        """
        Get list of available NBA seasons with caching
        
        Returns:
            List of season strings
        """
        # Try to get from cache first
        cached_result = self.cache_service.get_cached_response('seasons')
        if cached_result:
            return cached_result
        
        # Generate seasons from 1996-97 to current
        current_year = 2024
        seasons = []
        
        for year in range(1996, current_year + 1):
            season = f"{year}-{str(year + 1)[2:]}"
            seasons.append(season)
        
        seasons.reverse()  # Most recent first
        
        # Cache the result
        self.cache_service.set_cached_response('seasons', seasons)
        
        logger.info(f"Generated {len(seasons)} available seasons")
        return seasons