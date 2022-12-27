from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from gtts import gTTS
import os
# constant and credentials

RESSOURCES_KEYWORDS = [
    "realpython",
    "medium",
    "geeksforgeeks",
    "freecodecamp",
    "tutorialspoint"
]

# taking keyword
key = input("Please enter the concept that you would like explore: ")
web_articles = [] #
# meta
options = webdriver.ChromeOptions()
#options.add_argument("--enable-features=ReaderMode")
with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException,ElementNotSelectableException,NoSuchElementException])
    driver.get('https://duckduckgo.com/?')
    input_field = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'searchbox_input__bEGm3')))
    input_field.send_keys(key)
    input_field.send_keys(Keys.ENTER)
    first_link = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div[3]/div/div[1]/div[5]/div[1]/article/div[1]/div/a')))
    for ressource in RESSOURCES_KEYWORDS:
        print(ressource)
        web_articles += driver.find_elements(By.PARTIAL_LINK_TEXT, ressource)
    for web_article in web_articles:
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL)
        action.move_to_element(web_article)
        action.click()
        action.perform()

    tabs = driver.window_handles
    print(tabs)
    for tab in tabs:
        driver.switch_to.window(tab)

    #first_link.click()
        if "realpython" in driver.current_url:
            article = driver.find_element(By.CLASS_NAME,'article')
            print(f"rp article saved")

        elif "medium" in driver.current_url:
            article = driver.find_element(By.TAG_NAME, 'article')
            print(f"medium article saved")

        elif "geeksforgeeks" in driver.current_url:
            article = driver.find_element(By.TAG_NAME, "article")
            print(f"gg article saved")

        elif "freecodecamp" in driver.current_url:
            article = driver.find_element(By.XPATH, "//*[@id='site-main']/div/article")
            print(f"fcc article saved")
        
        elif "tutorialspoint" in driver.current_url:
            article = driver.find_element(By.CLASS_NAME, "tutorial-content")
            print(f"tp article saved")
        
        else:
            article = None

        if article:
            try:
                    tts = gTTS(article.text,lang='en')
                    tts.save(f"./srv/{key.replace(' ', '_')}_{ressource}.mp3")
            except:
                os.mkdir("./srv/")
                tts = gTTS(article.text,lang='en')
                tts.save(f"./srv/{key.replace(' ', '_')}_{ressource}.mp3")