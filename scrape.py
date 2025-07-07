from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import time

# Setup Chrome using webdriver-manager
def create_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run in headless mode
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

    wait = webdriver.support.ui.WebDriverWait(driver, 10)
    wait.until(lambda d: d.find_element(By.XPATH, "/html/body/div/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[3]/div/div[2]/div[4]/div[1]/div[1]/span"))  # wait

    intake = driver.find_element(By.XPATH, "/html/body/div/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[3]/div/div[2]/div[4]/div[1]/div[1]/span")
    try:
        burn = driver.find_element(By.XPATH, "/html/body/div[1]/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[1]/div[9]/span[2]")
    except:
        burn = 0
    weight = driver.find_element(By.XPATH, "/html/body/div[1]/md-content/md-content/div[1]/div[2]/md-content/div[6]/div[3]/div/div[2]/div[4]/div[2]/div[2]/div/span[1]")
    print(f"Intake: {intake.text}")
    print(f"Burn: {burn.text}")
    print(f"Weight: {weight.text}")
    return intake.text, burn.text, weight.text

def main():
    driver = create_driver()
    username = ""  # Replace with your username
    password = ""  # Replace with your password
    wait = WebDriverWait(driver, 10)
    try:
        login(driver, wait, username, password)
        time.sleep(2)
        intake, burn, weight = scrape_elements(driver, wait)
        intake = intake.replace(" kcal", "").replace("kcal", "").strip()
        burn = burn.replace(" kcal", "").replace("kcal", "").strip()
        weight = weight.replace(" kg", "").replace("kg", "").strip()
    finally:
        driver.quit()
        return intake, burn, weight

# Main script
if __name__ == "__main__":
    main()
