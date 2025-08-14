"""
Cache service for managing response caching with TTL
"""

from typing import Any, Optional, Dict, List
from flask import current_app
import logging
import json
import hashlib
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CacheService:
    """Service class for cache operations with TTL management"""
    
    # Cache timeout configurations (in seconds)
    CACHE_TIMEOUTS = {
        'player_search': 3600,      # 1 hour
        'player_info': 3600,        # 1 hour
        'player_shots': 1800,       # 30 minutes
        'player_stats': 1800,       # 30 minutes
        'seasons': 86400,           # 24 hours
        'default': 900              # 15 minutes
    }
    
    def __init__(self):
        """Initialize the cache service"""
        self.cache_prefix = "nba_shotchart:"
    
    def _get_cache_key(self, key_type: str, *args, **kwargs) -> str:
        """
        Generate a consistent cache key
        
        Args:
            key_type: Type of cache key (player_search, player_info, etc.)
            *args: Positional arguments for the key
            **kwargs: Keyword arguments for the key
            
        Returns:
            Generated cache key string
        """
        # Create a consistent string from args and kwargs
        key_parts = [str(arg) for arg in args]
        
        # Sort kwargs for consistency
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        
        key_string = ":".join(key_parts)
        
        # Hash long keys to avoid key length issues
        if len(key_string) > 100:
            key_hash = hashlib.md5(key_string.encode()).hexdigest()
            key_string = f"hash:{key_hash}"
        
        return f"{self.cache_prefix}{key_type}:{key_string}"
    
    def get_cached_response(self, key_type: str, *args, **kwargs) -> Optional[Any]:
        """
        Retrieve cached data
        
        Args:
            key_type: Type of cache key
            *args: Positional arguments for the key
            **kwargs: Keyword arguments for the key
            
        Returns:
            Cached data or None if not found/expired
        """
        if not hasattr(current_app, 'cache'):
            logger.warning("Cache not available")
            return None
        
        cache_key = self._get_cache_key(key_type, *args, **kwargs)
        
        try:
            cached_data = current_app.cache.get(cache_key)
            
            if cached_data is not None:
                logger.info(f"Cache hit for key: {cache_key}")
                return cached_data
            else:
                logger.debug(f"Cache miss for key: {cache_key}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving from cache: {str(e)}")
            return None
    
    def set_cached_response(self, key_type: str, data: Any, *args, **kwargs) -> bool:
        """
        Store data in cache with appropriate TTL
        
        Args:
            key_type: Type of cache key
            data: Data to cache
            *args: Positional arguments for the key
            **kwargs: Keyword arguments for the key
            
        Returns:
            True if successfully cached, False otherwise
        """
        if not hasattr(current_app, 'cache'):
            logger.warning("Cache not available")
            return False
        
        cache_key = self._get_cache_key(key_type, *args, **kwargs)
        timeout = self.CACHE_TIMEOUTS.get(key_type, self.CACHE_TIMEOUTS['default'])
        
        try:
            current_app.cache.set(cache_key, data, timeout=timeout)
            logger.info(f"Cached data for key: {cache_key} (TTL: {timeout}s)")
            return True
            
        except Exception as e:
            logger.error(f"Error storing in cache: {str(e)}")
            return False
    
    def invalidate_cache(self, pattern: str) -> int:
        """
        Invalidate cache entries matching a pattern
        
        Args:
            pattern: Pattern to match cache keys
            
        Returns:
            Number of keys invalidated
        """
        if not hasattr(current_app, 'cache'):
            logger.warning("Cache not available")
            return 0
        
        try:
            # Note: SimpleCache doesn't support pattern deletion
            # This is a limitation we'd need to address with Redis in production
            logger.warning(f"Pattern invalidation not supported with SimpleCache: {pattern}")
            return 0
            
        except Exception as e:
            logger.error(f"Error invalidating cache: {str(e)}")
            return 0
    
    def clear_player_cache(self, player_id: int) -> int:
        """
        Clear all cached data for a specific player
        
        Args:
            player_id: NBA player ID
            
        Returns:
            Number of keys cleared
        """
        if not hasattr(current_app, 'cache'):
            return 0
        
        # List of cache types that might contain player data
        cache_types = ['player_info', 'player_shots', 'player_stats']
        cleared_count = 0
        
        for cache_type in cache_types:
            try:
                # Try to clear common variations
                variations = [
                    self._get_cache_key(cache_type, player_id),
                    self._get_cache_key(cache_type, player_id, '2023-24'),
                    self._get_cache_key(cache_type, player_id, '2023-24', 'Regular Season'),
                ]
                
                for key in variations:
                    if current_app.cache.delete(key):
                        cleared_count += 1
                        logger.info(f"Cleared cache key: {key}")
                        
            except Exception as e:
                logger.error(f"Error clearing player cache: {str(e)}")
        
        return cleared_count
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics (limited with SimpleCache)
        
        Returns:
            Dictionary with cache statistics
        """
        stats = {
            'cache_type': 'SimpleCache',
            'timestamp': datetime.utcnow().isoformat(),
            'supported_operations': [
                'get', 'set', 'delete'
            ],
            'limitations': [
                'No pattern matching',
                'No hit/miss statistics',
                'No memory usage stats'
            ]
        }
        
        return stats
    
    def warm_cache(self, player_ids: List[int], seasons: List[str]) -> Dict[str, int]:
        """
        Pre-warm cache with commonly requested data
        
        Args:
            player_ids: List of player IDs to pre-load
            seasons: List of seasons to pre-load
            
        Returns:
            Dictionary with warming statistics
        """
        stats = {
            'players_warmed': 0,
            'shots_warmed': 0,
            'stats_warmed': 0,
            'errors': 0
        }
        
        try:
            from app.services.nba_api_service import NBAApiService
            nba_service = NBAApiService()
            
            for player_id in player_ids:
                try:
                    # Warm player info
                    player_info = nba_service.get_player_info(player_id)
                    if player_info:
                        self.set_cached_response('player_info', player_info, player_id)
                        stats['players_warmed'] += 1
                    
                    # Warm shot data for recent seasons
                    for season in seasons[:2]:  # Limit to 2 most recent seasons
                        try:
                            shots = nba_service.get_shot_chart_data(player_id, season)
                            if shots:
                                self.set_cached_response('player_shots', shots, player_id, season, 'Regular Season')
                                stats['shots_warmed'] += 1
                            
                            stats_data = nba_service.get_player_stats(player_id, season)
                            if stats_data:
                                self.set_cached_response('player_stats', stats_data, player_id, season)
                                stats['stats_warmed'] += 1
                                
                        except Exception as season_error:
                            logger.error(f"Error warming cache for player {player_id}, season {season}: {str(season_error)}")
                            stats['errors'] += 1
                    
                except Exception as player_error:
                    logger.error(f"Error warming cache for player {player_id}: {str(player_error)}")
                    stats['errors'] += 1
            
            logger.info(f"Cache warming completed: {stats}")
            
        except Exception as e:
            logger.error(f"Error during cache warming: {str(e)}")
            stats['errors'] += 1
        
        return stats
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform cache health check
        
        Returns:
            Health check results
        """
        health = {
            'status': 'unknown',
            'timestamp': datetime.utcnow().isoformat(),
            'cache_available': False,
            'test_key_success': False
        }
        
        try:
            if hasattr(current_app, 'cache'):
                health['cache_available'] = True
                
                # Test cache operations
                test_key = f"{self.cache_prefix}health_check"
                test_value = {'test': True, 'timestamp': health['timestamp']}
                
                # Test set
                current_app.cache.set(test_key, test_value, timeout=60)
                
                # Test get
                retrieved = current_app.cache.get(test_key)
                if retrieved and retrieved.get('test') is True:
                    health['test_key_success'] = True
                    health['status'] = 'healthy'
                else:
                    health['status'] = 'degraded'
                
                # Clean up test key
                current_app.cache.delete(test_key)
                
            else:
                health['status'] = 'unavailable'
                
        except Exception as e:
            health['status'] = 'error'
            health['error'] = str(e)
            logger.error(f"Cache health check failed: {str(e)}")
        
        return health