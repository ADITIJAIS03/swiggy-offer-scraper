# Swiggy Offer Scraper 🛍️

This Python script is designed to scrape restaurant offers from Swiggy. It extracts details like restaurant names, their special offers (e.g., Buy 1 Get 1), food items, prices, and saves the data into an Excel file for further analysis. The scraper uses **Selenium** for browsing automation and **Pandas** for handling the scraped data.

## Overview

The **Swiggy Offer Scraper** is built to scrape restaurant offers on Swiggy, such as **Buy 1 Get 1**, **Veg**, and other special deals. The script collects details of the food items, prices, and any special offers, then saves them in an Excel file (`filtered_swiggy_offers.xlsx`). This can help users track discounts and offers available at Swiggy.

### Features:
- Scrapes special offers and food items from Swiggy restaurant menus.
- Filters for offers like **Buy 1 Get 1** and **Veg** items.
- Extracts restaurant details such as restaurant name and URL.
- Saves the scraped data to an Excel file for easy reference.

## Prerequisites

Before you can run the script, you need to have the following installed:

- **Python 3.x**: Make sure you have Python 3.x installed. You can download it from [here](https://www.python.org/downloads/).
- **Chrome WebDriver**: Since this project uses Selenium with Chrome, download the correct version of [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) based on your Chrome browser version.

## Setup Instructions

1. **Clone the repository or download the files**:
   - If you have Git installed, clone the repository:
     ```bash
     git clone https://github.com/ADITIJAIS03/swiggy-offer-scraper.git
     ```
   - Alternatively, download the files as a zip and extract them.

2. **Install the required libraries**:
   - It’s recommended to use a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
     pip install -r requirements.txt
     ```

3. **Download ChromeDriver**:
   - Ensure that `chromedriver.exe` is either added to your system’s PATH or is in the same directory as the script.
   - Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

4. **Prepare your input file**:
   - Ensure that the input file (`filtered_swiggy_offers.xlsx`) is available and contains restaurant names and URLs from which you want to scrape offers.

## How to Use

1. **Input File Setup**:
   - The script expects an input Excel file (`filtered_swiggy_offers.xlsx`) that contains the restaurant names and Swiggy URLs.
   - Ensure that this file is in the same directory as the Python script.

2. **Running the Script**:
   To start scraping, simply run the script using:
   ```bash
   python swiggy_offer_scraper.py
