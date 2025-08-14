"""
Pydantic models for player data validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List

class PlayerResponse(BaseModel):
    """Player response model"""
    id: int = Field(..., description="NBA player ID")
    firstName: str = Field(..., description="Player's first name")
    lastName: str = Field(..., description="Player's last name")
    fullName: str = Field(..., description="Player's full name")
    teamId: int = Field(..., description="Current team ID")
    teamName: str = Field(..., description="Current team name")
    position: str = Field(..., description="Player position")
    jerseyNumber: str = Field(..., description="Jersey number")
    imageUrl: Optional[str] = Field(None, description="Player headshot URL")
    
    @validator('id')
    def validate_player_id(cls, v):
        if v <= 0:
            raise ValueError('Player ID must be positive')
        return v
    
    @validator('fullName')
    def validate_full_name(cls, v):
        if not v.strip():
            raise ValueError('Full name cannot be empty')
        return v.strip()

class ShotResponse(BaseModel):
    """Shot response model"""
    id: str = Field(..., description="Unique shot identifier")
    locationX: int = Field(..., description="X coordinate on court")
    locationY: int = Field(..., description="Y coordinate on court")
    shotDistance: int = Field(..., description="Shot distance in feet")
    shotMade: bool = Field(..., description="Whether shot was made")
    shotType: str = Field(..., description="Type of shot")
    period: int = Field(..., description="Game period")
    timeRemaining: str = Field(..., description="Time remaining in period")
    shotZone: str = Field(..., description="Shot zone on court")
    
    @validator('period')
    def validate_period(cls, v):
        if v < 1 or v > 4:
            raise ValueError('Period must be between 1 and 4')
        return v
    
    @validator('shotDistance')
    def validate_shot_distance(cls, v):
        if v < 0:
            raise ValueError('Shot distance cannot be negative')
        return v

class ShotStatsResponse(BaseModel):
    """Shot statistics response model"""
    totalAttempts: int = Field(..., description="Total shot attempts")
    totalMade: int = Field(..., description="Total shots made")
    fieldGoalPercentage: float = Field(..., description="Field goal percentage")
    threePointAttempts: int = Field(..., description="Three point attempts")
    threePointMade: int = Field(..., description="Three point shots made")
    threePointPercentage: float = Field(..., description="Three point percentage")
    averageShotDistance: float = Field(..., description="Average shot distance")
    
    @validator('fieldGoalPercentage', 'threePointPercentage')
    def validate_percentage(cls, v):
        if v < 0 or v > 1:
            raise ValueError('Percentage must be between 0 and 1')
        return v
    
    @validator('totalMade')
    def validate_made_vs_attempts(cls, v, values):
        if 'totalAttempts' in values and v > values['totalAttempts']:
            raise ValueError('Made shots cannot exceed total attempts')
        return v

class PlayerSearchResponse(BaseModel):
    """Player search response model"""
    data: List[PlayerResponse] = Field(..., description="List of matching players")
    query: str = Field(..., description="Search query used")
    count: int = Field(..., description="Number of results returned")
    
    @validator('count')
    def validate_count_matches_data(cls, v, values):
        if 'data' in values and v != len(values['data']):
            raise ValueError('Count must match data length')
        return v

class ShotDataResponse(BaseModel):
    """Shot data response model"""
    data: List[ShotResponse] = Field(..., description="List of shots")
    player_id: int = Field(..., description="Player ID")
    season: str = Field(..., description="NBA season")
    season_type: str = Field(..., description="Season type")
    count: int = Field(..., description="Number of shots returned")
    
    @validator('season')
    def validate_season_format(cls, v):
        if not v or len(v) != 7 or v[4] != '-':
            raise ValueError('Season must be in format YYYY-YY')
        return v

class ErrorResponse(BaseModel):
    """Error response model"""
    error: dict = Field(..., description="Error details")
    
    class Config:
        schema_extra = {
            "example": {
                "error": {
                    "code": "PLAYER_NOT_FOUND",
                    "message": "Player with ID 999999 not found",
                    "details": "Additional error details"
                }
            }
        }