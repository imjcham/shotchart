# NBA Shot Chart Visualizer

A modern web application for visualizing NBA player shot charts with a React frontend and Python Flask backend.

## Architecture

- **Frontend**: React 18 with TypeScript, Vite, D3.js, Tailwind CSS
- **Backend**: Python Flask with nba_api library
- **Development**: Docker Compose for local development

## Quick Start

1. Clone the repository
2. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Open http://localhost:3000

## Development

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.9+ (for local backend development)

### Local Development
```bash
# Start all services
docker-compose up

# Frontend only (requires backend running)
cd frontend
npm run dev

# Backend only
cd backend
python -m flask run --debug
```

## Project Structure

```
nba-shotchart-app/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   ├── types/           # TypeScript interfaces
│   │   └── utils/           # Utility functions
│   ├── public/              # Static assets
│   └── package.json
├── backend/                  # Python Flask backend
│   ├── app/
│   │   ├── services/        # Business logic
│   │   ├── models/          # Data models
│   │   ├── routes/          # API endpoints
│   │   └── utils/           # Utility functions
│   ├── requirements.txt
│   └── app.py
├── docker-compose.yml        # Development environment
└── README.md
```

## Features

- Interactive shot chart visualization
- Real-time player search with typeahead
- Shot filtering by type, period, and season
- Responsive design for mobile devices
- Comprehensive error handling
- Performance optimized with caching

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/test` - Simple test endpoint
- `GET /api/players/search?q={query}` - Search players
- `GET /api/players/{id}` - Get player details
- `GET /api/players/{id}/shots` - Get shot chart data
- `GET /api/seasons` - Get available seasons

## Troubleshooting

If you encounter issues:

1. **Check if services are running:**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **View logs:**
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

3. **Test API directly:**
   ```bash
   python test_api.py
   ```

4. **Complete reset:**
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed debugging steps.