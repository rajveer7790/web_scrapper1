# 🏠 Property Scraper Pro

A Streamlit-based web application that scrapes property listings from various real estate websites. The application allows users to view property details in a clean card format, analyze property data, and download the data in CSV format.

## Features

- Scrape property listings from various real estate websites
- View properties in beautiful, responsive cards
- Analyze property data with interactive charts
- Download data in CSV format
- Simple and intuitive web interface

## Prerequisites

- Python 3.8+
- Streamlit
- Required Python packages (listed in requirements.txt)

## Local Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd Web-scraper
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application locally:
   ```bash
   streamlit run app.py
   ```

## Deployment to Streamlit Cloud

1. Push your code to a GitHub repository

2. Go to [Streamlit Cloud](https://share.streamlit.io/)

3. Click on "New app" and connect your GitHub account

4. Select your repository and branch

5. Set the main file path to `app.py`

6. Click "Deploy!"

## Environment Variables

No environment variables are required for the basic functionality. If you need to add any sensitive information later, you can add them in the Streamlit Cloud settings.

## Configuration

You can customize the app's appearance by modifying the `.streamlit/config.toml` file.

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
2. Open the provided URL in your web browser (usually http://localhost:8501)
3. Enter the website URL or use the default Property Onion URL
4. Click "Scrape Properties" to start scraping
5. Once complete, you can view the data and download it as a CSV file

## Supported Websites

- Property Onion (https://propertyonion.com/property_search)
- More websites can be added by extending the scraper functions

## Note

- The scraper uses Selenium with Chrome WebDriver for dynamic content loading
- Make sure you have a stable internet connection
- Some websites might have anti-scraping measures in place

## License

This project is open source and available under the MIT License.
