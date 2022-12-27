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
web_articles = [] 

# taking input
key = input("Please enter the concept that you would like explore: ")

# scraping
options = webdriver.ChromeOptions()
with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException,ElementNotSelectableException,NoSuchElementException])
    driver.get('https://duckduckgo.com/?')

    #ddg homepage
    input_field = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'searchbox_input__bEGm3')))
    input_field.send_keys(key)
    input_field.send_keys(Keys.ENTER)

    #ddg result page
    first_link = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div[3]/div/div[1]/div[5]/div[1]/article/div[1]/div/a')))
    for ressource in RESSOURCES_KEYWORDS:
        web_articles += driver.find_elements(By.PARTIAL_LINK_TEXT, ressource)
    for web_article in web_articles: #opening ea article in a tab
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL)
        action.move_to_element(web_article)
        action.click()
        action.perform()

    tabs = driver.window_handles
    for tab in tabs:
        title=""
        print(tab.title)
        driver.switch_to.window(tab)

    #first_link.click()
        if RESSOURCES_KEYWORDS[0] in driver.current_url:
            article = driver.find_element(By.CLASS_NAME,'article')
            title = RESSOURCES_KEYWORDS[0]
            print("rp")

        elif RESSOURCES_KEYWORDS[1] in driver.current_url:
            article = driver.find_element(By.TAG_NAME, "article")
            title = RESSOURCES_KEYWORDS[1]
            print("m")

        elif RESSOURCES_KEYWORDS[2] in driver.current_url:
            article = driver.find_element(By.TAG_NAME, "article")
            title = RESSOURCES_KEYWORDS[2]
            print("gg")

        elif RESSOURCES_KEYWORDS[3] in driver.current_url:
            article = driver.find_element(By.XPATH, "//*[@id='site-main']/div/article")
            title = RESSOURCES_KEYWORDS[3]
            print("fc")

        elif RESSOURCES_KEYWORDS[4] in driver.current_url:
            article = driver.find_element(By.CLASS_NAME, "tutorial-content")
            title = RESSOURCES_KEYWORDS[4]
            print("tp")


        else:
            article = None
            print("ddg")

        if article:
            print(article)
            try:
                print('Not creating new srv/ folder')
                tts = gTTS(article.text,lang='en')
                tts.save(f"./srv/{key.replace(' ', '_')}_{title}.mp3")
            except:
                print("creating new srv/")
                os.mkdir("./srv/")
                tts = gTTS(article.text,lang='en')
                tts.save(f"./srv/{key.replace(' ', '_')}_{title}.mp3")