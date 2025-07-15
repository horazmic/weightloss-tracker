from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import time
from dotenv import load_dotenv
import os
load_dotenv()

# Setup Chrome using webdriver-manager
def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--window-size=1920,1080")  # Set window size to typical monitor resolution
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login(driver, wait, username, password):
    driver.get("https://www.dine4fit.com/login")

    username_field = driver.find_element(By.ID, "input_2")
    password_field = driver.find_element(By.ID, "input_3")
    login_button = driver.find_element(By.XPATH, "/html/body/div[1]/md-content/md-content/div[1]/div/md-content/div/div[1]/div[3]/button")

    # wait for page to load
    wait.until(lambda d: d.find_element(By.ID, "input_2"))
    time.sleep(1)

    username_field.send_keys(username)
    password_field.send_keys(password)
    time.sleep(1)
    login_button.click()

def scrape_elements(driver, wait):
    url = "https://www.dine4fit.com/user/diary"
    driver.get(url)
    xpaths = {
        "intake": "/html/body/div/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[3]/div/div[2]/div[4]/div[1]/div[1]/span",
        "burn": "/html/body/div[1]/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[1]/div[9]/span[2]",
        "weight": "/html/body/div[1]/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[3]/div/div[2]/div[4]/div[2]/div[2]/div/span[1]",
        "protein": "/html/body/div/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div[3]/span[1]",
    }
    wait.until(lambda d: d.find_element(By.XPATH, xpaths["intake"]))
    data = {}
    try:
        for xpath in xpaths:
            data[xpath] = driver.find_element(By.XPATH, xpaths[xpath]).text
    except Exception as e:
        raise Exception(f"Element not found: {e}")
    return data

def main():
    driver = create_driver()
    username = os.getenv("dine4fit_username")
    password = os.getenv("dine4fit_password")
    if not username or not password:
        raise ValueError("Email credentials are not set in the environment variables.")

    wait = WebDriverWait(driver, 10)
    try:
        login(driver, wait, username, password)
        time.sleep(2)
        return scrape_elements(driver, wait)
    finally:
        driver.quit()

# Main script
if __name__ == "__main__":
    main()