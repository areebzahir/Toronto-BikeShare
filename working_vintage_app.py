"""
Toronto Bike Share Dashboard - Working Vintage Design
Using Streamlit components with CSS styling to avoid HTML rendering issues
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
    initial_sidebar_state="collapsed"
)

def load_vintage_css():
    """Load vintage CSS that works with Streamlit components"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue:wght@400;700&family=Crimson+Text:wght@400;600&family=Special+Elite:wght@400&display=swap');
        
        /* Hide Streamlit elements */
        .stApp > header, #MainMenu, .stDeployButton, footer, .stDecoration {display: none !important;}
        
        /* Root Variables */
        :root {
            --cream: #FAF7F0;
            --charcoal: #2C2416;
            --warm-gray: #6B5D4F;
            --rust-red: #C1492E;
            --transit-blue: #2E5C8A;
            --heritage-green: #4A7C59;
            --warm-amber: #D4A574;
            --faded-olive: #8B8661;
            --muted-terracotta: #B67C6D;
        }
        
        /* Global Styles */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        .stApp {
            background-color: var(--cream);
            font-family: 'Crimson Text', serif;
            color: var(--charcoal);
        }
        
        /* Vintage paper texture */
        body::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            opacity: 0.03;
            pointer-events: none;
            background-image: 
                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(44,36,22,0.02) 2px, rgba(44,36,22,0.02) 4px),
                repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(44,36,22,0.02) 2px, rgba(44,36,22,0.02) 4px);
            z-index: 1;
        }
        
        /* Corner decorations */
        .corner-decorations {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            pointer-events: none;
            z-index: 2;
        }
        .corner-decorations::before, .corner-decorations::after {
            content: "";
            position: absolute;
            width: 128px; height: 128px;
            border: 4px solid var(--faded-olive);
            opacity: 0.3;
        }
        .corner-decorations::before {
            top: 0; left: 0;
            border-right: none; border-bottom: none;
        }
        .corner-decorations::after {
            bottom: 0; right: 0;
            border-left: none; border-top: none;
        }
        
        /* Header styling */
        .vintage-header {
            background: linear-gradient(135deg, var(--cream) 0%, #F5F2E8 100%);
            border-bottom: 8px double var(--faded-olive);
            padding: 4rem 2rem;
            text-align: center;
            position: relative;
            margin-bottom: 0;
        }
        
        .vintage-stamp {
            position: absolute;
            top: 2rem; right: 2rem;
            width: 96px; height: 96px;
            border: 4px solid var(--rust-red);
            border-radius: 50%;
            background-color: var(--cream);
            display: flex;
            align-items: center;
            justify-content: center;
            transform: rotate(12deg);
            opacity: 0.8;
            font-family: 'Special Elite', monospace;
            color: var(--rust-red);
            font-weight: bold;
        }
        
        /* Typography classes for Streamlit components */
        .vintage-overline {
            font-size: 0.875rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.3em !important;
            color: var(--warm-gray) !important;
            text-align: center !important;
            font-weight: 600 !important;
            margin: 0 !important;
        }
        
        .vintage-title {
            font-family: 'Bebas Neue', Arial Black, sans-serif !important;
            font-size: clamp(4rem, 10vw, 8rem) !important;
            font-weight: 700 !important;
            line-height: 0.9 !important;
            text-align: center !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            margin: 1rem 0 !important;
        }
        
        .title-bike { color: var(--rust-red) !important; }
        .title-share { color: var(--transit-blue) !important; }
        
        .vintage-subtitle {
            font-size: 1.5rem !important;
            color: var(--warm-gray) !important;
            text-align: center !important;
            line-height: 1.6 !important;
            font-weight: 400 !important;
            margin: 1rem 0 !important;
        }
        
        .vintage-date {
            font-family: 'Special Elite', monospace !important;
            font-size: 0.875rem !important;
            color: var(--charcoal) !important;
            text-align: center !important;
            background-color: rgba(255,255,255,0.5) !important;
            padding: 0.75rem 1.5rem !important;
            border: 2px solid var(--charcoal) !important;
            border-radius: 8px !important;
            display: inline-block !important;
            margin: 1rem 0 !important;
        }
        
        /* Section titles */
        .section-title {
            font-family: 'Bebas Neue', Arial Black, sans-serif !important;
            font-size: clamp(2.5rem, 6vw, 4.5rem) !important;
            font-weight: 700 !important;
            text-align: center !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            margin: 2rem 0 !important;
        }
        
        /* Status intro */
        .status-badge {
            font-size: 0.75rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.2em !important;
            color: var(--transit-blue) !important;
            background-color: rgba(46,92,138,0.1) !important;
            padding: 0.5rem 1.5rem !important;
            border: 2px solid var(--transit-blue) !important;
            border-radius: 50px !important;
            display: inline-block !important;
            font-weight: 600 !important;
            text-align: center !important;
            margin-bottom: 1rem !important;
        }
        
        .status-description {
            font-size: 1.5rem !important;
            line-height: 1.6 !important;
            font-style: italic !important;
            color: var(--charcoal) !important;
            text-align: center !important;
            max-width: 600px !important;
            margin: 0 auto 2rem !important;
        }
        
        /* Cards */
        .vintage-card {
            background-color: white !important;
            border: 3px solid var(--charcoal) !important;
            border-radius: 12px !important;
            padding: 2rem !important;
            margin: 1rem 0 !important;
            position: relative !important;
            box-shadow: 
                0 8px 16px rgba(44,36,22,0.1),
                8px 8px 0 -2px var(--cream),
                8px 8px 0 0 var(--muted-terracotta) !important;
            transition: all 300ms ease !important;
        }
        
        .vintage-card:hover {
            transform: translateY(-4px) scale(1.02) !important;
            box-shadow: 
                0 12px 24px rgba(44,36,22,0.15),
                8px 8px 0 -2px var(--cream),
                8px 8px 0 0 var(--muted-terracotta) !important;
        }
        
        .hero-card {
            background: linear-gradient(135deg, var(--rust-red) 0%, #A63D28 100%) !important;
            color: white !important;
        }
        
        .success-card {
            background: linear-gradient(135deg, var(--heritage-green) 0%, #3E6B4A 100%) !important;
            color: white !important;
        }
        
        .info-card {
            background: linear-gradient(135deg, var(--transit-blue) 0%, #254A73 100%) !important;
            color: white !important;
        }
        
        .warning-card {
            background: linear-gradient(135deg, var(--warm-amber) 0%, #C19660 100%) !important;
            color: white !important;
        }
        
        .card-number {
            font-family: 'Bebas Neue', Arial Black, sans-serif !important;
            font-size: 4rem !important;
            font-weight: 700 !important;
            line-height: 0.9 !important;
            text-align: center !important;
            margin: 1rem 0 !important;
        }
        
        .card-label {
            font-size: 0.75rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.3em !important;
            text-align: center !important;
            font-weight: 600 !important;
            opacity: 0.9 !important;
        }
        
        .card-description {
            font-size: 0.875rem !important;
            text-align: center !important;
            font-weight: 600 !important;
            margin-top: 0.5rem !important;
        }
        
        /* Form styling */
        .form-title {
            font-family: 'Bebas Neue', Arial Black, sans-serif !important;
            font-size: 3rem !important;
            font-weight: 700 !important;
            text-align: center !important;
            color: var(--charcoal) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            margin-bottom: 1rem !important;
        }
        
        .form-subtitle {
            color: var(--warm-gray) !important;
            font-size: 1.125rem !important;
            text-align: center !important;
            line-height: 1.6 !important;
            margin-bottom: 2rem !important;
            padding-bottom: 2rem !important;
            border-bottom: 2px dashed var(--faded-olive) !important;
        }
        
        /* Sidebar styling */
        .sidebar-title {
            font-family: 'Bebas Neue', Arial Black, sans-serif !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            text-align: center !important;
            color: var(--charcoal) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            margin-bottom: 1.5rem !important;
        }
        
        /* Streamlit component overrides */
        .stButton > button {
            background: linear-gradient(135deg, var(--transit-blue) 0%, #254A73 100%) !important;
            color: white !important;
            border: 3px solid var(--transit-blue) !important;
            border-radius: 8px !important;
            font-family: 'Bebas Neue', Arial Black, sans-serif !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            padding: 1rem 2rem !important;
            font-size: 1.125rem !important;
            transition: all 300ms ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 16px rgba(46,92,138,0.3) !important;
        }
        
        .stSelectbox > div > div > select,
        .stTextInput > div > div > input {
            border: 2px solid var(--faded-olive) !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
            font-size: 1rem !important;
            font-family: 'Crimson Text', serif !important;
            background-color: white !important;
        }
        
        .stSelectbox > div > div > select:focus,
        .stTextInput > div > div > input:focus {
            border-color: var(--transit-blue) !important;
            box-shadow: 0 0 0 3px rgba(46,92,138,0.1) !important;
        }
        
        /* Map styling */
        .map-container {
            border-radius: 12px !important;
            overflow: hidden !important;
            border: 4px solid var(--muted-terracotta) !important;
            margin: 1rem 0 !important;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .vintage-stamp { display: none !important; }
            .vintage-title { font-size: 3rem !important; }
            .section-title { font-size: 2rem !important; }
        }
    </style>
    """, unsafe_allow_html=True)

# API URLs
STATION_STATUS_URL = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json'
STATION_INFO_URL = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"

def main():
    """Main application function"""
    
    # Load vintage CSS
    load_vintage_css()
    
    # Initialize session state
    if 'action' not in st.session_state:
        st.session_state.action = "rent"
    
    # Fetch data
    with st.spinner('Loading bike share data...'):
        try:
            data_df = query_station_status(STATION_STATUS_URL)
            latlon_df = get_station_latlon(STATION_INFO_URL)
            data = join_latlon(data_df, latlon_df)
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return
    
    # Create the app sections
    create_header()
    create_status_intro()
    create_current_status(data)
    create_find_ride_section(data)
    create_network_section(data)
    create_call_to_action()
    create_footer()

def create_header():
    """Create the vintage header using Streamlit components"""
    current_time = dt.datetime.now().strftime("%A, %B %d, %Y")
    
    # Corner decorations
    st.markdown('<div class="corner-decorations"></div>', unsafe_allow_html=True)
    
    # Header container
    st.markdown('<div class="vintage-header">', unsafe_allow_html=True)
    st.markdown('<div class="vintage-stamp"><div style="text-align: center;"><div style="font-size: 0.75rem;">EST</div><div style="font-size: 1.5rem;">2011</div></div></div>', unsafe_allow_html=True)
    
    # Use Streamlit components with CSS classes
    st.markdown('<p class="vintage-overline">━━━ City of Toronto ━━━</p>', unsafe_allow_html=True)
    
    st.markdown('<h1 class="vintage-title"><span class="title-bike">BIKE</span> <span class="title-share">SHARE</span></h1>', unsafe_allow_html=True)
    
    # Bike decorations
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align: center; font-size: 2rem; margin: 1rem 0;">🚲 ━━━━━━━━━━━━━━━━ 🚲</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="vintage-subtitle">Your Journey Across Toronto Begins Here</p>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="vintage-date">🕐 {current_time}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_status_intro():
    """Create the status introduction using Streamlit components"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="status-badge">🧭 Real-Time System Status</div>', unsafe_allow_html=True)
        st.markdown('<p class="status-description">Across the bustling streets of Toronto, thousands of bicycles await their next adventure. Where will yours take you today?</p>', unsafe_allow_html=True)

def create_current_status(data):
    """Create the current status section using Streamlit components"""
    # Calculate metrics
    total_bikes = sum(data['num_bikes_available'])
    stations_with_bikes = len(data[data['num_bikes_available'] > 0])
    stations_with_docks = len(data[data['num_docks_available'] > 0])
    total_stations = len(data)
    
    bike_availability_rate = (stations_with_bikes / total_stations) * 100
    dock_availability_rate = (stations_with_docks / total_stations) * 100
    
    # Section title
    st.markdown('<h2 class="section-title"><span style="color: var(--rust-red);">CURRENT</span> STATUS</h2>', unsafe_allow_html=True)
    
    # Hero card and E-bikes card
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="vintage-card hero-card">
            <div style="text-align: center;">
                <div class="card-label">Bikes Ready to Ride</div>
                <div class="card-number">{total_bikes:,}</div>
                <div style="background-color: rgba(255, 255, 255, 0.2); padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.875rem; font-weight: 600; display: inline-block;">System-wide Availability</div>
            </div>
            <div style="position: absolute; top: -1rem; right: -1rem; font-size: 8rem; opacity: 0.1;">🚲</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="vintage-card warning-card">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
                <div class="card-label">Electric Bikes</div>
                <div style="font-family: 'Bebas Neue', Arial Black, sans-serif; font-size: 2.5rem; font-weight: 700; margin: 1rem 0; text-transform: uppercase;">Coming Soon</div>
                <p style="font-size: 0.875rem; opacity: 0.9; font-weight: 600;">E-bikes temporarily unavailable</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats cards row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="vintage-card success-card">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📍</div>
                <div class="card-label">Stations w/ Bikes</div>
                <div class="card-number">{stations_with_bikes}</div>
                <div style="font-size: 1.5rem; opacity: 0.8; font-weight: 600;">/{total_stations}</div>
                <div class="card-description">{bike_availability_rate:.1f}% Ready</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="vintage-card info-card">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🅿️</div>
                <div class="card-label">Docking Stations</div>
                <div class="card-number">{stations_with_docks}</div>
                <div style="font-size: 1.5rem; opacity: 0.8; font-weight: 600;">/{total_stations}</div>
                <div class="card-description">{dock_availability_rate:.1f}% Available</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_find_ride_section(data):
    """Create the find your ride section using Streamlit components"""
    st.markdown('<div style="padding: 4rem 2rem; max-width: 1400px; margin: 0 auto;">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="vintage-card">
            <h3 class="form-title">Find Your Ride</h3>
            <p class="form-subtitle">Tell us where you are and we will guide you to the nearest bike</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Form content using Streamlit components
        st.markdown("**I NEED TO**")
        
        col_rent, col_return = st.columns(2)
        with col_rent:
            if st.button("🚲 Rent a Bike", key="rent", use_container_width=True):
                st.session_state.action = "rent"
        
        with col_return:
            if st.button("🅿️ Return a Bike", key="return", use_container_width=True):
                st.session_state.action = "return"
        
        st.markdown("**YOUR LOCATION**")
        address = st.text_input("Street Address", placeholder="123 Queen Street West")
        
        col_city, col_province = st.columns(2)
        with col_city:
            city = st.text_input("City", value="Toronto")
        with col_province:
            province = st.text_input("Province", value="Ontario")
        
        if st.session_state.action == "rent":
            st.markdown("**BIKE TYPE**")
            bike_type = st.selectbox("Select bike type", ["Mechanical", "E-Bike (Unavailable)"], index=0)
        
        # Action button
        action_text = "🧭 BEGIN YOUR JOURNEY" if st.session_state.action == "rent" else "🧭 FIND A DOCK"
        if st.button(action_text, type="primary", use_container_width=True):
            if address.strip():
                process_location_request(address, city, province, st.session_state.action, data)
            else:
                st.error("⚠️ Please enter your street address")
    
    with col2:
        # Station Guide using Streamlit components
        st.markdown('<div class="vintage-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="sidebar-title">Station Guide</h3>', unsafe_allow_html=True)
        
        # Legend items using simple Streamlit components
        st.markdown("🟢 **Plenty Available** - 5 or more bikes ready")
        st.markdown("🟡 **Limited Stock** - 1-4 bikes remaining")
        st.markdown("🔴 **Empty Station** - No bikes available")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Did you know section
        st.markdown("""
        <div class="vintage-card" style="background: linear-gradient(135deg, #F5F2E8 0%, #EDE9DC 100%);">
            <div style="text-align: center;">
                <div style="font-family: 'Bebas Neue', Arial Black, sans-serif; font-size: 1.125rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--charcoal); text-transform: uppercase; letter-spacing: 0.05em;">Did You Know?</div>
                <p style="font-size: 0.875rem; line-height: 1.6; color: var(--warm-gray);">
                    Toronto Bike Share has been connecting communities since 2011, making over 10 million trips across the city.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_network_section(data):
    """Create the explore the network section"""
    st.markdown('<div style="padding: 4rem 2rem; max-width: 1400px; margin: 0 auto;">', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title"><span style="color: var(--rust-red);">EXPLORE</span> THE NETWORK</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<p style="font-size: 1.25rem; color: var(--warm-gray); text-align: center; line-height: 1.6;">Every dot on this map represents a gateway to adventure - 1,000 stations connecting every corner of Toronto</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="vintage-card">', unsafe_allow_html=True)
    
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
                f"<b>Bikes:</b> {row['num_bikes_available']}<br>"
                f"<b>Docks:</b> {row['num_docks_available']}", 
                max_width=300
            )
        ).add_to(m)
    
    # Display map
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st_folium(m, width=700, height=500, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def create_call_to_action():
    """Create the call to action section"""
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, var(--cream) 0%, #F5F2E8 100%);">
        <div class="status-badge" style="margin-bottom: 2rem;">🚲 Your Adventure Awaits</div>
        <h2 style="font-family: 'Bebas Neue', Arial Black, sans-serif; font-size: clamp(3rem, 8vw, 5rem); font-weight: 700; margin-bottom: 1rem; line-height: 1.1; color: var(--charcoal); text-transform: uppercase; letter-spacing: 0.05em;">
            Every Ride Tells A Story
        </h2>
        <p style="font-size: 1.25rem; color: var(--warm-gray); max-width: 600px; margin: 0 auto 3rem; line-height: 1.6;">
            From the waterfront to the neighborhoods, Toronto is yours to discover. Hop on a bike and write your next chapter.
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_footer():
    """Create the footer"""
    timestamp = dt.datetime.now().strftime("%I:%M:%S %p")
    
    st.markdown(f"""
    <div style="border-top: 8px double var(--faded-olive); background: linear-gradient(135deg, var(--cream) 0%, #F5F2E8 100%); padding: 3rem 2rem; text-align: center;">
        <div style="font-family: 'Bebas Neue', Arial Black, sans-serif; font-size: 2rem; font-weight: 700; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">
            <span style="color: var(--rust-red);">TORONTO</span> BIKE SHARE
        </div>
        <div style="display: flex; align-items: center; justify-content: center; gap: 0.75rem; font-size: 0.875rem; color: var(--warm-gray); margin-bottom: 0.5rem; flex-wrap: wrap;">
            <span>A service of the City of Toronto</span>
            <span>•</span>
            <span>Operated by Bike Share Toronto</span>
        </div>
        <p style="font-family: 'Special Elite', monospace; font-size: 0.75rem; color: var(--warm-gray);">
            Data updates in real-time • Last refresh: {timestamp}
        </p>
    </div>
    """, unsafe_allow_html=True)

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
                chosen_station = get_bike_availability(user_location, data, ["mechanical"])
            else:
                chosen_station = get_dock_availability(user_location, data)
            
            if chosen_station:
                display_route_result(user_location, chosen_station, data, action)
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
            popup=f"Bikes: {row['num_bikes_available']}<br>Docks: {row['num_docks_available']}"
        ).add_to(m)
    
    # Add user and chosen station
    folium.Marker(user_location, popup="📍 You are here", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker(
        (chosen_station[1], chosen_station[2]), 
        popup=f"{'🚲 Get bike' if action == 'rent' else '🅿️ Return bike'} here",
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