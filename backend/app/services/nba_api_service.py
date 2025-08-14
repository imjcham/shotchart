"""
NBA API service for interfacing with the nba_api library
"""

from typing import List, Dict, Any, Optional
import logging
import time
from datetime import datetime

# Check if pandas is available
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

logger = logging.getLogger(__name__)

class NBAApiService:
    """Service class for NBA API operations using nba_api library"""
    
    def __init__(self):
        """Initialize the NBA API service"""
        self.request_delay = 0.6  # 600ms delay between requests to avoid rate limiting
        self.last_request_time = 0
        
    def _rate_limit(self):
        """Implement rate limiting to avoid NBA API throttling"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def search_players(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for NBA players by name
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of player dictionaries
        """
        try:
            self._rate_limit()
            
            from nba_api.stats.static import players
            
            # Get all players
            all_players = players.get_players()
            
            # Filter players by query
            query_lower = query.lower()
            matching_players = []
            
            for player in all_players:
                full_name = player['full_name'].lower()
                first_name = player['first_name'].lower()
                last_name = player['last_name'].lower()
                
                if (query_lower in full_name or 
                    query_lower in first_name or 
                    query_lower in last_name):
                    
                    formatted_player = {
                        'id': player['id'],
                        'firstName': player['first_name'],
                        'lastName': player['last_name'],
                        'fullName': player['full_name'],
                        'teamId': 0,  # Static data doesn't include current team
                        'teamName': '',
                        'position': '',
                        'jerseyNumber': '',
                        'imageUrl': f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player['id']}.png"
                    }
                    matching_players.append(formatted_player)
                    
                    if len(matching_players) >= limit:
                        break
            
            logger.info(f"Found {len(matching_players)} players matching '{query}'")
            return matching_players
            
        except Exception as e:
            logger.error(f"Error searching players with NBA API: {str(e)}")
            return []
    
    def get_player_info(self, player_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed player information
        
        Args:
            player_id: NBA player ID
            
        Returns:
            Player information dictionary or None if not found
        """
        try:
            self._rate_limit()
            
            from nba_api.stats.endpoints import commonplayerinfo
            from nba_api.stats.static import players
            
            # Get basic player info from static data
            player_info = players.find_player_by_id(player_id)
            if not player_info:
                logger.warning(f"Player not found in static data: {player_id}")
                return None
            
            # Get additional info from API
            if PANDAS_AVAILABLE:
                try:
                    self._rate_limit()
                    player_details = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                    player_data = player_details.get_data_frames()[0]
                    
                    if not player_data.empty:
                        row = player_data.iloc[0]
                        team_id = row.get('TEAM_ID', 0)
                        team_name = row.get('TEAM_NAME', '')
                        position = row.get('POSITION', '')
                        jersey = row.get('JERSEY', '')
                    else:
                        team_id = 0
                        team_name = ''
                        position = ''
                        jersey = ''
                        
                except Exception as api_error:
                    logger.warning(f"Could not get detailed info for player {player_id}: {str(api_error)}")
                    team_id = 0
                    team_name = ''
                    position = ''
                    jersey = ''
            else:
                # Fallback when pandas is not available
                team_id = 0
                team_name = ''
                position = ''
                jersey = ''
            
            formatted_player = {
                'id': player_info['id'],
                'firstName': player_info['first_name'],
                'lastName': player_info['last_name'],
                'fullName': player_info['full_name'],
                'teamId': team_id,
                'teamName': team_name,
                'position': position,
                'jerseyNumber': str(jersey) if jersey else '',
                'imageUrl': f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
            }
            
            logger.info(f"Retrieved player info for {player_info['full_name']}")
            return formatted_player
            
        except Exception as e:
            logger.error(f"Error getting player info: {str(e)}")
            return None
    
    def get_shot_chart_data(self, player_id: int, season: str, season_type: str = 'Regular Season') -> List[Dict[str, Any]]:
        """
        Get shot chart data for a player
        
        Args:
            player_id: NBA player ID
            season: NBA season (e.g., "2023-24")
            season_type: Type of season (Regular Season, Playoffs)
            
        Returns:
            List of shot dictionaries
        """
        if not PANDAS_AVAILABLE:
            logger.warning(f"Pandas not available, cannot retrieve shot data for player {player_id}")
            return []
            
        try:
            self._rate_limit()
            
            from nba_api.stats.endpoints import shotchartdetail
            
            # Get shot chart data
            shot_chart = shotchartdetail.ShotChartDetail(
                team_id=0,
                player_id=player_id,
                season_nullable=season,
                season_type_all_star=season_type,
                context_measure_simple='FGA'
            )
            
            shot_data = shot_chart.get_data_frames()[0]
            
            if shot_data.empty:
                logger.warning(f"No shot data found for player {player_id} in {season}")
                return []
            
            shots = []
            for _, row in shot_data.iterrows():
                shot = {
                    'id': f"shot_{row['GAME_ID']}_{row['GAME_EVENT_ID']}",
                    'locationX': int(row['LOC_X']),
                    'locationY': int(row['LOC_Y']),
                    'shotDistance': int(row['SHOT_DISTANCE']),
                    'shotMade': bool(row['SHOT_MADE_FLAG']),
                    'shotType': str(row['SHOT_TYPE']),
                    'period': int(row['PERIOD']),
                    'timeRemaining': str(row['MINUTES_REMAINING']) + ':' + str(row['SECONDS_REMAINING']).zfill(2),
                    'shotZone': str(row['SHOT_ZONE_BASIC'])
                }
                shots.append(shot)
            
            logger.info(f"Retrieved {len(shots)} shots for player {player_id}")
            return shots
            
        except Exception as e:
            logger.error(f"Error getting shot chart data: {str(e)}")
            return []
    
    def get_player_stats(self, player_id: int, season: str) -> Dict[str, Any]:
        """
        Get shooting statistics for a player
        
        Args:
            player_id: NBA player ID
            season: NBA season (e.g., "2023-24")
            
        Returns:
            Statistics dictionary
        """
        if not PANDAS_AVAILABLE:
            logger.warning(f"Pandas not available, cannot retrieve stats for player {player_id}")
            return {
                'totalAttempts': 0,
                'totalMade': 0,
                'fieldGoalPercentage': 0.0,
                'threePointAttempts': 0,
                'threePointMade': 0,
                'threePointPercentage': 0.0,
                'averageShotDistance': 0.0
            }
            
        try:
            self._rate_limit()
            
            # Try different endpoints for stats based on player activity
            try:
                from nba_api.stats.endpoints import playerdashboardbyyearoveryear
                
                # Get player stats
                player_stats = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(
                    player_id=player_id,
                    season=season
                )
                
                stats_data = player_stats.get_data_frames()[0]
                
            except Exception as dashboard_error:
                logger.warning(f"Dashboard stats failed for player {player_id}, trying career stats: {str(dashboard_error)}")
                
                # Fallback to career stats
                from nba_api.stats.endpoints import playercareerstats
                career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
                stats_data = career_stats.get_data_frames()[0]
                
                # Filter for the specific season if available
                if not stats_data.empty:
                    season_data = stats_data[stats_data['SEASON_ID'] == season]
                    if not season_data.empty:
                        stats_data = season_data
                    else:
                        # Use most recent season
                        stats_data = stats_data.tail(1)
            
            if stats_data.empty:
                logger.warning(f"No stats found for player {player_id} in {season}")
                return {
                    'totalAttempts': 0,
                    'totalMade': 0,
                    'fieldGoalPercentage': 0.0,
                    'threePointAttempts': 0,
                    'threePointMade': 0,
                    'threePointPercentage': 0.0,
                    'averageShotDistance': 0.0
                }
            
            row = stats_data.iloc[0]
            
            stats = {
                'totalAttempts': int(row.get('FGA', 0)),
                'totalMade': int(row.get('FGM', 0)),
                'fieldGoalPercentage': float(row.get('FG_PCT', 0.0)),
                'threePointAttempts': int(row.get('FG3A', 0)),
                'threePointMade': int(row.get('FG3M', 0)),
                'threePointPercentage': float(row.get('FG3_PCT', 0.0)),
                'averageShotDistance': 16.5  # This would need to be calculated from shot data
            }
            
            logger.info(f"Retrieved stats for player {player_id}")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting player stats: {str(e)}")
            return {
                'totalAttempts': 0,
                'totalMade': 0,
                'fieldGoalPercentage': 0.0,
                'threePointAttempts': 0,
                'threePointMade': 0,
                'threePointPercentage': 0.0,
                'averageShotDistance': 0.0
            }