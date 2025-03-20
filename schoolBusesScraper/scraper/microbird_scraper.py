import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def microbird_scraper():
    '''Loads a local HTML file from /data and scrapes information using Selenium.'''

    # Get absolute path of the HTML file
    html_file_path = os.path.abspath(os.path.join(os.getcwd(), "data", "table_1.html"))

    # Convert file path to a URL format
    local_url = f"file:///{html_file_path.replace(os.sep, '/')}"
    
    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (optional)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the local HTML file in the browser
    driver.get(local_url)

    # Wait for the page to load
    time.sleep(2)
    scraped_items = []

    elements = driver.find_elements(By.XPATH, "//table")
    print(f"Elements selected: {len(elements)}")

    title = elements[0].find_element(By.XPATH, "./tbody/tr[1]/td[2]").text
    model = elements[0].find_element(By.XPATH, "./tbody/tr[2]/td[2]").text
    passengers = elements[0].find_element(By.XPATH, "./tbody/tr[3]/td[2]").text
    engine = elements[0].find_element(By.XPATH, "./tbody/tr[17]/td[2]").text
    has_brake = elements[0].find_element(By.XPATH, "./tbody/tr[21]/td[2]").text


    scraped_items.append({
            "title": title,
            "make": title,
            "model": model,
            "brake": has_brake,
            "year": None,
            "mileage": None,
            "passengers": passengers,
            "wheelchair": None,
            "engine": engine,
            "vin": None,
            "price": None,
            "images": None,
            "transmission": None,
            "gvwr": None,
            "location": None,
            "description": None,
            "features": None
        })

    # Close browser
    driver.quit()

    # Save JSON to file
    json_output = json.dumps(scraped_items, indent=4, ensure_ascii=False)
    with open("data/scraped_buses_microbird.json", "w", encoding="utf-8") as f:
        f.write(json_output)

    print("Scraping completed! Data saved to /data/scraped_buses_microbird.json")

    return "data/scraped_buses_microbird.json"

