from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from openpyxl import Workbook
from io import BytesIO
import os
from tqdm import tqdm  # Importing tqdm for progress bar

# List of cities to process
cities = ["Ranchi","Jamshedpur", "Dhanbad", "Bhagalpur", "Gaya"]

# List of restaurant names to exclude
excluded_restaurants = [
    "Barbeque Nation", "GetAWay-Ice Creams & Desserts", "Barista Coffee", "Baskin Robbins Happyness Shakes",
    "Bikkgane Biryani", "Ovenfresh Cakes and Desserts", "Baskin Robbins - Ice Cream Desserts", "IGP Cakes",
    "The Dugout", "Biryani By Kilo", "Cafe Coffee Day", "Crusto's - Cheese Burst Pizza By Olio", "Dum Safar Biryani",
    "Faasos Signature Wraps & Rolls", "Firangi Bake", "Goila Butter Chicken", "Haldiram's Prabhuji",
    "LunchBox - Meals and Thalis", "Namaste Bowl", "Olio - The Wood Fired Pizzeria", "Veg Meals by Lunchbox",
    "Delights by INOX", "Keventers - Milkshakes & Desserts", "Vadilal Ice Creams", "Faasos - Wraps, Rolls & Shawarma",
    "Subway", "Sweet Truth - Cake and Desserts", "The Biryani Life", "The Good Bowl", "Wow! China",
    "Oven Story Pizza - Standout Toppings", "The Pizza Project by Oven Story", "UBQ by Barbeque Nation",
    "KFC", "Burger King", "Veg Daawat by Behrouz", "Pizza Hut", "Chai Break", "Behrouz Biryani",
    "Kouzina Kafe - The Food Court", "NIC Ice Creams", "Sundae Everyday Ice Creams", "Cupcake Bliss Cake & Desserts",
    "Slurpy Shakes", "Kaati Zone Rolls & Wraps", "Indiana Burgers", "Burger It Up", "McDonald's", "Biryani Badshah",
    "Domino's Pizza", "Wow! Momo", "PVR Cafe", "Cheesecakes By CakeZone", "The Dessert Heaven - Pastry, Brownie and Cakes",
    "CakeZone Patisserie", "Wow! Kulfi", "Wow! China", "La Pino'z Pizza", "Starbucks Coffee"
]

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

all_city_data = []

try:
    first_city_processed = False

    for city_name in cities:
        print(f"Processing city: {city_name}")
        driver.get("https://www.swiggy.com/offers-near-me")
        time.sleep(5)

        # Click "Others" if needed for subsequent cities
        if first_city_processed:
            try:
                others_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Others")]'))
                )
                others_button.click()
                time.sleep(5)
            except Exception as e:
                print(f"Error clicking 'Others' for {city_name}: {e}")

        # Click "Setup your precise location" for the first city
        if not first_city_processed:
            try:
                setup_location_btn = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Setup your precise location")]'))
                )
                setup_location_btn.click()
                time.sleep(5)
                first_city_processed = True
            except Exception as e:
                print(f"Error clicking setup location: {e}")
                continue

        # Enter city name in location search
        try:
            location_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search for area, street name..."]'))
            )
            location_input.clear()
            location_input.send_keys(city_name)
            time.sleep(3)

            first_suggestion = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="sc-beySbM eZHJfb"]'))
            )
            first_suggestion.click()
            time.sleep(7)
        except Exception as e:
            print(f"Error selecting location for {city_name}: {e}")
            continue

        # Click "Order Online" tab
        try:
            online_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "food-offer-near-me")]/div[contains(text(), "Order Online")]'))
            )
            online_tab.click()
            time.sleep(7)
        except Exception as e:
            print(f"Error clicking 'Order Online': {e}")
            continue

        # Click "Show More" to load all offers
        clicks = 0
        max_clicks = 100
        while clicks < max_clicks:
            try:
                show_more_button = WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Show more")]'))
                )
                show_more_button.click()
                clicks += 1
                time.sleep(6)
            except:
                break

        print(f"Completed clicking 'Show More' {clicks} time(s).")

        # Extract restaurant names, offers, and links
        print("Extracting restaurant names, offers, and links...")
        restaurant_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "sc-beySbM eLaouz")]')
        offer_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "sc-beySbM lnKOIC") or contains(@class, "sc-beySbM cUSKbj")]')
        link_elements = driver.find_elements(By.XPATH, '//a[contains(@class, "RestaurantList__RestaurantAnchor-sc-1d3nl43-3 kcEtBq")]')

        print(f"Total restaurants found: {len(restaurant_elements)}")
        print(f"Total offers found: {len(offer_elements)}")
        print(f"Total links found: {len(link_elements)}")

        # Adding progress bar for scraping
        for i in tqdm(range(min(len(restaurant_elements), len(offer_elements), len(link_elements))), desc="Extracting Data"):
            name = restaurant_elements[i].text.strip() if i < len(restaurant_elements) else "Unknown"
            offer = offer_elements[i].text.strip() if i < len(offer_elements) else "No Offer"
            link = link_elements[i].get_attribute("href") if i < len(link_elements) else "No Link"

            if name and offer and link:
                all_city_data.append({"Restaurant Name": name, "City": city_name, "Offer": offer, "Link": link})

    df = pd.DataFrame(all_city_data)
    if df.empty:
        print("No data scraped! Check XPaths or loading issues.")
    else:
        # Filtering out rows where the offer doesn't contain the word "item"
        filtered_df = df[df['Offer'].str.contains("item", case=False, na=False)]

        # Excluding specific restaurants
        excluded_restaurants_lower = [name.lower() for name in excluded_restaurants]
        filtered_df = filtered_df[~filtered_df['Restaurant Name'].str.lower().isin(excluded_restaurants_lower)]

        # Save to Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Filtered Data"
        ws.append(filtered_df.columns.tolist())

        for row in filtered_df.itertuples(index=False):
            ws.append(list(row))

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        with open("filtered_swiggy_offers.xlsx", "wb") as temp_file:
            temp_file.write(buffer.read())

        os.system("filtered_swiggy_offers.xlsx")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    input("Press Enter to close the browser...")
    driver.quit()
