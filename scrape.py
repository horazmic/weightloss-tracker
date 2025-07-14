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

    wait.until(lambda d: d.find_element(By.XPATH, "/html/body/div/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[3]/div/div[2]/div[4]/div[1]/div[1]/span"))  # wait

    try:
        intake = driver.find_element(By.XPATH, "/html/body/div/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[3]/div/div[2]/div[4]/div[1]/div[1]/span").text
    except:
        raise Exception("Intake element not found. Please check the XPath or the page structure.")
    try:
        weight = driver.find_element(By.XPATH, "/html/body/div[1]/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[3]/div/div[2]/div[4]/div[2]/div[2]/div/span[1]").text
    except:
        raise Exception("Weight element not found. Please check the XPath or the page structure.")
    try:
        burn = driver.find_element(By.XPATH, "/html/body/div[1]/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[1]/div[9]/span[2]").text
    except:
        burn = '0'
    return intake, burn, weight

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
        intake, burn, weight = scrape_elements(driver, wait)
        intake = intake.replace(" kcal", "").replace("kcal", "").strip()
        burn = burn.replace(" kcal", "").replace("kcal", "").strip()
        weight = weight.replace(" kg", "").replace("kg", "").strip()
        print(f"Intake: {intake} kcal, Burn: {burn} kcal, Weight: {weight} kg")
        return intake, burn, weight
    finally:
        driver.quit()

# Main script
if __name__ == "__main__":
    main()
