from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from pytube import Search
from gtts import gTTS
import ffmpy
import os


class Bot():
    def __init__(self, key:str):
        self.websites = [
            "realpython",
            "medium",
            "geeksforgeeks",
            "freecodecamp",
            "tutorialspoint"
            ]
        self.key = key
        self.channels = [
            "Network Chuck",
            "fireship io",
            "Kevin Powell",
            "Tech with Tim",
            "Mental Outlaw",
            "Leo's Bag Of Tricks",
            "Techno Tim",
            "Computerphile",
            "No Boilerplate",
            "ElectroBoom",
            "GreatScott",
            "Zaney",
            "DistroTube",
            "sentdex",
            "Engineer Man",
            "NoMagic"
        ]

    def read_articles(self, articles: dict)-> None:
        """ Saves the string passed as an audio file with the title"""
        for title in articles:
            article = articles[title]
            if article:
                try:
                    print('Not creating new srv/ folder')
                    tts = gTTS(article,lang='en')
                    tts.save(f"./srv/{self.key.replace(' ', '_')}_{title}.mp3")
                except:
                    print("creating new srv/")
                    os.mkdir("./srv/")
                    tts = gTTS(article,lang='en')
                    tts.save(f"./srv/{self.key.replace(' ', '_')}_{title}.mp3")

    def scrap_articles(self)-> tuple:
        """Scraps the www returns a tuple containing a relevant article (str) given a keyword and a title as a string"""
        scrapped_articles = dict()
        options = webdriver.ChromeOptions()
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
            web_articles = []
            wait = WebDriverWait(driver, timeout=10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException,ElementNotSelectableException,NoSuchElementException])
            driver.get('https://duckduckgo.com/?')

            #ddg homepage
            input_field = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-search-input')))
            input_field.send_keys(self.key)
            input_field.send_keys(Keys.ENTER)

            #ddg result page
            first_link = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div[3]/div/div[1]/div[5]/div[1]/article/div[1]/div/a')))
            for ressource in self.websites:
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
                driver.switch_to.window(tab)

                if self.websites[0] in driver.current_url:
                    article = driver.find_element(By.CLASS_NAME,'article').text
                    title = self.websites[0]

                elif self.websites[1] in driver.current_url:
                    article = driver.find_element(By.TAG_NAME, "article").text
                    title = self.websites[1]

                elif self.websites[2] in driver.current_url:
                    article = driver.find_element(By.TAG_NAME, "article").text
                    title = self.websites[2]

                elif self.websites[3] in driver.current_url:
                    article = driver.find_element(By.XPATH, "//*[@id='site-main']/div/article").text
                    title = self.websites[3]

                elif self.websites[4] in driver.current_url:
                    article = driver.find_element(By.CLASS_NAME, "tutorial-content").text
                    title = self.websites[4]


                else:
                    article = ""

                scrapped_articles.setdefault(title,article)
            return scrapped_articles

    def scrap_videos(self):
        for channel in self.channels:
            s = Search(f'{self.key} {channel}')
            vid = s.results[0]
            streams = vid.streams.filter(only_audio=True)
            stream = streams[0]
            stream.download()
    
    def vformat(self):
        dir = os.listdir()
        for file in dir:
            if file.endswith(".mp4"):
                print("2")
                mp4_audio = AudioSegment.from_file(f"./{file}", format="mp4")
                mp4_audio.export(f"{file}.mp3", format="mp3")

    def clean(self):
        dir = os.listdir()
        for file in dir:
            if file.endswith(".mp4"):
                os.rename(f"{file}",f"./srv/{file}")

if __name__=="__main__":
    key = input("Please enter the concept you would like to explore: ")
    j = Bot(key)
    scrapped_articles = j.scrap_articles()
    j.read_articles(scrapped_articles)
    j.scrap_videos()
    j.clean()