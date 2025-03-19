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

# Webdriver options config
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1366,768")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.daimlercoachesnorthamerica.com/pre-owned-motor-coaches/"
driver.get(url)

# Wait for elements to load
wait = WebDriverWait(driver, 10)

scraped_items = []

# Get total bus items
bus_count = len(wait.until(EC.presence_of_all_elements_located((
        By.XPATH, "//div[@class='coaches-models-wrapper']/div"))))
print(f"Total matches: {bus_count}")

for index in range(bus_count):
    try:
        # Refresh HTML
        driver.refresh()

        # Re-fetch selectedItems
        selectedItems = wait.until(EC.presence_of_all_elements_located((
            By.XPATH, "//div[@class='coaches-models-wrapper']/div")))
        item = selectedItems[index]

        # Extract title
        title = item.find_element(
            By.XPATH, ".//div[contains(@class, 'content')]/h4").text

        # Extract make and model
        make_match = re.search(r"[\d]+\s(.*?)–", title)
        make_aux = make_match.group(1).strip() if make_match else None
        model = (make_aux.replace("Mercedes Benz", "")
                 .replace("VH", "").replace("Setra", "")
                 .strip() if make_aux else None)
        make = make_aux.replace(model, "").strip() if make_aux else None

        # Extract year
        year_match = re.search(r"^([\d]+)\s", title)
        year = year_match.group(1).strip() if year_match else None

        # Extract mileage
        mileage = None
        try:
            mileage_text = item.find_element(
                By.XPATH, ".//h4/following-sibling::div[1]").text
            mileage_match = re.search(r"Mileage:\s([\d.,]+)", mileage_text)
            mileage = mileage_match.group(1).strip() if mileage_match else None
        except NoSuchElementException:
            pass

        # Extract Passengers
        passengers_match = re.search(r"–\s([\d]+)\sPass", title)
        passengers = passengers_match.group(1) if passengers_match else None

        # Wheelchair accessibility
        wheelchair = "Yes" if "ADA" in title else "No"

        # Extract engine
        engine = None
        try:
            engine_text = item.find_element(
                By.XPATH, ".//h4/following-sibling::div[1]").text
            engine_match = re.search(r"Engine:(.*)\n", engine_text)
            engine = engine_match.group(1).strip() if engine_match else None
        except NoSuchElementException:
            pass

        # Extract VIN
        vin = None
        try:
            vin_text = item.find_element(
                By.XPATH, ".//h4/following-sibling::div[1]").text
            vin_match = re.search(r"VIN#:(.*)\n", vin_text)
            vin = vin_match.group(1).strip() if vin_match else None
        except NoSuchElementException:
            pass

        # Extract price
        price_match = re.search(r"\$([\d.,]+)", title)
        price = price_match.group(1) if price_match else None

        # Click to open image gallery
        try:
            item.find_element(
                By.XPATH, ".//a[@class='fancybox-gallery']").click()
            wait2 = WebDriverWait(driver, 10)
            selected_images = wait2.until(EC.presence_of_all_elements_located((
                By.XPATH, "//div[contains(@class, 'thumbs')]/a")))

            # Extract image URLs
            image_urls = []
            for img in selected_images:
                try:
                    url_match = re.search(
                        r"\((.*)\)", img.get_attribute("style"))
                    image_urls.append(url_match.group(1))
                except NoSuchElementException:
                    image_urls.append(None)

            # Dinamycally wait and click close button
            close_button = WebDriverWait(driver, 5).until(
             EC.presence_of_element_located((
              By.XPATH, "//button[@title='Close']")))
            close_button.click()
        except NoSuchElementException:
            image_urls = []  # If galerry fails return empty list

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
            "image_url": None,
            "image_metadata": None
        })
    except Exception as e:
        print(f"Error processing bus {index+1}: {e}")

# Close browser
driver.quit()

# Save JSON to file
json_output = json.dumps(scraped_items, indent=4, ensure_ascii=False)
with open("data/scraped_buses.json", "w", encoding="utf-8") as f:
    f.write(json_output)

print("Scraping completed! Data saved to scraped_buses.json")
