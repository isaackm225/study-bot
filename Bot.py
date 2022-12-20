from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

# constant and credentials
RESSOURCES = [
    "The Real Python",
    "Healthline",
    "Medium",
    "How to Geek",
    "Network Chuck",
    "Fireship io",
    "Kevin Powell",
    "Web dev simplified",
    "Python Geeks",
    "W3 schools",
    "tech with tim",
    "documentation"
]

# taking keyword
key = input("Please enter the concept that you would like explore: ")

# waits

def waitfor_results(driver):
    """waits for duckduckgo search results"""
    return driver.find_element(By.TAG_NAME, 'article')

# meta
options = Options()
options.binary_location=r'C:\Users\Isaac Kone\AppData\Local\Mozilla Firefox\firefox.exe'
with webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options) as driver:
    waits = WebDriverWait(driver, timeout=10)
    for ressource in RESSOURCES:
        driver.get(f'https://duckduckgo.com/?')
        input_field = driver.find_element(By.XPATH, '//input')
        input_field.send_keys(f'{key} {ressource}')
        input_field.send_keys(Keys.ENTER)
        waits.until(waitfor_results)


