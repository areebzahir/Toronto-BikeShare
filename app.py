"""
Toronto Bike Share Dashboard - Vintage Transit Poster Design
A beautiful, vintage-styled dashboard with real-time bike share data
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
    page_title="Toronto Bike Share | A Journey Through the City",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Vintage transit poster CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2family=Bebas+Neue:wght@400;700&family=Crimson+Text:wght@400;600&display=swap');
    
    /* Hide Streamlit elements */
    .stApp > header, #MainMenu, .stDeployButton, footer, .stDecoration {display: none !important;}
    
    /* Global Styles */
    .stApp {
        background-color: #FAF7F0;
        font-family: 'Crimson Text', serif;
        color: #2C2416;
    }
    
    .main .block-container {
        padding: 2rem !important;
        max-width: 1200px !important;
    }
    
    /* Typography */
    .vintage-title {
        font-family: 'Bebas Neue', Arial Black, sans-serif !important;
        font-size: 4rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin: 2rem 0 !important;
        text-transform: uppercase !important;
    }
    
    .title-bike { color: #922b0d !important; }
    .title-share { color: #2E5C8A !important; }
    
    .section-title {
        font-family: 'Bebas Neue', Arial Black, sans-serif !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin: 2rem 0 !important;
        text-transform: uppercase !important;
        color: #2C2416 !important;
    }
    
    /* Cards */
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 3px solid #2C2416;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 8px 8px 0 -2px #FAF7F0, 8px 8px 0 0 #B67C6D;
    }
    
    .hero-card {
        background: linear-gradient(135deg, #922b0d 0%, #7a2409 100%);
        color: white;
    }
    
    .success-card {
        background: linear-gradient(135deg, #01874a 0%, #016a3a 100%);
        color: white;
    }
    
    .info-card {
        background: linear-gradient(135deg, #2E5C8A 0%, #254A73 100%);
        color: white;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #D4A574 0%, #C19660 100%);
        color: white;
    }
    
    .card-number {
        font-family: 'Bebas Neue', Arial Black, sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin: 1rem 0;
    }
    
    .card-label {
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-weight: 600;
        opacity: 0.9;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #922b0d 0%, #7a2409 100%) !important;
        color: white !important;
        border: 3px solid #922b0d !important;
        border-radius: 8px !important;
        font-family: 'Bebas Neue', Arial Black, sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        padding: 1rem 2rem !important;
        font-size: 1.125rem !important;
    }
    
    /* Form elements */
    .stSelectbox > div > div > select,
    .stTextInput > div > div > input {
        border: 2px solid #8B8661 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-family: 'Crimson Text', serif !important;
        background-color: #faefe8 !important;
        color: #2C2416 !important;
    }
</style>
""", unsafe_allow_html=True)

# API URLs
STATION_STATUS_URL = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json'
STATION_INFO_URL = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"

def main():
    """Main application function"""
    
    # Initialize session state
    if 'action' not in st.session_state:
        st.session_state.action = "rent"
    
    # Header
    create_header()
    
    # Fetch data
    with st.spinner('Loading bike share data...'):
        try:
            data_df = query_station_status(STATION_STATUS_URL)
            latlon_df = get_station_latlon(STATION_INFO_URL)
            data = join_latlon(data_df, latlon_df)
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return
    
    # Status section
    create_status_section(data)
    
    # Sidebar for bike finding
    create_sidebar_find_bike(data)
    
    # Map section
    create_map_section(data)
    
    # Footer
    create_footer()

def create_header():
    """Create the header"""
    current_time = dt.datetime.now().strftime("%A, %B %d, %Y")
    
    # Overline
    st.markdown('<p style="text-align: center; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.3em; color: #6B5D4F; margin-bottom: 1rem;">━━━ City of Toronto ━━━</p>', unsafe_allow_html=True)
    
    # Main title
    st.markdown('<h1 class="vintage-title"><span class="title-bike">BIKE</span> <span class="title-share">SHARE</span></h1>', unsafe_allow_html=True)
    
    # Decorations
    st.markdown('<div style="text-align: center; font-size: 2rem; margin: 1rem 0;">🚲 ━━━━━━━━━━━━━━━━ 🚲</div>', unsafe_allow_html=True)
    
    # Subtitle
    st.markdown('<p style="font-size: 1.5rem; color: #6B5D4F; text-align: center; margin: 1rem 0;">Your Journey Across Toronto Begins Here</p>', unsafe_allow_html=True)
    
    # Date
    st.markdown(f'<div style="text-align: center; margin: 2rem 0;"><div style="font-family: monospace; font-size: 0.875rem; background: rgba(255,255,255,0.5); padding: 0.75rem 1.5rem; border: 2px solid #2C2416; border-radius: 8px; display: inline-block;">🕐 {current_time}</div></div>', unsafe_allow_html=True)

def create_status_section(data):
    """Create the status section"""
    # Calculate metrics
    total_bikes = sum(data['num_bikes_available'])
    stations_with_bikes = len(data[data['num_bikes_available'] > 0])
    stations_with_docks = len(data[data['num_docks_available'] > 0])
    total_stations = len(data)
    
    bike_availability_rate = (stations_with_bikes / total_stations) * 100
    dock_availability_rate = (stations_with_docks / total_stations) * 100
    
    # Status intro
    st.markdown('<div style="text-align: center; margin: 3rem 0 2rem;"><div style="display: inline-block; padding: 0.5rem 1.5rem; border: 2px solid #2E5C8A; border-radius: 50px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.2em; color: #2E5C8A; background: rgba(46,92,138,0.1); font-weight: 600;">🧭 Real-Time System Status</div></div>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 1.5rem; line-height: 1.6; font-style: italic; color: #2C2416; text-align: center; max-width: 600px; margin: 0 auto 2rem;">Across the bustling streets of Toronto, thousands of bicycles await their next adventure. Where will yours take you today</p>', unsafe_allow_html=True)
    
    # Section title
    st.markdown('<h2 class="section-title"><span style="color: #922b0d;">CURRENT</span> STATUS</h2>', unsafe_allow_html=True)
    
    # Hero card and E-bikes
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f'''
        <div class="metric-card hero-card">
            <div class="card-label">Bikes Available Now</div>
            <div class="card-number">{total_bikes:,}</div>
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.875rem; font-weight: 600; display: inline-block;">System-wide Availability</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Calculate ebike metrics
    total_ebikes = data['ebike'].sum()
    stations_with_ebikes = len(data[data['ebike'] > 0])
    
    with col2:
        st.markdown(f'''
        <div class="metric-card warning-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <div class="card-label">E-Bikes Available Now</div>
            <div style="font-family: 'Bebas Neue', Arial Black, sans-serif; font-size: 2rem; font-weight: 700; margin: 1rem 0;">{total_ebikes:,}</div>
            <p style="font-size: 0.875rem; opacity: 0.9;">{stations_with_ebikes} stations with e-bikes</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Stats row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card success-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📍</div>
            <div class="card-label">Stations w/ Bikes</div>
            <div class="card-number">{stations_with_bikes}</div>
            <div style="font-size: 1.5rem; opacity: 0.8;">/{total_stations}</div>
            <div style="font-size: 0.875rem; margin-top: 0.5rem; font-weight: 600;">{bike_availability_rate:.1f}% Ready</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card info-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔒</div>
            <div class="card-label">Docking Stations</div>
            <div class="card-number">{stations_with_docks}</div>
            <div style="font-size: 1.5rem; opacity: 0.8;">/{total_stations}</div>
            <div style="font-size: 0.875rem; margin-top: 0.5rem; font-weight: 600;">{dock_availability_rate:.1f}% Available</div>
        </div>
        ''', unsafe_allow_html=True)

def create_sidebar_find_bike(data):
    """Create the find bike functionality in the sidebar"""
    
    # Sidebar header with vintage styling
    st.sidebar.markdown('''
    <div style="
        background: linear-gradient(135deg, #922b0d 0%, #7a2409 100%);
        color: white;
        padding: 1.5rem 1rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        border-radius: 0 0 15px 15px;
    ">
        <h2 style="
            font-family: 'Bebas Neue', Arial Black, sans-serif; 
            font-size: 1.8rem; 
            margin: 0; 
            text-transform: uppercase;
            text-shadow: 2px 2px 0 rgba(0,0,0,0.3);
        ">🚲 Find Your Ride</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">
            Get started in seconds
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Action selection
    st.sidebar.markdown("### What do you need?")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🚲 Rent", key="rent_btn", use_container_width=True):
            st.session_state.action = "rent"
    
    with col2:
        if st.button("🔒 Return", key="return_btn", use_container_width=True):
            st.session_state.action = "return"
    
    # Show current selection
    current_action = st.session_state.get('action', 'rent')
    if current_action == 'rent':
        st.sidebar.success("🚲 **Renting a bike**")
    else:
        st.sidebar.info("🔒 **Returning a bike**")
    
    st.sidebar.markdown("---")
    
    # Location input
    st.sidebar.markdown("### Where are you?")
    
    # Geolocation button
    if st.sidebar.button("📍 Use My Location", key="geo_btn", use_container_width=True):
        st.sidebar.info("🔄 Geolocation coming soon! Enter address below.")
    
    # Address input
    address = st.sidebar.text_input(
        "Street Address", 
        placeholder="123 Queen Street West, Toronto",
        help="Enter your street address in Toronto"
    )
    
    # City and Province (auto-filled)
    col1, col2 = st.sidebar.columns(2)
    with col1:
        city = st.text_input("City", value="Toronto", disabled=True)
    with col2:
        province = st.text_input("Province", value="Ontario", disabled=True)
    
    # Bike type selection (only for rent)
    if current_action == 'rent':
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Bike Preference")
        
        bike_type = st.sidebar.radio(
            "Choose bike type:",
            ["Any Available", "Mechanical Only", "E-Bike Only"],
            key="bike_type_radio"
        )
        
        # Map radio selection to session state
        if bike_type == "E-Bike Only":
            st.session_state.bike_type = "ebike"
        elif bike_type == "Mechanical Only":
            st.session_state.bike_type = "mechanical"
        else:
            st.session_state.bike_type = "any"
    
    st.sidebar.markdown("---")
    
    # Action button
    action_text = "🚀 Find My Bike!" if current_action == 'rent' else "🎯 Find a Dock!"
    
    if st.sidebar.button(action_text, key="journey_btn", use_container_width=True, type="primary"):
        if address.strip():
            with st.spinner(f'🔍 Finding your {current_action}...'):
                process_location_request(address, city, province, current_action, data)
        else:
            st.sidebar.error("⚠️ Please enter your street address")
    
    # Help section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Tips")
    st.sidebar.markdown("""
    - **E-bikes** may be limited in winter
    - **Popular areas** fill up quickly
    - **Check the map** for real-time availability
    - **Docks** are needed to return bikes
    """)

def create_find_ride_section(data):
    """Create the find ride section with exact design match"""
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Custom styled form matching the design
        st.markdown('''
        <div style="background: white; padding: 2.5rem; border: 3px solid #2C2416; border-radius: 12px; margin: 2rem 0; box-shadow: 8px 8px 0 -2px #FAF7F0, 8px 8px 0 0 #B67C6D;">
            <h3 style="font-family: 'Bebas Neue', Arial Black, sans-serif; font-size: 2.5rem; font-weight: 700; text-align: center; margin-bottom: 1rem; text-transform: uppercase; color: #2C2416; letter-spacing: 0.05em;">FIND YOUR RIDE</h3>
            <p style="color: #9B9B9B; font-size: 1.125rem; text-align: center; margin-bottom: 2rem; line-height: 1.6;">Tell us where you are and we will guide you to the nearest bike</p>
            <div style="border-bottom: 2px dotted #CCCCCC; margin-bottom: 2rem;"></div>
        </div>
        ''', unsafe_allow_html=True)
        
        # I NEED TO section
        st.markdown('<div style="margin-bottom: 1.5rem;"><label style="font-size: 0.875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #2C2416; margin-bottom: 0.75rem; display: block;">I NEED TO</label></div>', unsafe_allow_html=True)
        
        # Custom styled buttons
        col_rent, col_return = st.columns(2)
        
        with col_rent:
            rent_style = "background: #922b0d; color: white; border: 2px solid #922b0d;" if st.session_state.get('action') == 'rent' else "background: white; color: #666; border: 2px solid #E5E5E5;"
            if st.button("🚲 Rent a Bike", key="rent_btn"):
                st.session_state.action = "rent"
        
        with col_return:
            return_style = "background: #922b0d; color: white; border: 2px solid #922b0d;" if st.session_state.get('action') == 'return' else "background: white; color: #666; border: 2px solid #E5E5E5;"
            if st.button("⚓ Return a Bike", key="return_btn"):
                st.session_state.action = "return"
        
        # YOUR LOCATION section
        st.markdown('<div style="margin: 2rem 0 1rem;"><label style="font-size: 0.875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #2C2416; margin-bottom: 0.75rem; display: block;">YOUR LOCATION</label></div>', unsafe_allow_html=True)
        
        # Custom styled input
        address = st.text_input("Street Address", placeholder="123 Queen Street West", key="address_input", label_visibility="collapsed")
        
        # CITY and PROVINCE
        col_city, col_province = st.columns(2)
        
        with col_city:
            st.markdown('<label style="font-size: 0.875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #2C2416; margin-bottom: 0.5rem; display: block;">CITY</label>', unsafe_allow_html=True)
            city = st.text_input("City", value="Toronto", key="city_input", label_visibility="collapsed")
        
        with col_province:
            st.markdown('<label style="font-size: 0.875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #2C2416; margin-bottom: 0.5rem; display: block;">PROVINCE</label>', unsafe_allow_html=True)
            province = st.text_input("Province", value="Ontario", key="province_input", label_visibility="collapsed")
        
        # BIKE TYPE section (only for rent)
        if st.session_state.get('action') == 'rent':
            st.markdown('<div style="margin: 2rem 0 1rem;"><label style="font-size: 0.875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #2C2416; margin-bottom: 0.75rem; display: block;">BIKE TYPE</label></div>', unsafe_allow_html=True)
            
            # Custom bike type buttons
            col_mech, col_ebike = st.columns(2)
            
            with col_mech:
                if st.button("Mechanical", key="mechanical_btn", use_container_width=True):
                    st.session_state.bike_type = "mechanical"
            
            with col_ebike:
                if st.button("E-Bike", key="ebike_btn", use_container_width=True):
                    st.session_state.bike_type = "ebike"
        
        # Action button with custom styling
        action_text = "🚀 BEGIN YOUR JOURNEY" if st.session_state.get('action') == 'rent' else "🎯 FIND A DOCK"
        
        st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
        if st.button(action_text, key="journey_btn", use_container_width=True):
            if address.strip():
                process_location_request(address, city, province, st.session_state.get('action', 'rent'), data)
            else:
                st.error("⚠️ Please enter your street address")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Station Guide
        st.markdown('''
        <div class="metric-card">
            <h3 style="font-family: 'Bebas Neue', Arial Black, sans-serif; font-size: 1.5rem; font-weight: 700; text-align: center; margin-bottom: 1.5rem; text-transform: uppercase;">Station Guide</h3>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("🟢 **Plenty Available** - 5 or more bikes ready")
        st.markdown("🟡 **Limited Stock** - 1-4 bikes remaining")
        st.markdown("🔴 **Empty Station** - No bikes available")
        
        st.markdown('''
        <div class="metric-card" style="background: linear-gradient(135deg, #F5F2E8 0%, #EDE9DC 100%); margin-top: 1rem;">
            <div style="text-align: center;">
                <div style="font-family: 'Bebas Neue', Arial Black, sans-serif; font-size: 1.125rem; font-weight: 700; margin-bottom: 0.5rem; text-transform: uppercase;">Did You Know</div>
                <p style="font-size: 0.875rem; line-height: 1.6; color: #6B5D4F;">
                    Toronto Bike Share has been connecting communities since 2011, making over 10 million trips across the city.
                </p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

def create_map_section(data):
    """Create the map section"""
    st.markdown('<h2 class="section-title"><span style="color: #922b0d;">EXPLORE</span> THE NETWORK</h2>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 1.25rem; color: #6B5D4F; text-align: center; line-height: 1.6; max-width: 600px; margin: 0 auto 2rem;">Every dot on this map represents a gateway to adventure - 1,000 stations connecting every corner of Toronto</p>', unsafe_allow_html=True)
    
    # Create map
    center = [43.65306613746548, -79.38815311015]
    m = folium.Map(location=center, zoom_start=12, tiles='cartodbpositron')
    
    # Add station markers
    for _, row in data.iterrows():
        marker_color = get_marker_color(row['num_bikes_available'])
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=3,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.7,
            popup=folium.Popup(
                f"<b>Station:</b> {row.get('name', row['station_id'])}<br>"
                f"<b>Total Bikes:</b> {row['num_bikes_available']}<br>"
                f"<b>E-bikes:</b> {row['ebike']}<br>"
                f"<b>Mechanical:</b> {row['mechanical']}<br>"
                f"<b>Docks:</b> {row['num_docks_available']}", 
                max_width=300
            )
        ).add_to(m)
    
    # Create styled map container with border - properly centered
    st.markdown('''
    <div style="
        display: flex; 
        justify-content: center; 
        align-items: center;
        width: 100%;
        margin: 2rem 0;
        padding: 0;
    ">
        <div style="
            border: 4px solid #2C2416;
            border-radius: 16px;
            padding: 8px;
            background: linear-gradient(45deg, #922b0d 0%, #2C2416 25%, #922b0d 50%, #2C2416 75%, #922b0d 100%);
            background-size: 20px 20px;
            box-shadow: 
                inset 0 0 0 4px #FAF7F0,
                inset 0 0 0 8px #2C2416,
                8px 8px 0 -2px #FAF7F0, 
                8px 8px 0 0 #B67C6D;
            max-width: 920px;
            width: 100%;
        ">
            <div style="
                border: 2px solid #2C2416;
                border-radius: 12px;
                overflow: hidden;
                background: white;
                width: 100%;
            ">
    ''', unsafe_allow_html=True)
    
    # Display larger centered map with proper width
    st_folium(m, width=900, height=600, returned_objects=[], use_container_width=True)
    
    # Close the styled container
    st.markdown('</div></div></div>', unsafe_allow_html=True)
    
    # Map legend
    ready_stations = len(data[data['num_bikes_available'] >= 5])
    limited_stations = len(data[(data['num_bikes_available'] >= 1) & (data['num_bikes_available'] < 5)])
    empty_stations = len(data[data['num_bikes_available'] == 0])
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**🧭 MAP LEGEND**")
    with col2:
        st.markdown(f"🟢 **{ready_stations}** Ready")
    with col3:
        st.markdown(f"🟡 **{limited_stations}** Limited")
    with col4:
        st.markdown(f"🔴 **{empty_stations}** Empty")

def create_footer():
    """Create the footer"""
    timestamp = dt.datetime.now().strftime("%I:%M:%S %p")
    
    st.markdown("---")
    
    st.markdown(f'''
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #FAF7F0 0%, #F5F2E8 100%);">
        <div style="font-family: 'Bebas Neue', Arial Black, sans-serif; font-size: 2rem; font-weight: 700; margin-bottom: 1rem; text-transform: uppercase;">
            <span style="color: #922b0d;">TORONTO</span> BIKE SHARE
        </div>
        <div style="font-size: 0.875rem; color: #6B5D4F; margin-bottom: 0.5rem;">
            A service of the City of Toronto • Operated by Bike Share Toronto
        </div>
        <p style="font-family: monospace; font-size: 0.75rem; color: #6B5D4F;">
            Data updates in real-time • Last refresh: {timestamp}
        </p>
    </div>
    ''', unsafe_allow_html=True)

def process_location_request(address, city, province, action, data):
    """Process location request and show results"""
    full_address = f"{address} {city} {province}"
    
    with st.spinner(f"🔍 Finding your {'bike' if action == 'rent' else 'dock'}..."):
        try:
            user_location = geocode(full_address)
            if not user_location:
                st.error("❌ Could not find the address. Please check and try again.")
                return
            
            if action == "rent":
                # Get selected bike type from session state
                bike_type = st.session_state.get('bike_type', 'any')
                if bike_type == 'ebike':
                    chosen_station = get_bike_availability(user_location, data, ["ebike"])
                elif bike_type == 'mechanical':
                    chosen_station = get_bike_availability(user_location, data, ["mechanical"])
                else:  # any
                    chosen_station = get_bike_availability(user_location, data, ["mechanical", "ebike"])
            else:
                chosen_station = get_dock_availability(user_location, data)
            
            if chosen_station:
                display_route_result(user_location, chosen_station, data, action)
            else:
                bike_type_text = st.session_state.get('bike_type', 'mechanical')
                if action == 'rent':
                    st.warning(f"⚠️ No {bike_type_text} {'bikes' if action == 'rent' else 'docks'} available nearby. Try selecting a different bike type.")
                else:
                    st.warning(f"⚠️ No {'bikes' if action == 'rent' else 'docks'} available nearby.")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

def display_route_result(user_location, chosen_station, data, action):
    """Display route result with map"""
    m = folium.Map(location=user_location, zoom_start=16, tiles='cartodbpositron')
    
    # Add all stations
    for _, row in data.iterrows():
        marker_color = get_marker_color(row['num_bikes_available'])
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=4,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.8,
            popup=f"Bikes: {row['num_bikes_available']}<br>E-bikes: {row['ebike']}<br>Mechanical: {row['mechanical']}<br>Docks: {row['num_docks_available']}"
        ).add_to(m)
    
    # Add user and chosen station
    folium.Marker(user_location, popup="📍 You are here", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker(
        (chosen_station[1], chosen_station[2]), 
        popup=f"{'🚲 Get bike' if action == 'rent' else '🔒 Return bike'} here",
        icon=folium.Icon(color="red")
    ).add_to(m)
    
    # Add route
    try:
        coordinates, duration = run_osrm(chosen_station, user_location)
        folium.PolyLine(coordinates, color="blue", weight=4, opacity=0.8).add_to(m)
    except:
        duration = "N/A"
    
    st.success(f"✅ Found! Walking time: **{duration}**")
    st_folium(m, width=700, height=400, returned_objects=[])

if __name__ == "__main__":
    main()

