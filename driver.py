"""
    Utility functions to keep track of upto which problems have been downloaded so that we can continue from 
    that problem if downloading of questions stop halfway 
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager

# Tracks the questions we have already downloaded
def create_driver():

    # Setup Selenium Webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    
    options.add_argument('--log-level=3')                   # Show only fatal errors
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-data-dir=" + ".config/chromium")

    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager().install()), options=options)
    
    return driver