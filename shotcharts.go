package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"shotchart/shot"
	"strconv"
	"strings"

	"github.com/jbowens/nbagame"
)

const (
	defaultPort     = "9001"
	defaultPlayerID = 201935 // James Harden
	templatePath    = "template/shotchart.html"
)

// PageData represents the data passed to the HTML template
type PageData struct {
	ShotData       string
	AllNames       string
	PlayerImage    string
	PagePlayerName string
}

// Server represents the HTTP server with its dependencies
type Server struct {
	template    *template.Template
	playerCache map[string]int
}

// NewServer creates a new server instance
func NewServer() (*Server, error) {
	tmpl, err := template.ParseFiles(templatePath)
	if err != nil {
		return nil, fmt.Errorf("failed to parse template: %w", err)
	}

	server := &Server{
		template:    tmpl,
		playerCache: make(map[string]int),
	}

	// Pre-populate player cache
	if err := server.loadPlayerCache(); err != nil {
		log.Printf("Warning: failed to load player cache: %v", err)
	}

	return server, nil
}

// loadPlayerCache pre-loads all NBA players for faster lookups
func (s *Server) loadPlayerCache() error {
	players, err := nbagame.API.Players.All()
	if err != nil {
		return fmt.Errorf("failed to fetch players: %w", err)
	}

	for _, player := range players {
		playerName := fmt.Sprintf("%s %s", player.FirstName, player.LastName)
		s.playerCache[playerName] = player.ID
	}

	log.Printf("Loaded %d players into cache", len(s.playerCache))
	return nil
}

// getPlayerID returns the player ID for a given player name
func (s *Server) getPlayerID(playerName string) int {
	if id, exists := s.playerCache[playerName]; exists {
		return id
	}
	
	// Fallback to API call if not in cache
	players, err := nbagame.API.Players.All()
	if err != nil {
		log.Printf("Error fetching players: %v", err)
		return defaultPlayerID
	}

	for _, player := range players {
		fullName := fmt.Sprintf("%s %s", player.FirstName, player.LastName)
		if fullName == playerName {
			s.playerCache[playerName] = player.ID
			return player.ID
		}
	}

	log.Printf("Player not found: %s, using default", playerName)
	return defaultPlayerID
}

// getPlayerImage returns the NBA stats image URL for a player
func (s *Server) getPlayerImage(playerID int) string {
	return fmt.Sprintf("http://stats.nba.com/media/players/230x185/%d.png", playerID)
}

// getAllPlayerNames returns a JavaScript-formatted string of all player names
func (s *Server) getAllPlayerNames() string {
	if len(s.playerCache) == 0 {
		// Fallback if cache is empty
		s.loadPlayerCache()
	}

	var names []string
	for name := range s.playerCache {
		names = append(names, fmt.Sprintf("\"%s\"", name))
	}

	return strings.Join(names, ",")
}

// processRequest extracts player information from the HTTP request
func (s *Server) processRequest(r *http.Request) (int, string) {
	if err := r.ParseForm(); err != nil {
		log.Printf("Error parsing form: %v", err)
		return defaultPlayerID, ""
	}

	playerNames := r.Form["names"]
	if len(playerNames) == 0 || playerNames[0] == "" {
		return defaultPlayerID, ""
	}

	playerName := strings.TrimSpace(playerNames[0])
	playerID := s.getPlayerID(playerName)
	
	log.Printf("Request for player: %s (ID: %d)", playerName, playerID)
	return playerID, playerName
}

// formatShotData converts shot data to JavaScript array format
func (s *Server) formatShotData(shots []*shot.ShotDetailRow) string {
	if len(shots) == 0 {
		return ""
	}

	var data strings.Builder
	for i, shot := range shots {
		if i > 0 {
			data.WriteString(",")
		}
		data.WriteString(fmt.Sprintf("[%d, %d, '%d feet']", 
			shot.LocationX, shot.LocationY, shot.ShotDistance))
	}

	return data.String()
}

// homeHandler handles the main page requests
func (s *Server) homeHandler(w http.ResponseWriter, r *http.Request) {
	playerID, playerName := s.processRequest(r)
	
	// Get shot data
	shotData, err := shot.GetShots(playerID)
	if err != nil {
		log.Printf("Error getting shot data for player %d: %v", playerID, err)
		http.Error(w, "Failed to load shot data", http.StatusInternalServerError)
		return
	}

	// Prepare template data
	pageData := PageData{
		ShotData:       s.formatShotData(shotData),
		AllNames:       s.getAllPlayerNames(),
		PlayerImage:    s.getPlayerImage(playerID),
		PagePlayerName: playerName,
	}

	// Execute template
	if err := s.template.Execute(w, pageData); err != nil {
		log.Printf("Error executing template: %v", err)
		http.Error(w, "Failed to render page", http.StatusInternalServerError)
		return
	}
}

// staticHandler serves static files
func (s *Server) staticHandler(w http.ResponseWriter, r *http.Request) {
	// Remove leading slash and serve file
	filePath := r.URL.Path[1:]
	
	// Basic security check
	if strings.Contains(filePath, "..") {
		http.Error(w, "Invalid file path", http.StatusBadRequest)
		return
	}

	http.ServeFile(w, r, filePath)
}

// setupRoutes configures the HTTP routes
func (s *Server) setupRoutes() {
	http.HandleFunc("/", s.homeHandler)
	http.HandleFunc("/images/", s.staticHandler)
	http.HandleFunc("/css/", s.staticHandler)
	http.HandleFunc("/static/", s.staticHandler)
	
	// Serve typeahead bundle
	http.HandleFunc("/typeahead.bundle.js", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/javascript")
		http.ServeFile(w, r, "typeahead.bundle.js")
	})
}

// getPort returns the port to listen on
func getPort() string {
	if port := os.Getenv("PORT"); port != "" {
		return port
	}
	return defaultPort
}

func main() {
	// Create server instance
	server, err := NewServer()
	if err != nil {
		log.Fatalf("Failed to create server: %v", err)
	}

	// Setup routes
	server.setupRoutes()

	// Get port
	port := getPort()
	
	log.Printf("Starting NBA Shot Chart server on port %s", port)
	log.Printf("Visit http://localhost:%s to view the application", port)

	// Start server
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}