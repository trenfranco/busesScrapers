from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def download_pdf():
    '''Dwnload PDF files'''

    # Get the absolute path
    download_path = os.path.abspath(os.path.join(os.getcwd(), "./data"))

    # Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,  # Set your folder
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True  # Prevents opening PDFs in browser
    })
    chrome_options.add_argument("--headless=new")

    # Launch Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open website
    driver.get("https://www.microbird.com/school-vehicles")

    # Wait for elements to load
    wait = WebDriverWait(driver, 10)

    # Get total bus items
    elements = wait.until(EC.presence_of_all_elements_located((
            By.XPATH, '//a[@data-testid="linkElement"][span[contains(., "G5")'
            ' or contains(., "T-Series") or contains(., "MB")]]')))

    print(f"Elements selected: {len(elements)}")

    for index, element in enumerate(elements):
        try:
            # Get the URL before clicking
            bus_page_url = element.get_attribute("href")

            # Open bus detail page in a new tab
            driver.execute_script(f"window.open('{bus_page_url}', '_blank');")

            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[-1])
            print(f"Navigated to: {bus_page_url}")

            # Wait for the PDF link to appear
            pdf_link = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@href, ".pdf")]')))
            pdf_url = pdf_link.get_attribute("href")

            # Download pdf
            driver.get(pdf_url)

            # Wait for the PDF to download
            time.sleep(5)  # Adjust if necessary

            # Close the PDF tab
            driver.close()
            
            # Switch back to the main page
            driver.switch_to.window(driver.window_handles[0])

            print("Downloaded PDF")

        except Exception as e:
            print(f"Error processing {bus_page_url}: {e}")

    print("PDF download started!")

    driver.quit()

download_pdf()
