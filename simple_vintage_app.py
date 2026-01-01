"""
Toronto Bike Share Dashboard - Simple Vintage Design
A nostalgic, retro-styled dashboard that actually works
"""

import streamlit as st
import requests
import pandas as pd
import datetime as dt
import folium
from streamlit_folium import st_folium
from helper import *

# Configure Streamlit page
st.set_page_config(
    page_title="Toronto Bike Share | Vintage Board",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple vintage CSS that works
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Anton&family=Special+Elite&display=swap');
    
    .stApp > header, #MainMenu, .stDeployButton, footer, .stDecoration {display: none !important;}
    
    .stApp {
        background: #F4F1E8;
        font-family: 'Special Elite', monospace;
        color: #3D2914;
    }
    
    .main .block-container {
        padding: 1rem !important;
        max-width: 1400px !important;
    }
    
    .vintage-header {
        background: linear-gradient(135deg, #D2691E 0%, #CD853F 100%);
        color: #F4F1E8;
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border: 4px solid #8B4513;
        text-align: center;
    }
    
    .vintage-title {
        font-family: 'Anton', sans-serif;
        font-size: 3rem;
        margin: 0;
        text-transform: uppercase;
        text-shadow: 2px 2px 0 #8B4513;
    }
    
    .vintage-card {
        background: linear-gradient(135deg, #2F4F4F 0%, #1C3333 100%);
        color: #F4F1E8;
        border: 3px solid #8B4513;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px rgba(139, 69, 19, 0.3);
    }
    
    .vintage-card.primary {
        background: linear-gradient(135deg, #DAA520 0%, #B8860B 100%);
        color: #3D2914;
    }
    
    .vintage-card.secondary-teal {
        background: linear-gradient(135deg, #5F9EA0 0%, #4682B4 100%);
    }
    
    .vintage-card.secondary-terra {
        background: linear-gradient(135deg, #CD853F 0%, #D2691E 100%);
    }
    
    .card-number {
        font-family: 'Anton', sans-serif;
        font-size: 2.5rem;
        margin: 0.5rem 0;
    }
    
    .card-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    .card-subtitle {
        font-size: 0.7rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }
    
    .stButton > button {
        background: #D2691E !important;
        color: #F4F1E8 !important;
        border: 2px solid #8B4513 !important;
        border-radius: 6px !important;
        font-family: 'Special Elite', monospace !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
    }
    
    .sidebar-header {
        background: #8B4513;
        color: #F4F1E8;
        padding: 1rem;
        margin: -1rem -1rem 1rem -1rem;
        text-align: center;
        border-radius: 0 0 8px 8px;
    }
</style>
""", unsafe_allow_html=True)

# API URLs
STATION_STATUS_URL = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json'
STATION_INFO_URL = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"

def main():
    """Main application function"""
    
    # Vintage header
    st.markdown('''
    <div class="vintage-header">
        <div class="vintage-title">🚲 Toronto Bike Share</div>
        <div style="font-size: 1rem; margin-top: 0.5rem;">VINTAGE TRANSIT BOARD • EST. 2011</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown('''
    <div class="sidebar-header">
        <h2 style="margin: 0; font-family: 'Anton', sans-serif;">🎫 FIND YOUR RIDE</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">VINTAGE CONTROL PANEL</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🚲 RENT", use_container_width=True):
            st.session_state.action = "rent"
    with col2:
        if st.button("🔒 RETURN", use_container_width=True):
            st.session_state.action = "return"
    
    # Address input
    st.sidebar.markdown("**LOCATION:**")
    address = st.sidebar.text_input("Street Address", placeholder="123 Queen Street West")
    
    if st.sidebar.button("🚨 FIND STATION", use_container_width=True, type="primary"):
        if address:
            st.sidebar.success("✅ PROCESSING REQUEST...")
        else:
            st.sidebar.error("⚠️ ADDRESS REQUIRED")
    
    # Fetch data
    try:
        with st.spinner('LOADING VINTAGE TRANSIT DATA...'):
            data_df = query_station_status(STATION_STATUS_URL)
            latlon_df = get_station_latlon(STATION_INFO_URL)
            data = join_latlon(data_df, latlon_df)
        
        if data.empty:
            st.error("No data available")
            return
            
        # Calculate metrics
        total_bikes = data['num_bikes_available'].sum()
        total_ebikes = data['ebike'].sum()
        stations_with_bikes = len(data[data['num_bikes_available'] > 0])
        stations_with_docks = len(data[data['num_docks_available'] > 0])
        total_stations = len(data)
        
        # Main content
        st.markdown("## CURRENT STATUS")
        st.markdown("Live mechanical readouts from Toronto's bicycle network")
        
        # Data cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'''
            <div class="vintage-card primary">
                <div class="card-label">Bikes Available Now</div>
                <div class="card-number">{total_bikes:,}</div>
                <div class="card-subtitle">System-wide inventory</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            availability_rate = (stations_with_bikes / total_stations) * 100
            st.markdown(f'''
            <div class="vintage-card primary">
                <div class="card-label">Stations w/ Bikes</div>
                <div class="card-number">{stations_with_bikes}</div>
                <div class="card-subtitle">{availability_rate:.1f}% operational</div>
            </div>
            ''', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            stations_with_ebikes = len(data[data['ebike'] > 0])
            st.markdown(f'''
            <div class="vintage-card secondary-teal">
                <div class="card-label">E-Bikes Available</div>
                <div class="card-number">{total_ebikes}</div>
                <div class="card-subtitle">{stations_with_ebikes} electric stations</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            dock_rate = (stations_with_docks / total_stations) * 100
            st.markdown(f'''
            <div class="vintage-card secondary-terra">
                <div class="card-label">Docking Stations</div>
                <div class="card-number">{stations_with_docks}</div>
                <div class="card-subtitle">{dock_rate:.1f}% dock availability</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Map section
        st.markdown("## 🗺️ NETWORK MAP")
        
        # Create simple map
        center = [43.65306613746548, -79.38815311015]
        m = folium.Map(location=center, zoom_start=12, tiles='cartodbpositron')
        
        # Add markers
        for _, row in data.iterrows():
            marker_color = get_marker_color(row['num_bikes_available'])
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=3,
                color=marker_color,
                fill=True,
                fill_color=marker_color,
                fill_opacity=0.7,
                popup=f"Bikes: {row['num_bikes_available']}<br>E-bikes: {row['ebike']}<br>Docks: {row['num_docks_available']}"
            ).add_to(m)
        
        st_folium(m, width=None, height=400, returned_objects=[], use_container_width=True)
        
        # Legend
        col1, col2, col3 = st.columns(3)
        ready_stations = len(data[data['num_bikes_available'] >= 5])
        limited_stations = len(data[(data['num_bikes_available'] >= 1) & (data['num_bikes_available'] < 5)])
        empty_stations = len(data[data['num_bikes_available'] == 0])
        
        with col1:
            st.markdown(f"🟢 **ABUNDANT:** {ready_stations} stations")
        with col2:
            st.markdown(f"🟡 **LIMITED:** {limited_stations} stations")
        with col3:
            st.markdown(f"🔴 **EMPTY:** {empty_stations} stations")
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please check your internet connection and try refreshing the page.")

if __name__ == "__main__":
    main()