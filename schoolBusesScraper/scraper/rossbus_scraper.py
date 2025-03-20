from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import json
import re


def rossbus_scraper():
    '''Scrapes in HTML parser mode 
    and exports data as JSON file'''

    # Webdriver options config
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1366,768")
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-running-insecure-content")       

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://www.rossbus.com/used-buses"
    driver.get(url)

    scraped_items = []

    # Get total bus items
    bus_count = len(driver.find_elements(
                By.XPATH, "//ul[@class='NoBullet MoreProductWrapper']/li/div/div"))
    print(f"Total matches: {bus_count}")
    
    for index in range(bus_count):
        try:

            # Re-fetch selectedItems
            selectedItems = driver.find_elements(
                By.XPATH, "//ul[@class='NoBullet MoreProductWrapper']/li/div/div")
            item = selectedItems[index]

            # Extract title
            title = None
            try:
                title = "Bus: " + item.find_element(
                    By.XPATH, ".//h6").text
            except NoSuchElementException:
                pass

            # Extract make
            make = None
            try:
                make_text = item.find_element(
                    By.XPATH, ".//li[contains(., 'Make')]").text
                make = re.search(r"Make:(.*)", make_text).group(1).strip()
            except NoSuchElementException:
                pass

            # Extract model
            model = None
            try:
                model_text = item.find_element(
                    By.XPATH, ".//li[contains(., 'Model')]").text
                model = re.search(r"Model:(.*)", model_text).group(1).strip()
            except NoSuchElementException:
                pass

            # Extract year
            year = None
            try:
                year_text = item.find_element(
                    By.XPATH, ".//li[contains(., 'Year')]").text
                year = re.search(r"([\d]+)", year_text).group(1).strip()
            except NoSuchElementException:
                pass

            # Extract mileage
            mileage = None
            try:
                mileage_text = item.find_element(
                    By.XPATH, ".//li[contains(., 'Miles')]").text
                if mileage_text:
                    mileage = re.search(r"Miles:\s(.*)", mileage_text).group(1).strip()
            except NoSuchElementException:
                pass

            # Extract Passengers
            passengers = None
            try:
                passengers_text = item.find_element(
                    By.XPATH, ".//li[contains(., 'Capacity')]").text
                passengers = re.search(r"([\d.,]+)", passengers_text).group(1).strip()
            except NoSuchElementException:
                pass

            # Wheelchair accessibility
            wheelchair = None
            try:
                wheelchair_text = item.find_element(
                        By.XPATH, ".//li[contains(., 'Lift Equipped')]").text
                wheelchair = "Yes" if "Yes" in wheelchair_text else "No"
            except NoSuchElementException:
                pass

            # Extract engine
            engine = None

            # Extract VIN
            vin = None
            try:
                vin = item.find_element(
                    By.XPATH, ".//h6").text
            except NoSuchElementException:
                pass

            # Extract price
            price = None
            try:
                price_text = item.find_element(
                    By.XPATH, ".//span[@class='Total_Amount']").text
                price = price_text.replace("$", "").strip()
            except NoSuchElementException:
                pass

            # Extract image (only 1 available per listing)
            image_urls = []
            try:
                image = item.find_element(By.XPATH, ".//img").get_attribute("src")
                image_urls.append(image)
            except NoSuchElementException:
                image_urls = []

            # Extract color
            color = None
            try:
                color_text = item.find_element(
                    By.XPATH, ".//li[contains(., 'Color')]").text
                color = re.search(r"Color:(.*)", color_text).group(1).strip()
            except NoSuchElementException:
                pass

            # Extract has_brake
            has_brake = None
            try:
                has_brake_text = item.find_element(
                    By.XPATH, ".//li[contains(., 'Brakes')]").text
                has_brake = re.search(r"Brakes:(.*)", has_brake_text).group(1).strip()
            except NoSuchElementException:
                pass

            # Extract source URL
            source_url = None
            try:
                source_url = item.find_element(
                    By.XPATH, ".//a[contains(., 'read more')]").get_attribute("href")
            except NoSuchElementException:
                pass
        except Exception as e:
            print(f"Error processing bus {index+1}: {e}")

        # Store data
        scraped_items.append({
            "title": title,
            "make": make,
            "model": model,
            "year": year,
            "mileage": mileage,
            "passengers": passengers,
            "wheelchair": wheelchair,
            "engine": engine,
            "vin": vin,
            "price": price,
            "images": image_urls,
            "transmission": None,
            "gvwr": None,
            "location": None,
            "description": None,
            "features": None,

            "brake": has_brake,# new
            "color": color,# new
            "source_url": source_url# new
        })

    # Close browser
    driver.quit()

    # Save JSON to file
    json_output = json.dumps(scraped_items, indent=4, ensure_ascii=False)
    with open("data/scraped_buses_rossbus.json", "w", encoding="utf-8") as f:
        f.write(json_output)

    print("Scraping completed! Data saved to /data/scraped_buses_rossbus.json")

    return "data/scraped_buses_rossbus.json"
