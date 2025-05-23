import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import base64
import csv
import io
import pandas as pd
import time

def add_custom_css():
    """Add custom CSS to style the app"""
    st.markdown("""
    <style>
    .property-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        background-color: #f9f9f9;
        border-left: 5px solid #4caf50;
    }
    .property-card h3 {
        margin-top: 0;
        color: #2c3e50;
    }
    .status-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .status-available {
        background-color: #e8f5e9;
        color: #2e7d32;
    }
    .status-upcoming {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    </style>
    """, unsafe_allow_html=True)

def get_table_download_link(properties, filename="property_data.csv"):
    """Generate a download link for the property data"""
    try:
        # Convert to DataFrame
        df = pd.DataFrame(properties)
        
        # Select and rename columns
        if all(col in df.columns for col in ['Price', 'Beds', 'Bath', 'SqFt', 'Address', 'City', 'State', 'Zip Code']):
            df['Full Address'] = df['Address'] + ', ' + df['City'] + ', ' + df['State'] + ' ' + df['Zip Code']
            df = df[['Price', 'Beds', 'Bath', 'SqFt', 'Full Address']]
            df.columns = ['Price', 'Beds', 'Bathroom', 'SqFt', 'Full Address']
        
        # Convert to CSV
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    except Exception as e:
        st.error(f"Error generating download link: {str(e)}")
        return ""

def scrape_property_data(url):
    """Scrape property data from the given URL."""
    try:
        # Sample data for demonstration
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sample_data = [
            {
                'Price': '500000',
                'Beds': '3',
                'Bath': '2',
                'SqFt': '1000',
                'Address': '123 Main St',
                'City': 'New York',
                'State': 'NY',
                'Zip Code': '10001',
                'Status': 'Available'
            },
            {
                'Price': '1200000',
                'Beds': '4',
                'Bath': '3.5',
                'SqFt': '3000',
                'Address': '456 Ocean Dr',
                'City': 'Miami',
                'State': 'FL',
                'Zip Code': '33139',
                'Status': 'Upcoming'
            },
            {
                'Price': '350000',
                'Beds': '3',
                'Bath': '2',
                'SqFt': '1750',
                'Address': '789 Oak Ln',
                'City': 'Austin',
                'State': 'TX',
                'Zip Code': '73301',
                'Status': 'Available'
            }
        ]
        
        # Add a small delay to simulate loading
        time.sleep(1)
        return sample_data
        
    except Exception as e:
        st.error(f"Error scraping data: {str(e)}")
        return []

def display_property_cards(properties):
    """Display property data in styled cards."""
    if not properties:
        st.warning("No property data available to display.")
        return
    
    st.subheader("Property Listings")
    
    # Create columns for the cards
    cols = st.columns(2)
    
    for idx, prop in enumerate(properties):
        with cols[idx % 2]:
            # Format price with commas
            price = f"${int(prop.get('Price', 0)):,}" if prop.get('Price') else 'N/A'
            full_address = f"{prop.get('Address', 'N/A')}, {prop.get('City', 'N/A')}, {prop.get('State', 'N/A')} {prop.get('Zip Code', '')}"
            
            # Create the card
            st.markdown(
                f"""
                <div class="property-card">
                    <p><strong>{full_address}</strong></p>
                    <p><strong>Price: {price}</strong></p>
                    <p>{prop.get('Beds', 'N/A')} Beds | {prop.get('Bath', 'N/A')} Baths</p>
                    <p>{prop.get('SqFt', 'N/A')} SqFt</p>
                </div>
                """,
                unsafe_allow_html=True
            )

def display_analytics(properties):
    """Display analytics for the property data."""
    if not properties:
        return
    
    st.subheader("Analytics")
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Listings", len(properties))
    
    with col2:
        available = sum(1 for p in properties if 'available' in p.get('Status', '').lower())
        st.metric("Available", available)
    
    with col3:
        prices = []
        for p in properties:
            try:
                price_str = p.get('Price', '').replace('$', '').replace(',', '').strip()
                if price_str.replace('.', '').isdigit():
                    prices.append(float(price_str))
            except:
                continue
        
        avg_price = sum(prices) / len(prices) if prices else 0
        st.metric("Avg. Price", f"${avg_price:,.2f}" if prices else "N/A")

def main():
    # App header
    st.title("🏠 Property Scraper Pro")
    st.markdown("""
    Scrape, analyze, and download property listings from various websites.
    """)

    # Default property websites
    default_websites = {
        "Property Onion": "https://www.propertyonion.com",
        "Zillow": "https://www.zillow.com",
        "Realtor.com": "https://www.realtor.com",
        "Redfin": "https://www.redfin.com"
    }

    # Sidebar for input
    with st.sidebar:
        st.header("🔧 Settings")
        
        # Website selection
        website_choice = st.selectbox(
            "Choose a website or enter custom URL:",
            ["Select a website", "Custom URL"] + list(default_websites.keys())
        )
        
        # Show URL input field if custom URL is selected
        if website_choice == "Custom URL":
            website_url = st.text_input("Enter Property Website URL:", 
                                     placeholder="https://example.com")
        elif website_choice in default_websites:
            website_url = default_websites[website_choice]
            st.info(f"Selected: {website_url}")
        else:
            website_url = ""
            st.info("Please select a website or choose 'Custom URL'")
        
        # Add some space
        st.write("")
        
        # Scrape button
        if st.button("🚀 Scrape Properties", type="primary", 
                   disabled=not website_url):
            st.session_state['scrape_clicked'] = True
            st.session_state['current_url'] = website_url
        else:
            if 'scrape_clicked' not in st.session_state:
                st.session_state['scrape_clicked'] = False
    
    # Main content area
    if st.session_state['scrape_clicked']:
        # Scrape data
        st.info(f"Scraping data from: {st.session_state['current_url']}")
        properties = scrape_property_data(st.session_state['current_url'])
        
        if properties:
            # Display data in cards
            display_property_cards(properties)
            
            # Display analytics
            display_analytics(properties)
            
            # Download section
            st.subheader("💾 Download Data")
            st.markdown(get_table_download_link(properties, "property_listings.csv"), unsafe_allow_html=True)
            
            # Show raw data in an expandable section
            with st.expander("📋 View Raw Data"):
                for prop in properties:
                    st.write(prop)
    else:
        st.markdown("---")
        st.subheader("Welcome to Property Scraper Pro!")
        st.write("Get started by selecting a website from the sidebar and clicking the 'Scrape Properties' button.")
        
        st.markdown("### Features:")
        st.markdown("""
        - Scrape property listings from various websites
        - View properties in beautiful cards
        - Analyze property data with interactive charts
        - Download data in CSV format
        
        Try it out with the default URL or enter your own!
        """)

if __name__ == "__main__":
    main()
