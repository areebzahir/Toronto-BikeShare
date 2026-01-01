# 🚲 Toronto Bike Share Dashboard

A real-time Streamlit web application for tracking bike availability at Toronto bike share stations with authentic vintage design themes.

## 🎨 Available Versions

### 1. **Poster App** (`poster_app.py`) - Authentic Vintage Transit Poster ⭐
- **1950s-60s Aesthetic**: Inspired by mid-century travel posters and transit signage
- **Authentic Typography**: Bebas Neue, Crimson Text, and Special Elite fonts
- **Vintage Color Palette**: Aged paper, heritage blues, vintage greens, rust reds
- **Narrative Design**: Story-driven interface with "Begin Your Urban Journey"
- **Torn Paper Cards**: Asymmetrical layout with decorative corners and layered shadows
- **Heritage Frames**: Double borders and vintage document styling

### 2. **Main App** (`app.py`) - Compact Vintage Design
- **Real-time Data**: Live bike availability with sidebar navigation
- **E-bike Support**: Full integration with electric bike data (40+ e-bikes)
- **Compact Layout**: Optimized spacing for better page fit
- **Interactive Maps**: Visual station locations with route planning
- **Smart Search**: Find nearest bike or dock based on location

## Features

- **Real-time E-bike Data**: Shows actual e-bike availability (40+ e-bikes across 20+ stations)
- **Route Planning**: Get walking directions and estimated travel time
- **Bike Type Filtering**: Choose between e-bikes, mechanical bikes, or any available
- **Station Details**: Comprehensive information including bike types and dock availability
- **Live Updates**: Data refreshes automatically from Toronto's official API
- **Vintage Aesthetics**: Authentic mid-century design with narrative storytelling

## Prerequisites

- **Python 3.8+**
- **Conda** (Anaconda or Miniconda)

## Installation & Setup

### 1. Create and Activate Conda Environment

```bash
# Create environment from the provided file
conda env create -f environment-windows.yml

# Activate the environment
conda activate bikeshare_streamlit
```

### 2. Verify Installation

```bash
# Check if all packages are installed correctly
python -c "import streamlit, folium, pandas, requests, geopy; print('✅ All packages installed successfully')"
```

### 3. Run the Application

Choose which version you want to run:

```bash
# Make sure conda environment is activated first
conda activate bikeshare_streamlit

# Run the authentic vintage poster app (recommended)
streamlit run poster_app.py

# OR run the compact vintage app
streamlit run app.py
```

## Usage

1. **Launch the App**: The dashboard will open in your default web browser
2. **View Overview**: See real-time metrics and station map
3. **Find a Bike/Dock**: 
   - Use the journey planning form (poster app) or sidebar (main app)
   - Choose whether you want to rent or return a bike
   - Select bike preferences (e-bike, mechanical, or both)
   - Click "Chart My Course" or "Find My Bike!"
4. **Explore the Map**: Interactive network map with station details

## File Structure

```
Toronto-BikeShare/
├── poster_app.py             # Authentic vintage transit poster design ⭐
├── app.py                    # Compact vintage application
├── helper.py                 # Utility functions for data processing
├── environment-windows.yml   # Conda environment configuration
├── requirements.txt          # Python package dependencies
└── README.md                # This file
```

## Design Philosophy

### Authentic Vintage Transit Poster (`poster_app.py`)
- **Emotional Goals**: Nostalgia, trust, warmth, wonder
- **Typography**: 3-font system (Bebas Neue, Crimson Text, Special Elite)
- **Color Palette**: Aged paper (#FAF7F0), heritage blue (#2E5C8A), vintage green (#4A7C59)
- **Layout**: Organic, poster-inspired asymmetrical design
- **Narrative**: Story-driven content framing data as urban adventure

### Compact Vintage (`app.py`)
- **Optimized spacing** for single-page viewing
- **Sidebar navigation** for clean interface
- **Real e-bike data** integration
- **Functional focus** with vintage styling

## Key Functions

### Data Processing (`helper.py`)
- `query_station_status()`: Fetch real-time station data with e-bike support
- `get_station_latlon()`: Get station location information
- `join_latlon()`: Combine status and location data
- `geocode()`: Convert addresses to coordinates
- `get_bike_availability()`: Find nearest available bikes by type
- `get_dock_availability()`: Find nearest available docks
- `run_osrm()`: Calculate walking routes and times

## API Endpoints

The app uses Toronto's official Bike Share API:
- **Station Status**: `https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json`
- **Station Information**: `https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information`

## Current Data (Live)

- **6,200+ bikes** available system-wide
- **40+ e-bikes** available across 20+ stations
- **1,000+ stations** throughout Toronto
- **Real-time updates** every 30 seconds

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure the conda environment is activated
   ```bash
   conda activate bikeshare_streamlit
   ```

2. **API Connection Issues**: Check your internet connection and firewall settings

3. **E-bike Data Showing 0**: The app now correctly parses e-bike data from the API

4. **Map Not Loading**: Try refreshing the page or clearing browser cache

## Dependencies

Key packages used in this application:
- **Streamlit**: Web application framework
- **Folium**: Interactive mapping
- **Pandas**: Data manipulation
- **Requests**: API communication
- **GeoPy**: Geocoding and distance calculations

## Design Inspiration

The vintage poster design draws inspiration from:
- 1950s-60s National Parks posters
- Vintage railway and subway signage
- Mid-century editorial design
- Urban planning documents from the "golden age" of public transit
- Hand-printed letterpress posters
