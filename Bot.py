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
    "Medium",
    "Geeks for Geeks",
    "W3 schools",
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
with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
    waits = WebDriverWait(driver, timeout=10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException,ElementNotSelectableException,NoSuchElementException])
    for ressource in RESSOURCES:
        print(ressource)
        link_list = []
        driver.get(f'https://duckduckgo.com/?')
        time.sleep(5)
        input_field = driver.find_element(By.CLASS_NAME, 'searchbox_input__bEGm3')
        input_field.send_keys(f'{key} {ressource}')
        input_field.send_keys(Keys.ENTER)
        waits.until(waitfor_results)
        first_result = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[3]/div/div[1]/div[5]/div[1]/article/div[1]/div/a')
        link_list.append(first_result)
        first_result.click()
        ressource_to_links.setdefault(ressource,link_list)
        #Maybe we could make the program look for the reader view of the page
        #For now just going with per ressources scraping template
        if "realpython" in str(driver.current_url):
            article = driver.find_element(By.CLASS_NAME,'article')

        elif "medium" in str(driver.current_url):
            article = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div/main/div/div[3]/div/div/article/div/div[2]/section/div/div[2]')

        elif "geeksforgeeks" in str(driver.current_url):
            article = driver.find_element(By.XPATH, "//*[@id='post-449297']")

        elif "w3schools" in str(driver.current_url):
            article = driver.find_element(By.XPATH, "//*[@id='main']")

        elif "freecodecamp" in str(driver.current_url):
            article = driver.find_element(By.XPATH, "//*[@id='site-main']/div/article")
        
        elif "tutorialspoint" in str(driver.current_url):
            article = driver.find_element(By.XPATH, "//*[@id='mainContent']")
        
        else:
            article = driver.find_element(By.TAG_NAME, "body")

        #If we land on youtube we cannot scrap text 
        #went with one link inside the list as multiple links are trouble to find => code below is intermittent
        #make note to always go through the tools documentation b4 starting a project
        #waits.until(waitfor_results)
        #second_result = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[3]/div/div[1]/div[5]/div[2]/article/div[1]/div/a')
        #link_list.append(second_result)
        #waits.until(waitfor_results)
        #third_result = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[3]/div/div[1]/div[5]/div[3]/article/div[1]/div/a')
        #link_list.append(third_result)
        #waits.until(waitfor_results)
        #print(ressource_to_links)
        #print(second_result.text)
        #print(third_result.text)
        tts = gTTS(article.text,lang='en')
        tts.save(f"{key}_{ressource}_{driver.title}.mp3")