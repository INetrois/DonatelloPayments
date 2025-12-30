import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = "https://donatello.to/Degchan?a=600&c=token&m=information"

os.environ.setdefault("MOZ_HEADLESS", "1")
options = Options()

options.headless = True
options.add_argument("-headless")
options.add_argument("--headless=new")

driver = webdriver.Firefox(options=options, keep_alive=False)
wait = WebDriverWait(driver, 15)

try:
    driver.get(url)

    btn = wait.until(EC.element_to_be_clickable((By.ID, "submit-button")))
    old_url = driver.current_url
    btn.click()

    wait.until(EC.url_changes(old_url))
    print(driver.current_url)
finally:
    driver.quit()
