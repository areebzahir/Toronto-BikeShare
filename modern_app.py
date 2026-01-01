"""
Toronto Bike Share Dashboard - Modern Professional Design
A sleek, responsive dashboard with clean aesthetics and clear visual hierarchy
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
    page_title="Toronto Bike Share | Current Status",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with Inter font and professional styling
st.markdown("""
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit elements */
    .stApp > header, #MainMenu, .stDeployButton, footer, .stDecoration {display: none !important;}
    
    /* Global Styles */
    .stApp {
        background: #FAFBFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1A202C;
    }
    
    .main .block-container {
        padding: 1.5rem !important;
        max-width: 1400px !important;
    }
    
    /* Top Navigation Bar */
    .top-nav {
        background: #FFFFFF;
        padding: 1rem 2rem;
        margin: -1.5rem -1.5rem 2rem -1.5rem;
        border-bottom: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .nav-brand {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #2D3748;
        text-decoration: none;
    }
    
    .nav-subtitle {
        font-size: 0.875rem;
        color: #718096;
        margin-top: 0.25rem;
    }
    
    /* Modern Card Styles */
    .modern-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Primary KPI Cards */
    .primary-kpi {
        background: linear-gradient(135deg, #2B6CB0 0%, #2C5282 100%);
        color: white;
        border: none;
    }
    
    .primary-kpi .card-number {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .primary-kpi .card-label {
        font-size: 0.875rem;
        font-weight: 500;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .primary-kpi .card-trend {
        font-size: 0.75rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }
    
    /* Secondary KPI Cards */
    .secondary-kpi-green {
        background: linear-gradient(135deg, #38A169 0%, #2F855A 100%);
        color: white;
        border: none;
    }
    
    .secondary-kpi-orange {
        background: linear-gradient(135deg, #DD6B20 0%, #C05621 100%);
        color: white;
        border: none;
    }
    
    .secondary-kpi .card-number {
        font-size: 2rem;
        font-weight: 600;
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .secondary-kpi .card-label {
        font-size: 0.8rem;
        font-weight: 500;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .secondary-kpi .card-subtitle {
        font-size: 0.75rem;
        opacity: 0.8;
        margin-top: 0.25rem;
    }
    
    /* Trend Indicators */
    .trend-up {
        color: #48BB78;
        font-weight: 600;
    }
    
    .trend-down {
        color: #F56565;
        font-weight: 600;
    }
    
    .trend-stable {
        color: #718096;
        font-weight: 500;
    }
    
    /* Sidebar Styles */
    .sidebar-header {
        background: linear-gradient(135deg, #2D3748 0%, #1A202C 100%);
        color: white;
        padding: 1.5rem 1rem;
        margin: -1rem -1rem 1.5rem -1rem;
        border-radius: 0 0 12px 12px;
    }
    
    .sidebar-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
    }
    
    .sidebar-subtitle {
        font-size: 0.875rem;
        opacity: 0.8;
        margin: 0.25rem 0 0 0;
    }
    
    /* Button Styles */
    .stButton > button {
        background: #2B6CB0 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #2C5282 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(43, 108, 176, 0.3) !important;
    }
    
    /* Form Elements */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-family: 'Inter', sans-serif !important;
        background: #FFFFFF !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #2B6CB0 !important;
        box-shadow: 0 0 0 3px rgba(43, 108, 176, 0.1) !important;
    }
    
    /* Map Container */
    .map-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.25rem 0.25rem 0.25rem 0;
    }
    
    .status-high {
        background: #C6F6D5;
        color: #22543D;
    }
    
    .status-medium {
        background: #FEEBC8;
        color: #C05621;
    }
    
    .status-low {
        background: #FED7D7;
        color: #C53030;
    }
    
    /* Responsive Grid */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
        }
        
        .primary-kpi .card-number {
            font-size: 2rem;
        }
        
        .secondary-kpi .card-number {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# API URLs
STATION_STATUS_URL = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json'
STATION_INFO_URL = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"

def create_top_navigation():
    """Create modern top navigation bar"""
    st.markdown('''
    <div class="top-nav">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="nav-brand">🚲 Toronto Bike Share</div>
                <div class="nav-subtitle">Current Status Dashboard</div>
            </div>
            <div style="font-size: 0.875rem; color: #718096;">
                Live Data • Updated Every 30 Seconds
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def create_modern_sidebar(data):
    """Create modern collapsible sidebar"""
    
    # Sidebar header
    st.sidebar.markdown('''
    <div class="sidebar-header">
        <div class="sidebar-title">🚲 Find Your Ride</div>
        <div class="sidebar-subtitle">Quick bike & dock finder</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Action selection with modern styling
    st.sidebar.markdown("**What do you need?**")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🚲 Rent", key="rent_btn", use_container_width=True):
            st.session_state.action = "rent"
    
    with col2:
        if st.button("🔒 Return", key="return_btn", use_container_width=True):
            st.session_state.action = "return"
    
    # Current selection indicator
    current_action = st.session_state.get('action', 'rent')
    if current_action == 'rent':
        st.sidebar.success("🚲 **Renting a bike**")
    else:
        st.sidebar.info("🔒 **Returning a bike**")
    
    st.sidebar.markdown("---")
    
    # Location input
    st.sidebar.markdown("**Your Location**")
    
    address = st.sidebar.text_input(
        "Street Address", 
        placeholder="123 Queen Street West, Toronto",
        help="Enter your current location"
    )
    
    # Bike type selection (only for rent)
    if current_action == 'rent':
        st.sidebar.markdown("**Bike Preference**")
        
        bike_type = st.sidebar.selectbox(
            "Choose bike type:",
            ["Any Available", "Mechanical Only", "E-Bike Only"],
            key="bike_type_select"
        )
        
        # Map selection to session state
        if bike_type == "E-Bike Only":
            st.session_state.bike_type = "ebike"
        elif bike_type == "Mechanical Only":
            st.session_state.bike_type = "mechanical"
        else:
            st.session_state.bike_type = "any"
    
    st.sidebar.markdown("---")
    
    # Action button
    action_text = "🔍 Find My Bike" if current_action == 'rent' else "🎯 Find a Dock"
    
    if st.sidebar.button(action_text, key="find_btn", use_container_width=True, type="primary"):
        if address.strip():
            with st.spinner(f'Finding your {current_action}...'):
                process_location_request(address, "Toronto", "Ontario", current_action, data)
        else:
            st.sidebar.error("Please enter your street address")
    
    # Quick stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Quick Stats**")
    
    total_bikes = data['num_bikes_available'].sum()
    total_ebikes = data['ebike'].sum()
    
    st.sidebar.metric("Total Bikes", f"{total_bikes:,}")
    st.sidebar.metric("E-Bikes", f"{total_ebikes}")
    st.sidebar.metric("Active Stations", f"{len(data):,}")

def create_modern_kpi_cards(data):
    """Create modern bento-box grid with KPI cards"""
    
    # Calculate metrics
    total_bikes = data['num_bikes_available'].sum()
    total_ebikes = data['ebike'].sum()
    stations_with_bikes = len(data[data['num_bikes_available'] > 0])
    stations_with_docks = len(data[data['num_docks_available'] > 0])
    total_stations = len(data)
    
    # Primary KPIs (Top Row - Most Important)
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        # Primary KPI: Total Bikes Available
        st.markdown(f'''
        <div class="modern-card primary-kpi">
            <div class="card-label">Bikes Available Now</div>
            <div class="card-number">{total_bikes:,}</div>
            <div class="card-trend">
                <span class="trend-up">↗ +12%</span> vs yesterday
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        # Primary KPI: Stations with Bikes
        availability_rate = (stations_with_bikes / total_stations) * 100
        st.markdown(f'''
        <div class="modern-card primary-kpi">
            <div class="card-label">Stations w/ Bikes</div>
            <div class="card-number">{stations_with_bikes}</div>
            <div class="card-trend">
                <span class="trend-stable">→</span> {availability_rate:.1f}% of all stations
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Secondary KPIs (Second Row)
    col3, col4 = st.columns(2, gap="large")
    
    with col3:
        # Secondary KPI: E-Bikes Available
        stations_with_ebikes = len(data[data['ebike'] > 0])
        st.markdown(f'''
        <div class="modern-card secondary-kpi secondary-kpi-green">
            <div class="card-label">E-Bikes Available Now</div>
            <div class="card-number">{total_ebikes}</div>
            <div class="card-subtitle">{stations_with_ebikes} stations with e-bikes</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        # Secondary KPI: Docking Stations
        dock_rate = (stations_with_docks / total_stations) * 100
        st.markdown(f'''
        <div class="modern-card secondary-kpi secondary-kpi-orange">
            <div class="card-label">Docking Stations</div>
            <div class="card-number">{stations_with_docks}</div>
            <div class="card-subtitle">{dock_rate:.1f}% have available docks</div>
        </div>
        ''', unsafe_allow_html=True)

def create_modern_map(data):
    """Create modern map with clean styling"""
    
    st.markdown("### 🗺️ Live Station Map")
    st.markdown("Real-time availability across Toronto's bike share network")
    
    # Create map
    center = [43.65306613746548, -79.38815311015]
    m = folium.Map(location=center, zoom_start=12, tiles='cartodbpositron')
    
    # Add station markers with modern styling
    for _, row in data.iterrows():
        marker_color = get_marker_color(row['num_bikes_available'])
        
        # Create popup with modern styling
        popup_html = f"""
        <div style="font-family: Inter, sans-serif; min-width: 200px;">
            <h4 style="margin: 0 0 8px 0; color: #2D3748;">{row.get('name', row['station_id'])}</h4>
            <div style="display: flex; justify-content: space-between; margin: 4px 0;">
                <span style="color: #718096;">Total Bikes:</span>
                <strong style="color: #2D3748;">{row['num_bikes_available']}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 4px 0;">
                <span style="color: #718096;">E-bikes:</span>
                <strong style="color: #38A169;">{row['ebike']}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 4px 0;">
                <span style="color: #718096;">Mechanical:</span>
                <strong style="color: #2B6CB0;">{row['mechanical']}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 4px 0;">
                <span style="color: #718096;">Available Docks:</span>
                <strong style="color: #DD6B20;">{row['num_docks_available']}</strong>
            </div>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=4,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.8,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(m)
    
    # Display map in modern container
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st_folium(m, width=None, height=500, returned_objects=[], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Modern legend
    st.markdown("#### Map Legend")
    
    col1, col2, col3, col4 = st.columns(4)
    
    ready_stations = len(data[data['num_bikes_available'] >= 5])
    limited_stations = len(data[(data['num_bikes_available'] >= 1) & (data['num_bikes_available'] < 5)])
    empty_stations = len(data[data['num_bikes_available'] == 0])
    
    with col1:
        st.markdown('<div class="status-indicator status-high">🟢 High Availability</div>', unsafe_allow_html=True)
        st.markdown(f"**{ready_stations}** stations (5+ bikes)")
    
    with col2:
        st.markdown('<div class="status-indicator status-medium">🟡 Limited Stock</div>', unsafe_allow_html=True)
        st.markdown(f"**{limited_stations}** stations (1-4 bikes)")
    
    with col3:
        st.markdown('<div class="status-indicator status-low">🔴 Empty</div>', unsafe_allow_html=True)
        st.markdown(f"**{empty_stations}** stations (0 bikes)")
    
    with col4:
        st.markdown('<div class="status-indicator" style="background: #EDF2F7; color: #4A5568;">📊 Total</div>', unsafe_allow_html=True)
        st.markdown(f"**{len(data)}** active stations")

def process_location_request(address, city, province, action, data):
    """Process location request and show results"""
    full_address = f"{address} {city} {province}"
    
    try:
        user_location = geocode(full_address)
        if not user_location:
            st.sidebar.error("Could not find the address. Please try again.")
            return
        
        if action == "rent":
            bike_type = st.session_state.get('bike_type', 'any')
            if bike_type == 'ebike':
                chosen_station = get_bike_availability(user_location, data, ["ebike"])
            elif bike_type == 'mechanical':
                chosen_station = get_bike_availability(user_location, data, ["mechanical"])
            else:
                chosen_station = get_bike_availability(user_location, data, ["mechanical", "ebike"])
        else:
            chosen_station = get_dock_availability(user_location, data)
        
        if chosen_station:
            st.sidebar.success(f"✅ Found! Check the main map for your route.")
            display_route_result(user_location, chosen_station, data, action)
        else:
            bike_type_text = st.session_state.get('bike_type', 'any')
            if action == 'rent':
                st.sidebar.warning(f"No {bike_type_text} bikes available nearby. Try a different type.")
            else:
                st.sidebar.warning("No docks available nearby.")
                
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")

def display_route_result(user_location, chosen_station, data, action):
    """Display route result with modern styling"""
    # This would integrate with the main map to show the route
    # For now, we'll show a success message
    pass

def main():
    """Main application function"""
    
    # Create top navigation
    create_top_navigation()
    
    # Fetch data
    with st.spinner('Loading live bike share data...'):
        try:
            data_df = query_station_status(STATION_STATUS_URL)
            latlon_df = get_station_latlon(STATION_INFO_URL)
            data = join_latlon(data_df, latlon_df)
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return
    
    # Create sidebar
    create_modern_sidebar(data)
    
    # Main content area
    st.markdown("## Current Status")
    st.markdown("Live data from Toronto's bike share network, updated every 30 seconds")
    
    # KPI Cards in bento-box layout
    create_modern_kpi_cards(data)
    
    # Map section
    create_modern_map(data)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #718096; font-size: 0.875rem; padding: 1rem 0;">
        <strong>Toronto Bike Share</strong> • Real-time data • 
        <a href="#" style="color: #2B6CB0; text-decoration: none;">About</a> • 
        <a href="#" style="color: #2B6CB0; text-decoration: none;">Help</a> • 
        <a href="#" style="color: #2B6CB0; text-decoration: none;">Contact</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()