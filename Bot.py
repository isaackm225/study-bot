from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import action_builder
from gtts import gTTS
import time
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
    "documentation",
    "freecodecamp",
    "javatpoint",
    "tutorialspoint"
]

ressource_to_links = {}

# taking keyword
key = input("Please enter the concept that you would like explore: ")

# waits

def waitfor_results(driver):
    """waits for duckduckgo search results"""
    return driver.find_element(By.XPATH, '//*[@id="r1-3"]')

# meta
options = webdriver.ChromeOptions()
#options.add_argument("--enable-features=ReaderMode")
with webdriver.Chrome(options=options) as driver:
    waits = WebDriverWait(driver, timeout=10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException,ElementNotSelectableException,NoSuchElementException])
    for ressource in RESSOURCES:
        print(ressource)
        link_list = []
        driver.get(f'https://duckduckgo.com/?')
        input_field = driver.find_element(By.XPATH, '//input')
        input_field.send_keys(f'{key} {ressource}')
        input_field.send_keys(Keys.ENTER)
        waits.until(waitfor_results)
        first_result = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[3]/div/div[1]/div[5]/div[1]/article/div[1]/div/a')
        link_list.append(first_result)
        first_result.click()
        #Maybe we could make the program look for the reader view of the page



        #If we land on youtube we cannot scrap text 
        if "youtube" not in str(driver.title).lower():
        #went with one link inside the list as multiple links are trouble to find => code below is intermittent
        #make note to always go through the tools documentation b4 starting a project
        #waits.until(waitfor_results)
        #second_result = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[3]/div/div[1]/div[5]/div[2]/article/div[1]/div/a')
        #link_list.append(second_result)
        #waits.until(waitfor_results)
        #third_result = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[3]/div/div[1]/div[5]/div[3]/article/div[1]/div/a')
        #link_list.append(third_result)
        #waits.until(waitfor_results)
            ressource_to_links.setdefault(ressource,link_list)
        #print(ressource_to_links)
        #print(second_result.text)
        #print(third_result.text)
            body = driver.find_element(By.TAG_NAME,"body")
            time.sleep(5)
            action = ActionChains(driver)
            action.key_down(Keys.F9)
            action.key_up(Keys.F9)
            action.perform()
            txt = body.text
            print(txt)
            tts = gTTS(txt,lang='en')
            tts.save(f"{key}_{ressource}_{driver.title}.mp3")

        else:
            pass
        '''