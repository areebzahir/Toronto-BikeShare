"""
Helper functions for the Toronto Bike Share Dashboard
Contains utility functions for data fetching, processing, and mapping
"""

import requests
import pandas as pd
import json
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import streamlit as st

def query_station_status(url):
    """
    Fetch station status data from the Toronto Bike Share API
    
    Args:
        url (str): API endpoint URL for station status
        
    Returns:
        pandas.DataFrame: DataFrame containing station status information
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        stations = data['data']['stations']
        
        # Process station data
        processed_data = []
        for station in stations:
            station_info = {
                'station_id': station['station_id'],
                'num_bikes_available': station['num_bikes_available'],
                'num_docks_available': station['num_docks_available'],
                'is_installed': station['is_installed'],
                'is_renting': station['is_renting'],
                'is_returning': station['is_returning'],
                'last_reported': station['last_reported']
            }
            
            # Parse vehicle types if available
            if 'vehicle_types_available' in station:
                ebike_count = 0
                mechanical_count = 0
                
                for vehicle_type in station['vehicle_types_available']:
                    if vehicle_type['vehicle_type_id'] == 'ebike':
                        ebike_count = vehicle_type['count']
                    elif vehicle_type['vehicle_type_id'] == 'mechanical':
                        mechanical_count = vehicle_type['count']
                
                station_info['ebike'] = ebike_count
                station_info['mechanical'] = mechanical_count
            else:
                # Fallback if vehicle types not available
                station_info['ebike'] = 0
                station_info['mechanical'] = station['num_bikes_available']
            
            processed_data.append(station_info)
        
        return pd.DataFrame(processed_data)
        
    except requests.RequestException as e:
        st.error(f"Error fetching station status: {str(e)}")
        return pd.DataFrame()
    except (KeyError, json.JSONDecodeError) as e:
        st.error(f"Error parsing station status data: {str(e)}")
        return pd.DataFrame()

def get_station_latlon(url):
    """
    Fetch station location data from the Toronto Bike Share API
    
    Args:
        url (str): API endpoint URL for station information
        
    Returns:
        pandas.DataFrame: DataFrame containing station location information
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        stations = data['data']['stations']
        
        # Process location data
        location_data = []
        for station in stations:
            location_info = {
                'station_id': station['station_id'],
                'name': station['name'],
                'lat': station['lat'],
                'lon': station['lon'],
                'capacity': station['capacity']
            }
            location_data.append(location_info)
        
        return pd.DataFrame(location_data)
        
    except requests.RequestException as e:
        st.error(f"Error fetching station locations: {str(e)}")
        return pd.DataFrame()
    except (KeyError, json.JSONDecodeError) as e:
        st.error(f"Error parsing station location data: {str(e)}")
        return pd.DataFrame()

def join_latlon(status_df, location_df):
    """
    Join station status data with location data
    
    Args:
        status_df (pandas.DataFrame): Station status data
        location_df (pandas.DataFrame): Station location data
        
    Returns:
        pandas.DataFrame: Combined DataFrame with status and location data
    """
    if status_df.empty or location_df.empty:
        return pd.DataFrame()
    
    # Merge on station_id
    merged_df = pd.merge(status_df, location_df, on='station_id', how='inner')
    
    # Filter for active stations only
    active_stations = merged_df[
        (merged_df['is_installed'] == 1) & 
        (merged_df['is_renting'] == 1)
    ].copy()
    
    return active_stations

def geocode(address):
    """
    Convert an address to latitude and longitude coordinates
    
    Args:
        address (str): Street address to geocode
        
    Returns:
        list or str: [latitude, longitude] if successful, empty string if failed
    """
    try:
        geolocator = Nominatim(user_agent="toronto_bikeshare_app")
        location = geolocator.geocode(address, timeout=10)
        
        if location:
            return [location.latitude, location.longitude]
        else:
            return ''
            
    except Exception as e:
        st.error(f"Geocoding error: {str(e)}")
        return ''

def get_marker_color(num_bikes):
    """
    Determine marker color based on number of available bikes
    
    Args:
        num_bikes (int): Number of available bikes at station
        
    Returns:
        str: Color code for the marker
    """
    if num_bikes >= 5:
        return 'green'
    elif num_bikes >= 1:
        return 'orange'
    else:
        return 'red'

def calculate_distance(point1, point2):
    """
    Calculate distance between two geographic points
    
    Args:
        point1 (list): [latitude, longitude] of first point
        point2 (list): [latitude, longitude] of second point
        
    Returns:
        float: Distance in kilometers
    """
    return geodesic(point1, point2).kilometers

def get_bike_availability(user_location, data, bike_modes):
    """
    Find the nearest station with available bikes matching user preferences
    
    Args:
        user_location (list): [latitude, longitude] of user
        data (pandas.DataFrame): Station data
        bike_modes (list): List of preferred bike types ('ebike', 'mechanical')
        
    Returns:
        list or None: [station_id, latitude, longitude] of best station, None if no suitable station
    """
    if not bike_modes:
        bike_modes = ['ebike', 'mechanical']
    
    # Filter stations based on bike availability and preferences
    available_stations = data.copy()
    
    # Filter based on bike type preferences
    if 'ebike' in bike_modes and 'mechanical' in bike_modes:
        # User wants any type of bike
        available_stations = available_stations[available_stations['num_bikes_available'] > 0]
    elif 'ebike' in bike_modes:
        # User wants only e-bikes
        available_stations = available_stations[available_stations['ebike'] > 0]
    elif 'mechanical' in bike_modes:
        # User wants only mechanical bikes
        available_stations = available_stations[available_stations['mechanical'] > 0]
    else:
        return None
    
    if available_stations.empty:
        return None
    
    # Calculate distances and find nearest station
    available_stations = available_stations.copy()
    available_stations['distance'] = available_stations.apply(
        lambda row: calculate_distance(user_location, [row['lat'], row['lon']]), 
        axis=1
    )
    
    # Sort by distance and get the nearest station
    nearest_station = available_stations.loc[available_stations['distance'].idxmin()]
    
    return [nearest_station['station_id'], nearest_station['lat'], nearest_station['lon']]

def get_dock_availability(user_location, data):
    """
    Find the nearest station with available docks for bike return
    
    Args:
        user_location (list): [latitude, longitude] of user
        data (pandas.DataFrame): Station data
        
    Returns:
        list or None: [station_id, latitude, longitude] of best station, None if no suitable station
    """
    # Filter stations with available docks and accepting returns
    available_stations = data[
        (data['num_docks_available'] > 0) & 
        (data['is_returning'] == 1)
    ].copy()
    
    if available_stations.empty:
        return None
    
    # Calculate distances and find nearest station
    available_stations['distance'] = available_stations.apply(
        lambda row: calculate_distance(user_location, [row['lat'], row['lon']]), 
        axis=1
    )
    
    # Sort by distance and get the nearest station
    nearest_station = available_stations.loc[available_stations['distance'].idxmin()]
    
    return [nearest_station['station_id'], nearest_station['lat'], nearest_station['lon']]

def run_osrm(station_coords, user_location):
    """
    Get route coordinates and duration using OSRM routing service
    
    Args:
        station_coords (list): [station_id, latitude, longitude] of destination
        user_location (list): [latitude, longitude] of user
        
    Returns:
        tuple: (coordinates_list, duration_string)
    """
    try:
        # OSRM demo server - for production, consider using your own instance
        osrm_url = "http://router.project-osrm.org/route/v1/walking"
        
        # Format coordinates for OSRM (longitude,latitude)
        start_coords = f"{user_location[1]},{user_location[0]}"
        end_coords = f"{station_coords[2]},{station_coords[1]}"
        
        # Build request URL
        request_url = f"{osrm_url}/{start_coords};{end_coords}?overview=full&geometries=geojson"
        
        response = requests.get(request_url, timeout=10)
        response.raise_for_status()
        
        route_data = response.json()
        
        if route_data['code'] == 'Ok' and route_data['routes']:
            route = route_data['routes'][0]
            
            # Extract coordinates (convert from [lon, lat] to [lat, lon])
            coordinates = [
                [coord[1], coord[0]] 
                for coord in route['geometry']['coordinates']
            ]
            
            # Calculate duration in minutes
            duration_seconds = route['duration']
            duration_minutes = int(duration_seconds / 60)
            
            if duration_minutes < 1:
                duration_str = "< 1 min"
            else:
                duration_str = f"{duration_minutes} min"
            
            return coordinates, duration_str
        else:
            # Fallback: return straight line
            return [user_location, [station_coords[1], station_coords[2]]], "N/A"
            
    except Exception as e:
        st.warning(f"Could not calculate route: {str(e)}")
        # Fallback: return straight line between points
        return [user_location, [station_coords[1], station_coords[2]]], "N/A"

def format_station_popup(station_data):
    """
    Format station information for map popup
    
    Args:
        station_data (pandas.Series): Station data row
        
    Returns:
        str: Formatted HTML string for popup
    """
    return f"""
    <div style="font-family: Arial, sans-serif;">
        <h4>{station_data.get('name', 'Station')}</h4>
        <p><strong>Station ID:</strong> {station_data['station_id']}</p>
        <p><strong>Total Bikes:</strong> {station_data['num_bikes_available']}</p>
        <p><strong>Mechanical Bikes:</strong> {station_data['mechanical']}</p>
        <p><strong>E-Bikes:</strong> {station_data['ebike']}</p>
        <p><strong>Available Docks:</strong> {station_data['num_docks_available']}</p>
        <p><strong>Capacity:</strong> {station_data.get('capacity', 'N/A')}</p>
    </div>
    """