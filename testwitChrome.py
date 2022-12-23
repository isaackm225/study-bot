from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import action_builder
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager




options = Options()
#options.binary_location=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
with Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
    driver.get('https://quotes.toscrape.com/')
    footer = driver.find_element(By.TAG_NAME, "footer")
    delta_y = footer.rect['y']
    ActionChains(driver)\
        .scroll_by_amount(0, delta_y)\
        .perform()