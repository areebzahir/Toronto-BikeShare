"""
Toronto Bike Share Dashboard - Vintage Transit Poster Design
A nostalgic 1950s-60s transit authority poster that evokes urban exploration
"""

import streamlit as st
import requests
import pandas as pd
import datetime as dt
import folium
from streamlit_folium import st_folium
from helper import *
import time
import pytz

# Configure Streamlit page
st.set_page_config(
    page_title="Toronto Bike Share | Transit Authority",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentic vintage transit poster CSS
st.markdown("""
<style>
    /* Import authentic vintage fonts */
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue:wght@400&family=Crimson+Text:wght@400;600&family=Special+Elite&display=swap');
    
    /* Hide Streamlit elements */
    .stApp > header, #MainMenu, .stDeployButton, footer, .stDecoration {display: none !important;}
    
    /* Global vintage poster styling */
    .stApp {
        background: #FAF7F0;
        font-family: 'Crimson Text', serif;
        color: #2C2416;
        line-height: 1.6;
    }
    
    .main .block-container {
        padding: 3rem 2rem !important;
        max-width: 1200px !important;
    }
    
    /* Vintage poster header */
    .poster-header {
        text-align: center;
        margin: 0 0 4rem 0;
        padding: 3rem 2rem;
        background: #FAF7F0;
        border: 6px double #2C2416;
        position: relative;
        clip-path: polygon(0% 0%, 98% 0%, 100% 2%, 100% 100%, 2% 100%, 0% 98%);
    }
    
    .poster-header::before {
        content: '';
        position: absolute;
        top: 12px;
        left: 12px;
        right: 12px;
        bottom: 12px;
        border: 2px solid #2E5C8A;
        opacity: 0.3;
    }
    
    .poster-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 4rem;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #2E5C8A;
        margin: 0 0 1rem 0;
        text-shadow: 3px 3px 0 rgba(44, 36, 22, 0.1);
    }
    
    .poster-subtitle {
        font-family: 'Crimson Text', serif;
        font-size: 1.5rem;
        font-style: italic;
        color: #2C2416;
        margin: 0 0 1rem 0;
    }
    
    .poster-meta {
        font-family: 'Special Elite', monospace;
        font-size: 0.9rem;
        color: #4A7C59;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    /* Torn paper cards */
    .paper-card {
        background: #FAF7F0;
        border: 3px solid #4A7C59;
        margin: 2rem 0;
        padding: 2rem;
        position: relative;
        box-shadow: 
            4px 4px 0 rgba(44, 36, 22, 0.1),
            8px 8px 0 rgba(44, 36, 22, 0.05),
            12px 12px 20px rgba(44, 36, 22, 0.15);
        clip-path: polygon(0% 2px, 2px 0%, calc(100% - 2px) 0%, 100% 2px, 100% calc(100% - 2px), calc(100% - 2px) 100%, 2px 100%, 0% calc(100% - 2px));
        transition: all 300ms ease;
    }
    
    .paper-card:hover {
        transform: translateY(-4px);
        box-shadow: 
            6px 6px 0 rgba(44, 36, 22, 0.1),
            12px 12px 0 rgba(44, 36, 22, 0.05),
            18px 18px 30px rgba(44, 36, 22, 0.2);
    }
    
    /* Decorative corners */
    .paper-card::before {
        content: '';
        position: absolute;
        top: 8px;
        left: 8px;
        width: 8px;
        height: 8px;
        background: #4A7C59;
        opacity: 0.6;
    }
    
    .paper-card::after {
        content: '';
        position: absolute;
        bottom: 8px;
        right: 8px;
        width: 8px;
        height: 8px;
        background: #4A7C59;
        opacity: 0.6;
    }
    
    /* Status-specific card colors */
    .card-primary {
        border-color: #2E5C8A;
    }
    
    .card-primary::before,
    .card-primary::after {
        background: #2E5C8A;
    }
    
    .card-success {
        border-color: #4A7C59;
    }
    
    .card-warning {
        border-color: #D4A574;
    }
    
    .card-warning::before,
    .card-warning::after {
        background: #D4A574;
    }
    
    .card-alert {
        border-color: #C1492E;
    }
    
    .card-alert::before,
    .card-alert::after {
        background: #C1492E;
    }
    
    /* Hero numbers */
    .hero-number {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 4rem;
        font-weight: 400;
        color: #2E5C8A;
        text-align: center;
        margin: 1rem 0;
        text-shadow: 2px 2px 0 rgba(44, 36, 22, 0.1);
    }
    
    .hero-label {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        text-align: center;
        color: #2C2416;
        margin-bottom: 0.5rem;
    }
    
    .hero-context {
        font-family: 'Crimson Text', serif;
        font-size: 1rem;
        text-align: center;
        color: #2C2416;
        font-style: italic;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.5rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #2E5C8A;
        text-align: center;
        margin: 3rem 0 2rem 0;
        position: relative;
    }
    
    .section-header::before,
    .section-header::after {
        content: '◆';
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        color: #4A7C59;
        font-size: 1rem;
    }
    
    .section-header::before {
        left: -3rem;
    }
    
    .section-header::after {
        right: -3rem;
    }
    
    /* Narrative text */
    .story-text {
        font-family: 'Crimson Text', serif;
        font-size: 1.2rem;
        line-height: 1.8;
        color: #2C2416;
        text-align: center;
        max-width: 600px;
        margin: 0 auto 2rem auto;
        font-style: italic;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0.25rem;
        border: 2px solid;
    }
    
    .badge-available {
        background: #4A7C59;
        color: #FAF7F0;
        border-color: #4A7C59;
    }
    
    .badge-limited {
        background: #D4A574;
        color: #2C2416;
        border-color: #D4A574;
    }
    
    .badge-critical {
        background: #C1492E;
        color: #FAF7F0;
        border-color: #C1492E;
    }
    
    /* Heritage frame for map */
    .heritage-frame {
        border: 8px double #2C2416;
        padding: 1rem;
        background: #FAF7F0;
        margin: 2rem 0;
        position: relative;
    }
    
    .heritage-frame::before {
        content: '';
        position: absolute;
        top: 12px;
        left: 12px;
        right: 12px;
        bottom: 12px;
        border: 2px dashed #2E5C8A;
        opacity: 0.4;
    }
    
    /* Vintage buttons */
    .stButton > button {
        background: #2E5C8A !important;
        color: #FAF7F0 !important;
        border: 3px solid #2C2416 !important;
        border-radius: 0 !important;
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        padding: 1rem 2rem !important;
        width: 100% !important;
        box-shadow: 4px 4px 0 rgba(44, 36, 22, 0.2) !important;
        transition: all 300ms ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 6px 6px 0 rgba(44, 36, 22, 0.2) !important;
        background: #4A7C59 !important;
    }
    
    /* Form elements */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: #FAF7F0 !important;
        border: 2px solid #2C2416 !important;
        border-radius: 0 !important;
        font-family: 'Crimson Text', serif !important;
        font-size: 1rem !important;
        padding: 0.75rem !important;
        color: #2C2416 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #2E5C8A !important;
        box-shadow: 0 0 0 3px rgba(46, 92, 138, 0.2) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #FAF7F0;
        border-right: 4px solid #2E5C8A;
    }
    
    /* Sidebar content styling */
    .css-1d391kg .stButton > button {
        background: #2E5C8A !important;
        color: #FAF7F0 !important;
        border: 2px solid #2C2416 !important;
        border-radius: 8px !important;
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 0.75rem 1rem !important;
        width: 100% !important;
        box-shadow: 2px 2px 0 rgba(44, 36, 22, 0.2) !important;
        transition: all 300ms ease !important;
    }
    
    .css-1d391kg .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 3px 3px 0 rgba(44, 36, 22, 0.2) !important;
        background: #4A7C59 !important;
    }
    
    /* Sidebar radio buttons */
    .css-1d391kg .stRadio > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid #D4A574 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
    }
    
    .css-1d391kg .stRadio label {
        color: #2C2416 !important;
        font-family: 'Crimson Text', serif !important;
        font-size: 0.9rem !important;
    }
    
    .css-1d391kg .stRadio input[type="radio"]:checked + div {
        background-color: #2E5C8A !important;
    }
    
    /* Sidebar text inputs */
    .css-1d391kg .stTextInput > div > div > input {
        background: #FFFFFF !important;
        border: 2px solid #2C2416 !important;
        border-radius: 8px !important;
        font-family: 'Crimson Text', serif !important;
        font-size: 0.9rem !important;
        padding: 0.75rem !important;
        color: #2C2416 !important;
    }
    
    .css-1d391kg .stTextInput > div > div > input::placeholder {
        color: #6B5D4F !important;
        opacity: 0.7 !important;
    }
    
    .css-1d391kg .stTextInput > div > div > input:focus {
        border-color: #2E5C8A !important;
        box-shadow: 0 0 0 2px rgba(46, 92, 138, 0.2) !important;
        color: #2C2416 !important;
    }
    
    /* Disabled text inputs (for Toronto/Ontario) - Multiple selectors to override Streamlit defaults */
    .css-1d391kg .stTextInput > div > div > input:disabled,
    .css-1d391kg .stTextInput input:disabled,
    .css-1d391kg input[disabled],
    .stApp input[disabled],
    .stTextInput input[disabled] {
        background: #F5F2E8 !important;
        color: #000000 !important;
        opacity: 1 !important;
        font-weight: 700 !important;
        border: 2px solid #D4A574 !important;
        text-shadow: none !important;
        -webkit-text-fill-color: #000000 !important;
        -webkit-opacity: 1 !important;
    }
    
    /* Force black text on disabled inputs with highest specificity */
    .stApp .css-1d391kg .stTextInput > div > div > input[disabled] {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-family: 'Special Elite', monospace;
        font-size: 0.8rem;
        color: #4A7C59;
        text-align: center;
        letter-spacing: 0.05em;
        margin: 1rem 0;
    }
    
    /* Asymmetrical layout helpers */
    .offset-left {
        margin-left: 2rem;
    }
    
    .offset-right {
        margin-right: 2rem;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .poster-title {
            font-size: 2.5rem;
        }
        
        .hero-number {
            font-size: 2.5rem;
        }
        
        .section-header {
            font-size: 1.8rem;
        }
        
        .section-header::before,
        .section-header::after {
            display: none;
        }
        
        .offset-left,
        .offset-right {
            margin-left: 0;
            margin-right: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# API URLs
STATION_STATUS_URL = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json'
STATION_INFO_URL = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"

def get_toronto_time():
    """Get current Toronto time with proper timezone handling"""
    # Always start with UTC time to ensure consistency across servers
    utc_now = dt.datetime.now(pytz.UTC)
    # Convert to Toronto timezone (handles EST/EDT automatically)
    toronto_tz = pytz.timezone('America/Toronto')
    toronto_time = utc_now.astimezone(toronto_tz)
    return toronto_time

def format_toronto_time(toronto_time, format_string="%I:%M:%S %p"):
    """Format Toronto time with proper timezone label"""
    # Determine if it's EST or EDT
    timezone_name = "EST" if toronto_time.dst() == dt.timedelta(0) else "EDT"
    formatted_time = toronto_time.strftime(format_string)
    return f"{formatted_time} {timezone_name}"

def create_poster_header():
    """Create authentic vintage transit poster header with live time"""
    # Use the centralized Toronto time function
    toronto_time = get_toronto_time()
    current_date = toronto_time.strftime("%A, %B %d, %Y")
    
    st.markdown(f'''
    <div class="poster-header">
        <div class="poster-title">Toronto Bike Share</div>
        <div class="poster-subtitle">Your Gateway to Urban Adventure</div>
        <div class="poster-meta">Bike Share Dashboard Project • {current_date}</div>
    </div>
    ''', unsafe_allow_html=True)
        <div class="poster-subtitle">Your Gateway to Urban Adventure</div>
        <div class="poster-meta">Bike Share Dashboard Project • {current_time}</div>
    </div>
    ''', unsafe_allow_html=True)

def create_story_introduction():
    """Create narrative introduction"""
    st.markdown('''
    <div class="story-text">
        In the heart of Toronto, where streetcars once ruled and cyclists now roam, 
        a network of bicycles awaits to carry you through the urban tapestry. 
        Each station tells a story, each ride writes a new chapter in your city adventure.
    </div>
    ''', unsafe_allow_html=True)

def create_hero_metrics(data):
    """Create hero metric cards with asymmetrical layout"""
    
    # Calculate metrics
    total_bikes = data['num_bikes_available'].sum()
    total_ebikes = data['ebike'].sum()
    stations_with_bikes = len(data[data['num_bikes_available'] > 0])
    stations_with_docks = len(data[data['num_docks_available'] > 0])
    total_stations = len(data)
    
    st.markdown('<div class="section-header">Current Fleet Status</div>', unsafe_allow_html=True)
    
    # Asymmetrical layout - offset alternating cards
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f'''
        <div class="paper-card card-primary">
            <div class="hero-label">Bicycles Ready for Adventure</div>
            <div class="hero-number">{total_bikes:,}</div>
            <div class="hero-context">Across Toronto's cycling network</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        availability_rate = (stations_with_bikes / total_stations) * 100
        st.markdown(f'''
        <div class="paper-card card-success offset-right">
            <div class="hero-label">Active Stations</div>
            <div class="hero-number">{stations_with_bikes}</div>
            <div class="hero-context">{availability_rate:.0f}% of stations have bikes available</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Second row with different offset
    col3, col4 = st.columns([1, 1])
    
    with col3:
        stations_with_ebikes = len(data[data['ebike'] > 0])
        st.markdown(f'''
        <div class="paper-card card-warning offset-left">
            <div class="hero-label">Electric Bicycles</div>
            <div class="hero-number">{total_ebikes}</div>
            <div class="hero-context">Available at {stations_with_ebikes} stations citywide</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        dock_rate = (stations_with_docks / total_stations) * 100
        st.markdown(f'''
        <div class="paper-card card-alert">
            <div class="hero-label">Docking Facilities</div>
            <div class="hero-number">{stations_with_docks}</div>
            <div class="hero-context">{dock_rate:.0f}% capacity for bicycle returns</div>
        </div>
        ''', unsafe_allow_html=True)

def create_sidebar_journey_finder(data):
    """Create narrative-driven journey finder in sidebar"""
    
    # Initialize session state
    if 'action' not in st.session_state:
        st.session_state.action = "rent"
    
    # Sidebar header with vintage styling
    st.sidebar.markdown('''
    <div style="
        background: linear-gradient(135deg, #2E5C8A 0%, #254A73 100%);
        color: #FAF7F0;
        padding: 2rem 1rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        border-radius: 0 0 15px 15px;
        border: 3px solid #2C2416;
        box-shadow: 4px 4px 0 rgba(44, 36, 22, 0.2);
    ">
        <h2 style="
            font-family: 'Bebas Neue', sans-serif; 
            font-size: 2rem; 
            margin: 0 0 0.5rem 0; 
            text-transform: uppercase;
            text-shadow: 2px 2px 0 rgba(0,0,0,0.3);
            letter-spacing: 0.1em;
        ">Begin Your Journey</h2>
        <p style="margin: 0; font-size: 1rem; opacity: 0.9; font-family: 'Crimson Text', serif; font-style: italic;">
            Every adventure starts with a single pedal stroke
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Action selection with vintage buttons
    st.sidebar.markdown('<div style="font-family: \'Bebas Neue\', sans-serif; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 0.1em; color: #2C2416; margin-bottom: 1rem;">Type of Adventure</div>', unsafe_allow_html=True)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🚲 Rent", key="rent_btn", use_container_width=True):
            st.session_state.action = "rent"
    
    with col2:
        if st.button("🔒 Return", key="return_btn", use_container_width=True):
            st.session_state.action = "return"
    
    # Show current selection with vintage styling
    current_action = st.session_state.get('action', 'rent')
    if current_action == 'rent':
        st.sidebar.markdown('<div style="background: #4A7C59; color: #FAF7F0; padding: 0.75rem; border-radius: 8px; text-align: center; font-family: \'Bebas Neue\', sans-serif; text-transform: uppercase; letter-spacing: 0.05em; margin: 1rem 0;">🚲 Renting a Bicycle</div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<div style="background: #2E5C8A; color: #FAF7F0; padding: 0.75rem; border-radius: 8px; text-align: center; font-family: \'Bebas Neue\', sans-serif; text-transform: uppercase; letter-spacing: 0.05em; margin: 1rem 0;">🔒 Returning a Bicycle</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Location input with vintage styling
    st.sidebar.markdown('<div style="font-family: \'Bebas Neue\', sans-serif; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 0.1em; color: #2C2416; margin-bottom: 1rem;">Your Starting Location</div>', unsafe_allow_html=True)
    
    # Address input
    address = st.sidebar.text_input(
        "Street Address", 
        placeholder="123 Queen Street West, Toronto",
        help="Enter your street address in Toronto",
        label_visibility="collapsed"
    )
    
    # City and Province (auto-filled with vintage styling)
    col1, col2 = st.sidebar.columns(2)
    with col1:
        city = st.sidebar.text_input("City", value="Toronto", disabled=True, label_visibility="collapsed")
    with col2:
        province = st.sidebar.text_input("Province", value="Ontario", disabled=True, label_visibility="collapsed")
    
    # Bike type selection (only for rent)
    if current_action == 'rent':
        st.sidebar.markdown("---")
        st.sidebar.markdown('<div style="font-family: \'Bebas Neue\', sans-serif; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 0.1em; color: #2C2416; margin-bottom: 1rem;">Bicycle Preference</div>', unsafe_allow_html=True)
        
        bike_type = st.sidebar.radio(
            "Choose bike type:",
            ["Any Available Bicycle", "Traditional Mechanical", "Electric Powered"],
            key="bike_type_radio",
            label_visibility="collapsed"
        )
        
        # Map radio selection to session state
        if bike_type == "Electric Powered":
            st.session_state.bike_type = "ebike"
        elif bike_type == "Traditional Mechanical":
            st.session_state.bike_type = "mechanical"
        else:
            st.session_state.bike_type = "any"
    
    st.sidebar.markdown("---")
    
    # Current time display (using centralized Toronto time function)
    toronto_time = get_toronto_time()
    timezone_name = "EST" if toronto_time.dst() == dt.timedelta(0) else "EDT"
    current_time = toronto_time.strftime("%I:%M %p")
    current_date = toronto_time.strftime("%B %d, %Y")
    
    st.sidebar.markdown(f'''
    <div style="
        background: #FAF7F0; 
        border: 2px dashed #2E5C8A; 
        padding: 1rem; 
        text-align: center; 
        margin: 1rem 0;
        font-family: 'Special Elite', monospace;
        color: #2C2416;
    ">
        <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">Current Time ({timezone_name})</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{current_time}</div>
        <div style="font-size: 0.7rem; opacity: 0.7;">{current_date}</div>
        <div style="font-size: 0.6rem; opacity: 0.6; margin-top: 0.5rem;">Live Transit Data</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Action button with vintage styling
    action_text = "🗺️ Chart My Course" if current_action == 'rent' else "🎯 Find My Dock"
    
    if st.sidebar.button(action_text, key="journey_btn", use_container_width=True, type="primary"):
        if address.strip():
            with st.spinner(f'🔍 Plotting your urban adventure...'):
                process_location_request(address, city, province, current_action, data)
        else:
            st.sidebar.error("📍 Please provide your starting location")
    
    # Vintage help section
    st.sidebar.markdown("---")
    st.sidebar.markdown('''
    <div style="
        background: #F5F2E8; 
        border: 2px solid #D4A574; 
        padding: 1.5rem; 
        border-radius: 8px;
        font-family: 'Crimson Text', serif;
    ">
        <div style="font-family: 'Bebas Neue', sans-serif; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.1em; color: #2C2416; margin-bottom: 1rem; text-align: center;">Journey Tips</div>
        <div style="font-size: 0.9rem; line-height: 1.6; color: #2C2416;">
            <p style="margin: 0.5rem 0;">📍 <strong>Popular Areas:</strong> Entertainment District, Harbourfront</p>
            <p style="margin: 0.5rem 0;">⚡ <strong>E-bikes:</strong> Limited in winter months</p>
            <p style="margin: 0.5rem 0;">🗺️ <strong>Check Map:</strong> Real-time availability below</p>
            <p style="margin: 0.5rem 0;">🔒 <strong>Returns:</strong> Ensure dock availability</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def process_location_request(address, city, province, action, data):
    """Process location request and show results"""
    full_address = f"{address} {city} {province}"
    
    with st.spinner(f"🔍 Finding your {'bike' if action == 'rent' else 'dock'}..."):
        try:
            user_location = geocode(full_address)
            if not user_location:
                st.sidebar.error("❌ Could not find the address. Please check and try again.")
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
                    st.sidebar.warning(f"⚠️ No {bike_type_text} {'bikes' if action == 'rent' else 'docks'} available nearby. Try selecting a different bike type.")
                else:
                    st.sidebar.warning(f"⚠️ No {'bikes' if action == 'rent' else 'docks'} available nearby.")
                
        except Exception as e:
            st.sidebar.error(f"❌ Error: {str(e)}")

def display_route_result(user_location, chosen_station, data, action):
    """Display route result with map in main area"""
    
    # Show success message in sidebar
    st.sidebar.success(f"✅ Perfect! Route plotted successfully.")
    
    # Display detailed results in main area
    st.markdown('<div class="section-header">Your Urban Adventure Route</div>', unsafe_allow_html=True)
    
    # Get station details
    station_row = data[data['station_id'] == chosen_station[0]].iloc[0]
    station_name = station_row.get('name', f"Station {chosen_station[0]}")
    
    # Calculate route
    try:
        coordinates, duration = run_osrm(chosen_station, user_location)
    except:
        duration = "N/A"
    
    # Route summary card
    st.markdown(f'''
    <div class="paper-card card-success">
        <div class="hero-label">Journey Summary</div>
        <div style="font-family: 'Crimson Text', serif; font-size: 1.2rem; line-height: 1.8; margin: 1rem 0;">
            <strong>Destination:</strong> {station_name}<br>
            <strong>Walking Time:</strong> {duration}<br>
            <strong>Action:</strong> {'Rent your bicycle' if action == 'rent' else 'Return your bicycle'}
        </div>
        <div style="font-family: 'Bebas Neue', sans-serif; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.1em; color: #4A7C59;">
            {'🚲 Bikes Available: ' + str(station_row['num_bikes_available']) if action == 'rent' else '🔒 Docks Available: ' + str(station_row['num_docks_available'])}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Create route map
    m = folium.Map(location=user_location, zoom_start=16, tiles='cartodbpositron')
    
    # Add all stations with vintage styling
    for _, row in data.iterrows():
        marker_color = get_marker_color(row['num_bikes_available'])
        
        # Vintage-styled popup
        popup_html = f"""
        <div style="font-family: 'Crimson Text', serif; min-width: 200px; background: #FAF7F0; padding: 12px; border: 2px solid #2C2416;">
            <h4 style="font-family: 'Bebas Neue', sans-serif; margin: 0 0 8px 0; color: #2E5C8A; text-transform: uppercase;">{row.get('name', row['station_id'])}</h4>
            <div style="border-bottom: 1px solid #2C2416; margin: 8px 0;"></div>
            <p style="margin: 4px 0; font-size: 0.9rem;"><strong>Total Bicycles:</strong> {row['num_bikes_available']}</p>
            <p style="margin: 4px 0; font-size: 0.9rem;"><strong>Electric:</strong> {row['ebike']}</p>
            <p style="margin: 4px 0; font-size: 0.9rem;"><strong>Traditional:</strong> {row['mechanical']}</p>
            <p style="margin: 4px 0; font-size: 0.9rem;"><strong>Docking Space:</strong> {row['num_docks_available']}</p>
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
    
    # Add user location and destination
    folium.Marker(
        user_location, 
        popup="📍 Your Starting Point", 
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)
    
    folium.Marker(
        (chosen_station[1], chosen_station[2]), 
        popup=f"{'🚲 Get Your Bike Here' if action == 'rent' else '🔒 Return Your Bike Here'}",
        icon=folium.Icon(color="red", icon="bicycle")
    ).add_to(m)
    
    # Add route line
    if coordinates:
        folium.PolyLine(
            coordinates, 
            color="#2E5C8A", 
            weight=4, 
            opacity=0.8,
            dash_array="10,5"
        ).add_to(m)
    
    # Display in heritage frame
    st.markdown('<div class="heritage-frame">', unsafe_allow_html=True)
    st_folium(m, width=None, height=500, returned_objects=[], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def create_network_map(data):
    """Create heritage-framed network map"""
    
    st.markdown('<div class="section-header">The Great Toronto Cycling Network</div>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="story-text">
        Behold the intricate web of Toronto's bicycle infrastructure—a living map 
        where each dot represents possibility, each station a doorway to discovery.
    </div>
    ''', unsafe_allow_html=True)
    
    # Create map
    center = [43.65306613746548, -79.38815311015]
    m = folium.Map(location=center, zoom_start=12, tiles='cartodbpositron')
    
    # Add station markers
    for _, row in data.iterrows():
        marker_color = get_marker_color(row['num_bikes_available'])
        
        # Vintage-styled popup
        popup_html = f"""
        <div style="font-family: 'Crimson Text', serif; min-width: 200px; background: #FAF7F0; padding: 12px; border: 2px solid #2C2416;">
            <h4 style="font-family: 'Bebas Neue', sans-serif; margin: 0 0 8px 0; color: #2E5C8A; text-transform: uppercase;">{row.get('name', row['station_id'])}</h4>
            <div style="border-bottom: 1px solid #2C2416; margin: 8px 0;"></div>
            <p style="margin: 4px 0; font-size: 0.9rem;"><strong>Total Bicycles:</strong> {row['num_bikes_available']}</p>
            <p style="margin: 4px 0; font-size: 0.9rem;"><strong>Electric:</strong> {row['ebike']}</p>
            <p style="margin: 4px 0; font-size: 0.9rem;"><strong>Traditional:</strong> {row['mechanical']}</p>
            <p style="margin: 4px 0; font-size: 0.9rem;"><strong>Docking Space:</strong> {row['num_docks_available']}</p>
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
    
    # Display in heritage frame
    st.markdown('<div class="heritage-frame">', unsafe_allow_html=True)
    st_folium(m, width=None, height=500, returned_objects=[], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Legend with status badges
    st.markdown("### Network Status Legend")
    
    col1, col2, col3 = st.columns(3)
    
    ready_stations = len(data[data['num_bikes_available'] >= 5])
    limited_stations = len(data[(data['num_bikes_available'] >= 1) & (data['num_bikes_available'] < 5)])
    empty_stations = len(data[data['num_bikes_available'] == 0])
    
    with col1:
        st.markdown(f'<div class="status-badge badge-available">Abundant Supply</div>', unsafe_allow_html=True)
        st.markdown(f"**{ready_stations} stations** with 5+ bicycles ready")
    
    with col2:
        st.markdown(f'<div class="status-badge badge-limited">Limited Stock</div>', unsafe_allow_html=True)
        st.markdown(f"**{limited_stations} stations** with 1-4 bicycles remaining")
    
    with col3:
        st.markdown(f'<div class="status-badge badge-critical">Awaiting Resupply</div>', unsafe_allow_html=True)
        st.markdown(f"**{empty_stations} stations** currently without bicycles")

def create_footer():
    """Create vintage transit authority footer with live time"""
    
    # Use the centralized Toronto time function
    toronto_time = get_toronto_time()
    current_time = format_toronto_time(toronto_time)
    
    st.markdown("---")
    
    st.markdown(f'''
    <div class="paper-card card-primary" style="text-align: center; margin-top: 3rem;">
        <div class="hero-label">Toronto Bike Share Dashboard</div>
        <div style="font-family: 'Crimson Text', serif; font-size: 1.2rem; line-height: 1.8; color: #2C2416; text-align: center; max-width: 600px; margin: 1rem auto; font-style: italic;">
            Connecting communities through sustainable transportation. 
            Every journey matters, every ride builds a better city.
        </div>
        <div class="timestamp">
            Live data updated at {current_time}
        </div>
    </div>
    ''', unsafe_allow_html=True)

def main():
    """Main application with narrative flow"""
    
    # Add auto-refresh functionality
    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()
    
    # Auto-refresh every 30 seconds
    current_time = time.time()
    if current_time - st.session_state.last_update > 30:
        st.session_state.last_update = current_time
        st.rerun()
    
    # Create poster header
    create_poster_header()
    
    # Fetch data with vintage loading message
    with st.spinner('Consulting the great transit archives...'):
        try:
            data_df = query_station_status(STATION_STATUS_URL)
            latlon_df = get_station_latlon(STATION_INFO_URL)
            data = join_latlon(data_df, latlon_df)
        except Exception as e:
            st.error(f"The transit telegraph reports: {str(e)}")
            return
    
    # Story introduction
    create_story_introduction()
    
    # Hero metrics with asymmetrical layout
    create_hero_metrics(data)
    
    # Sidebar journey finder (replaces the main content journey finder)
    create_sidebar_journey_finder(data)
    
    # Network map
    create_network_map(data)
    
    # Footer
    create_footer()
    
    # Add refresh button and auto-refresh timer
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Refresh Data", key="refresh_btn", use_container_width=True):
            st.session_state.last_update = time.time()
            st.rerun()
    
    # Show last update time in Eastern timezone (proper UTC conversion)
    utc_timestamp = dt.datetime.fromtimestamp(st.session_state.last_update, tz=pytz.UTC)
    eastern = pytz.timezone('America/Toronto')
    eastern_time = utc_timestamp.astimezone(eastern)
    
    # Determine if it's EST or EDT
    timezone_name = "EST" if eastern_time.dst() == dt.timedelta(0) else "EDT"
    last_update_time = eastern_time.strftime(f"%I:%M:%S %p {timezone_name}")
    
    st.markdown(f'<div style="text-align: center; font-family: \'Special Elite\', monospace; font-size: 0.8rem; color: #6B5D4F; margin-top: 1rem;">Last updated: {last_update_time} • Auto-refresh in {30 - int(current_time - st.session_state.last_update)} seconds</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()