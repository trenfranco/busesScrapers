from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Create a Service object using ChromeDriverManager
service = Service(ChromeDriverManager().install())

# Start Chrome WebDriver with the service
driver = webdriver.Chrome(service=service)

# Open a webpage to test
driver.get("https://www.google.com")
print("Chrome WebDriver is working!")

# Close the browser
driver.quit()
