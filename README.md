# 🚲 Toronto Bike Share Dashboard

A real-time Streamlit web application for tracking bike availability at Toronto bike share stations.

## Features

- **Real-time Data**: Live bike availability across all Toronto bike share stations
- **Interactive Maps**: Visual representation of station locations and availability
- **Smart Search**: Find the nearest bike or dock based on your location
- **Route Planning**: Get walking directions and estimated travel time
- **Bike Type Filtering**: Choose between e-bikes and mechanical bikes
- **Responsive Design**: Clean, modern interface optimized for desktop and mobile

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

#### Option A: Using PowerShell Script (Recommended for Windows)
```powershell
# Run the PowerShell launcher
.\run_app.ps1
```

#### Option B: Using Batch File
```cmd
# Run the batch launcher
run_app.bat
```

#### Option C: Direct Command
```bash
# Make sure conda environment is activated first
conda activate bikeshare_streamlit

# Run the Streamlit app
streamlit run app.py
```

## Usage

1. **Launch the App**: The dashboard will open in your default web browser
2. **View Overview**: See real-time metrics and station map
3. **Find a Bike/Dock**: 
   - Use the sidebar to enter your location
   - Choose whether you want to rent or return a bike
   - Select bike preferences (e-bike, mechanical, or both)
   - Click "Find me a bike!" or "Find me a dock!"
4. **Get Directions**: View the route and estimated walking time to your chosen station

## File Structure

```
Toronto-BikeShare/
├── app.py                    # Main Streamlit application
├── helper.py                 # Utility functions for data processing
├── environment-windows.yml   # Conda environment configuration
├── requirements.txt          # Python package dependencies
├── run_app.ps1              # PowerShell launcher script
├── run_app.bat              # Batch launcher script
└── README.md                # This file
```

## Key Functions

### Data Processing (`helper.py`)
- `query_station_status()`: Fetch real-time station data
- `get_station_latlon()`: Get station location information
- `join_latlon()`: Combine status and location data
- `geocode()`: Convert addresses to coordinates
- `get_bike_availability()`: Find nearest available bikes
- `get_dock_availability()`: Find nearest available docks
- `run_osrm()`: Calculate walking routes and times

### User Interface (`app.py`)
- Interactive dashboard with real-time metrics
- Sidebar controls for user input
- Dynamic map generation with Folium
- Route visualization and travel time calculation

## API Endpoints

The app uses Toronto's official Bike Share API:
- **Station Status**: `https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json`
- **Station Information**: `https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information`

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure the conda environment is activated
   ```bash
   conda activate bikeshare_streamlit
   ```

2. **API Connection Issues**: Check your internet connection and firewall settings

3. **Geocoding Errors**: Ensure your address is specific and includes street name

4. **Map Not Loading**: Try refreshing the page or clearing browser cache

### Performance Tips

- The app automatically caches data for better performance
- Use the "Refresh Data" button to get the latest information
- For better route calculation, ensure your address is as specific as possible

## Dependencies

Key packages used in this application:
- **Streamlit**: Web application framework
- **Folium**: Interactive mapping
- **Pandas**: Data manipulation
- **Requests**: API communication
- **GeoPy**: Geocoding and distance calculations
- **Geopandas**: Geographic data processing
