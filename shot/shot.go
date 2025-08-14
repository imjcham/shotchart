package shot

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"

	"github.com/jbowens/nbagame/endpoints"
)

// ShotDetailRow represents a single shot attempt with location and distance information
type ShotDetailRow struct {
	LocationX    int `json:"locationX"`
	LocationY    int `json:"locationY"`
	ShotDistance int `json:"shotDistance"`
	ShotMade     int `json:"shotMade"`
	Period       int `json:"period"`
}

// Shotchart represents the complete response from the NBA stats API
type Shotchart struct {
	Parameters struct {
		AheadBehind    interface{} `json:"AheadBehind"`
		ClutchTime     interface{} `json:"ClutchTime"`
		ContextFilter  string      `json:"ContextFilter"`
		ContextMeasure string      `json:"ContextMeasure"`
		DateFrom       interface{} `json:"DateFrom"`
		DateTo         interface{} `json:"DateTo"`
		EndPeriod      interface{} `json:"EndPeriod"`
		EndRange       interface{} `json:"EndRange"`
		GameID         interface{} `json:"GameID"`
		GameSegment    interface{} `json:"GameSegment"`
		LastNGames     int         `json:"LastNGames"`
		LeagueID       string      `json:"LeagueID"`
		Location       interface{} `json:"Location"`
		Month          int         `json:"Month"`
		OpponentTeamID int         `json:"OpponentTeamID"`
		Outcome        interface{} `json:"Outcome"`
		Period         int         `json:"Period"`
		PlayerID       int         `json:"PlayerID"`
		PointDiff      interface{} `json:"PointDiff"`
		Position       interface{} `json:"Position"`
		RangeType      interface{} `json:"RangeType"`
		RookieYear     interface{} `json:"RookieYear"`
		Season         string      `json:"Season"`
		SeasonSegment  interface{} `json:"SeasonSegment"`
		SeasonType     string      `json:"SeasonType"`
		StartPeriod    interface{} `json:"StartPeriod"`
		StartRange     interface{} `json:"StartRange"`
		TeamID         int         `json:"TeamID"`
		VsConference   interface{} `json:"VsConference"`
		VsDivision     interface{} `json:"VsDivision"`
	} `json:"parameters"`
	Resource   string `json:"resource"`
	ResultSets []struct {
		Headers []string        `json:"headers"`
		Name    string          `json:"name"`
		RowSet  [][]interface{} `json:"rowSet"`
	} `json:"resultSets"`
}

const (
	// NBA Stats API endpoint for shot chart data
	baseURL = "http://stats.nba.com/stats/shotchartdetail"
	
	// Default season for shot data
	defaultSeason = "2014-15"
	
	// HTTP client timeout
	requestTimeout = 10 * time.Second
)

// createHTTPClient creates an HTTP client with proper headers for NBA Stats API
func createHTTPClient() *http.Client {
	return &http.Client{
		Timeout: requestTimeout,
	}
}

// GetData fetches raw shot chart data from NBA Stats API (legacy function)
func GetData() ([][]interface{}, error) {
	url := fmt.Sprintf("%s?Period=0&VsConference=&LeagueID=00&LastNGames=0&TeamID=0&Position=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season=%s&AheadBehind=&PlayerID=201935&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=Regular+Season&SeasonSegment=&GameID=", 
		baseURL, defaultSeason)

	client := createHTTPClient()
	resp, err := client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch shot data: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("API returned status code: %d", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response body: %w", err)
	}

	var data Shotchart
	if err := json.Unmarshal(body, &data); err != nil {
		return nil, fmt.Errorf("failed to unmarshal JSON: %w", err)
	}

	if len(data.ResultSets) == 0 {
		return nil, fmt.Errorf("no result sets in API response")
	}

	return data.ResultSets[0].RowSet, nil
}

// GetShots fetches shot chart data for a specific player using the nbagame library
func GetShots(playerID int) ([]*ShotDetailRow, error) {
	if playerID <= 0 {
		return nil, fmt.Errorf("invalid player ID: %d", playerID)
	}

	// Configure shot chart parameters
	params := endpoints.ShotChartDetailParams{
		ContextMeasure: "FGA",
		EndPeriod:      10,
		EndRange:       28800,
		LeagueID:       "00",
		PlayerID:       playerID,
		Season:         defaultSeason,
		SeasonType:     "Regular Season",
		StartPeriod:    1,
		TeamID:         0, // All teams
	}

	var resp endpoints.ShotChartDetailResponse
	if err := endpoints.DefaultRequester.Request("shotchartdetail", params, &resp); err != nil {
		return nil, fmt.Errorf("failed to request shot chart data for player %d: %w", playerID, err)
	}

	if len(resp.ShotDetails) == 0 {
		log.Printf("No shot data found for player ID: %d", playerID)
		return []*ShotDetailRow{}, nil
	}

	// Convert to our custom format for consistency
	var shots []*ShotDetailRow
	for _, shot := range resp.ShotDetails {
		shotRow := &ShotDetailRow{
			LocationX:    shot.LocationX,
			LocationY:    shot.LocationY,
			ShotDistance: shot.ShotDistance,
			ShotMade:     shot.ShotMade,
			Period:       shot.Period,
		}
		shots = append(shots, shotRow)
	}

	log.Printf("Retrieved %d shots for player ID: %d", len(shots), playerID)
	return shots, nil
}

// GetShotsByTeam fetches shot chart data for all players on a specific team
func GetShotsByTeam(teamID int, season string) ([]*ShotDetailRow, error) {
	if teamID <= 0 {
		return nil, fmt.Errorf("invalid team ID: %d", teamID)
	}

	if season == "" {
		season = defaultSeason
	}

	params := endpoints.ShotChartDetailParams{
		ContextMeasure: "FGA",
		EndPeriod:      10,
		EndRange:       28800,
		LeagueID:       "00",
		PlayerID:       0, // All players
		Season:         season,
		SeasonType:     "Regular Season",
		StartPeriod:    1,
		TeamID:         teamID,
	}

	var resp endpoints.ShotChartDetailResponse
	if err := endpoints.DefaultRequester.Request("shotchartdetail", params, &resp); err != nil {
		return nil, fmt.Errorf("failed to request shot chart data for team %d: %w", teamID, err)
	}

	var shots []*ShotDetailRow
	for _, shot := range resp.ShotDetails {
		shotRow := &ShotDetailRow{
			LocationX:    shot.LocationX,
			LocationY:    shot.LocationY,
			ShotDistance: shot.ShotDistance,
			ShotMade:     shot.ShotMade,
			Period:       shot.Period,
		}
		shots = append(shots, shotRow)
	}

	log.Printf("Retrieved %d shots for team ID: %d", len(shots), teamID)
	return shots, nil
}