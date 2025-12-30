import asyncio
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.config import settings


def _generate_url_sync(donatello_user: str, uuid: str, amount: int) -> str:
    page = requests.get(
        "https://donatello.to/api/v1/me",
        headers={"X-Token": settings.donatello_token},
        timeout=10,
    ).json()["page"]
    
    url = "{page}?c={app_name}&a={amount}&m={uuid}".format(
        page=page,
        app_name=settings.name,
        amount=amount,
        uuid=uuid,
    )

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
        new_url = driver.current_url
    finally:
        driver.quit()

    return new_url


async def generate_url(donatello_user: str, uuid: str, amount: int) -> str:
    return await asyncio.to_thread(_generate_url_sync, donatello_user, uuid, amount)
