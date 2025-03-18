from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import re


chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.daimlercoachesnorthamerica.com/pre-owned-motor-coaches/"
driver.get(url)

#dinamycally wait time
wait = WebDriverWait(driver, 10)
selectedItems = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='coaches-models-wrapper']/div")))

print(f"Total matches: {len(selectedItems)}")

scraped_tems = []

#scrape logic using XPATH
for item in selectedItems[:3]:

    #scrape buses information
    try:
        title = item.find_element(By.XPATH, "./div[contains(@class, 'content')]/h4").text

        make_match = re.search(r"[\d]+\s(.*?)–", title)
        make_aux = make_match.group(1).strip() if make_match else None

        model = make_aux.replace("Mercedes Benz", "").replace("VH", "").replace("Setra", "").strip() if make_aux else None

        make = make_aux.replace(model, "").strip() if make_aux else None

        year_match = re.search(r"^([\d]+)\s", title)
        year = year_match.group(1).strip() if year_match else None

        try:
            mileage_element = item.find_element(By.XPATH, ".//h4/following-sibling::div[1]").text
            mileage_match = re.search(r"Mileage:(.*)\n", mileage_element)
            mileage = mileage_match.group(1).strip() if mileage_match else None
        except:
            mileage = None

        passengers_match = re.search(r"–\s([\d]+)\sPass", title)
        passengers = passengers_match.group(1) if passengers_match else None

        wheelchair = "Yes" if "ADA" in title else "No"

        try:
            engine_element = item.find_element(By.XPATH, ".//h4/following-sibling::div[1]").text
            engine_match = re.search(r"Engine:(.*)\n", engine_element)
            engine = engine_match.group(1).strip() if engine_match else None
        except:
            engine = None

        try:
            vin_element = item.find_element(By.XPATH, ".//h4/following-sibling::div[1]").text
            vin_match = re.search(r"VIN#:(.*)\n", vin_element)
            vin = vin_match.group(1).strip() if vin_match else None
        except:
            vin = None

        price_match = re.search(r"\$([\d.,]+)", title)
        price = price_match.group(1) if price_match else None

        #Scrape images
        item.find_element(By.XPATH, ".//a[@class='fancybox-gallery']").click()
        wait2 = WebDriverWait(driver, 5)
        selected_images = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'thumbs')]/a")))

        image_urls = [img.get_attribute("href") for img in selected_images]

        scraped_tems.append({
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
            "transmission": None,
            "gvwr": None,
            "location": None,
            "description": None,
            "features": None,
            "image_url": None,
            "image_metadata": None
        })
    except Exception as e:
        print(f"Error processing item: {e}")
    print(scraped_tems)

# Close the browser
driver.quit()