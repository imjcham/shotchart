package shot

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

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
	url = "http://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=&LeagueID=00&LastNGames=0&TeamID=0&Position=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season=2014-15&AheadBehind=&PlayerID=201935&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=Regular+Season&SeasonSegment=&GameID="
)

func GetData() [][]interface{} {
	jsonBlob, _ := http.Get(url)
	shotcharts, _ := ioutil.ReadAll(jsonBlob.Body)

	var data Shotchart
	err := json.Unmarshal(shotcharts, &data)
	if err != nil {
		fmt.Println("error:", err)
	}
	return data.ResultSets[0].RowSet
}
