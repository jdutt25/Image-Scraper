# Jessica Dutton
# OSU CS 361
# Image Scraping Service

import requests
from requests.api import get
from selenium import webdriver
from flask import request 
from flask import Flask
import json
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/postmethod', methods=['POST'])

def postmethod():
    data = request.get_json()
    data = json.loads(data)
    print ('DATA', data)
    for i in data:
        key = i
    return getImageUrl(data[key])

def getImageUrl(keyword):
    print('KEYWORD', keyword)
    

    searchWords = ""

    if keyword == [""] or keyword == [" "] or not keyword:
        return "ERROR: Please submit at least one keyword"

    else:
        for i in keyword:
            searchWords += i
            searchWords += " "

    from selenium.webdriver.chrome.options import Options

    # use headless browser to prevent browser pop up

    options = Options()
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')  
    
    driver = webdriver.Chrome(chrome_options= options)

    driver.get("https://www.bing.com/images")                           # go to Bing images
    driver.find_element_by_name("q").send_keys(keyword)                 # input keyword(s)
    driver.implicitly_wait(10)
    driver.find_element_by_id("sb_search").click()                      # search
    driver.implicitly_wait(10)

    lst = driver.find_element_by_id("mmComponent_images_2")             # find images in first list on Bing
    images = lst.find_elements_by_tag_name("li")

    images[0].click()                                                   # first image
    driver.implicitly_wait(10)
                            
    response = requests.get(driver.current_url  )                       # use beautiful soup to obtain image url
    
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]
    image_url = urls[0]


    driver.close()    

    return ''+image_url

if __name__ == '__main__':
    app.run()

#print(getImageUrl("good company novel"))