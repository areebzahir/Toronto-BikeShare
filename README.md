# 🚲 Toronto Bike Share Dashboard

A real-time Streamlit web application for tracking bike availability at Toronto bike share stations with multiple design themes.

## 🎨 Available Versions

### 1. **Main App** (`app.py`) - Compact Vintage Design
- **Real-time Data**: Live bike availability across all Toronto bike share stations
- **Interactive Maps**: Visual representation of station locations and availability
- **Smart Search**: Find the nearest bike or dock based on your location
- **E-bike Support**: Full integration with electric bike data
- **Compact Layout**: Optimized spacing for better page fit
- **Sidebar Navigation**: Clean slide-right menu for bike finding

### 2. **Modern App** (`modern_app.py`) - Professional Design
- **Sleek Interface**: Clean, modern design with Inter font
- **Bento-box Layout**: Dynamic grid with visual hierarchy
- **High Contrast**: Accessible color palette (dark blue, green, orange)
- **Micro-interactions**: Hover effects and smooth transitions
- **Mobile Responsive**: Adapts from multi-column to single-column on mobile

### 3. **Simple Vintage App** (`simple_vintage_app.py`) - Retro Design
- **Mid-century Aesthetic**: Inspired by 1950s travel posters
- **Vintage Typography**: Anton and Special Elite fonts
- **Retro Color Palette**: Mustard yellows, dusty teals, terracotta
- **Flip-clock Cards**: Mechanical display styling
- **Nostalgic Interface**: Vintage control panel design

## Features

- **Real-time E-bike Data**: Shows actual e-bike availability (40+ e-bikes across 20+ stations)
- **Route Planning**: Get walking directions and estimated travel time
- **Bike Type Filtering**: Choose between e-bikes, mechanical bikes, or any available
- **Station Details**: Comprehensive information including bike types and dock availability
- **Live Updates**: Data refreshes automatically from Toronto's official API

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

# Run the main compact vintage app (recommended)
streamlit run app.py

# OR run the modern professional version
streamlit run modern_app.py

# OR run the simple vintage version
streamlit run simple_vintage_app.py
```

## Usage

1. **Launch the App**: The dashboard will open in your default web browser
2. **View Overview**: See real-time metrics and station map
3. **Find a Bike/Dock**: 
   - Use the sidebar to enter your location
   - Choose whether you want to rent or return a bike
   - Select bike preferences (e-bike, mechanical, or both)
   - Click "Find My Bike!" or "Find a Dock!"
4. **Get Directions**: View the route and estimated walking time to your chosen station

## File Structure

```
Toronto-BikeShare/
├── app.py                    # Main compact vintage application
├── modern_app.py             # Modern professional design
├── simple_vintage_app.py     # Simple retro design
├── helper.py                 # Utility functions for data processing
├── environment-windows.yml   # Conda environment configuration
├── requirements.txt          # Python package dependencies
└── README.md                # This file
```

## Key Functions

### Data Processing (`helper.py`)
- `query_station_status()`: Fetch real-time station data with e-bike support
- `get_station_latlon()`: Get station location information
- `join_latlon()`: Combine status and location data
- `geocode()`: Convert addresses to coordinates
- `get_bike_availability()`: Find nearest available bikes by type
- `get_dock_availability()`: Find nearest available docks
- `run_osrm()`: Calculate walking routes and times

### User Interface Features
- Interactive dashboard with real-time metrics
- Sidebar controls for user input
- Dynamic map generation with Folium
- Route visualization and travel time calculation
- Multiple design themes for different preferences

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

### Performance Tips

- The app automatically caches data for better performance
- Use the sidebar "Find" functionality to locate specific bikes
- For better route calculation, ensure your address is as specific as possible

## Dependencies

Key packages used in this application:
- **Streamlit**: Web application framework
- **Folium**: Interactive mapping
- **Pandas**: Data manipulation
- **Requests**: API communication
- **GeoPy**: Geocoding and distance calculations

## Design Themes

### Compact Vintage (app.py)
- Optimized spacing for single-page viewing
- Vintage transit poster aesthetic
- Sidebar navigation
- Real e-bike data integration

### Modern Professional (modern_app.py)
- Clean, minimalist design
- High contrast accessibility
- Bento-box grid layout
- Mobile-responsive design

### Simple Vintage (simple_vintage_app.py)
- Mid-century travel poster inspiration
- Retro color palette and typography
- Simplified vintage interface
- Nostalgic user experience
