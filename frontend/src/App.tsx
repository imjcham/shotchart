import React, { useState } from 'react'
import { Player } from './types'
import PlayerSearch from './components/PlayerSearch'
import ShotChart from './components/ShotChart'
import PlayerInfo from './components/PlayerInfo'
import FilterControls from './components/FilterControls'
import ErrorBoundary from './components/ErrorBoundary'
import './App.css'

function App() {
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null)
  const [filters, setFilters] = useState({
    shotMade: undefined,
    period: undefined,
    shotZone: undefined,
    season: '2023-24'
  })

  const handlePlayerSelect = (player: Player) => {
    setSelectedPlayer(player)
  }

  const handleFilterChange = (newFilters: typeof filters) => {
    setFilters(newFilters)
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-purple-900">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <header className="text-center mb-8">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">
              NBA Shot Chart Visualizer
            </h1>
            <p className="text-xl text-blue-200 max-w-2xl mx-auto">
              Explore NBA player shooting patterns with interactive shot charts
            </p>
          </header>

          {/* Main Content */}
          <div className="max-w-7xl mx-auto">
            {/* Search Section */}
            <div className="relative z-10 bg-white/10 backdrop-blur-md rounded-2xl p-6 mb-8">
              <PlayerSearch 
                onPlayerSelect={handlePlayerSelect}
                disabled={false}
              />
            </div>

            {selectedPlayer ? (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Player Info */}
                <div className="lg:col-span-1">
                  <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 mb-6">
                    <PlayerInfo player={selectedPlayer} />
                  </div>
                  
                  {/* Filter Controls */}
                  <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6">
                    <FilterControls 
                      filters={filters}
                      onFilterChange={handleFilterChange}
                    />
                  </div>
                </div>

                {/* Shot Chart */}
                <div className="lg:col-span-2">
                  <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6">
                    <ShotChart 
                      playerData={selectedPlayer}
                      filters={filters}
                    />
                  </div>
                </div>
              </div>
            ) : (
              /* Welcome State */
              <div className="relative z-0 bg-white/10 backdrop-blur-md rounded-2xl p-12 text-center">
                <div className="max-w-md mx-auto">
                  <div className="text-6xl mb-6">🏀</div>
                  <h2 className="text-2xl font-bold text-white mb-4">
                    Get Started
                  </h2>
                  <p className="text-blue-200 mb-6">
                    Search for an NBA player above to view their shot chart and shooting statistics.
                  </p>
                  <div className="text-sm text-blue-300">
                    Try searching for popular players like "LeBron James", "Stephen Curry", or "Giannis Antetokounmpo"
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <footer className="text-center mt-16 text-blue-300">
            <p className="text-sm">
              Data provided by NBA.com • Built with React and D3.js
            </p>
          </footer>
        </div>
      </div>
    </ErrorBoundary>
  )
}

export default App