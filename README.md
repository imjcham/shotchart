# NBA Shot Chart Visualizer

A Go web application that creates interactive basketball shot charts using NBA API data and Google Charts.

## Features

- Interactive shot chart visualization
- Player search with typeahead functionality
- Real-time NBA shot data from stats.nba.com
- Responsive web design
- Basketball court overlay for accurate shot positioning

## Prerequisites

- Go 1.16 or higher
- Internet connection for NBA API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/imjcham/shotchart.git
cd shotchart
```

2. Install dependencies:
```bash
go mod tidy
```

3. Run the application:
```bash
go run shotcharts.go
```

4. Open your browser and navigate to `http://localhost:9001`

## Usage

1. Start typing a player's name in the search box
2. Select a player from the dropdown
3. View their shot chart with distance tooltips
4. Each dot represents a shot attempt with distance information

## API

The application uses the NBA Stats API to fetch shot chart data:
- Endpoint: `stats.nba.com/stats/shotchartdetail`
- Season: 2014-15 (configurable)
- Data includes shot coordinates, distances, and success rates

## Project Structure

```
shotchart/
├── shotcharts.go          # Main web server
├── shot/
│   └── shot.go           # NBA API integration
├── template/
│   └── shotchart.html    # HTML template
├── static/               # Static assets (CSS, JS)
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- NBA Stats API for providing shot data
- Google Charts for visualization
- jbowens/nbagame Go library for NBA API integration