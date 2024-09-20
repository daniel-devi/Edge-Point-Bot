import json
import random
import requests
import time
# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Authentication details
from PASSWORD import EMAIL, PASSWORD

# Main
words_list = []

def wait_for(sec=3):
    '''
    Sets a Wait time for the program to wait
    '''
    time.sleep(sec)

def getRandomWordListsUrl():
    # Fetch random words from an online API
    randomWordListsUrl = "https://www.randomlists.com/data/words.json"
    response = requests.get(randomWordListsUrl)
    # Select 60 random words from the fetched data
    words_list.append(random.sample(json.loads(response.text)['data'], 60))
    print(f'{len(words_list)} words selected from {randomWordListsUrl}')

# Fetch random words
getRandomWordListsUrl()

# Initialize the Edge webdriver
driver = webdriver.Edge()

# Navigate to Microsoft login page
driver.get("https://login.live.com")
wait_for(5)

try:
    # Find and fill in the email field
    elem = driver.find_element_by_name('loginfmt')
    elem.clear()
    elem.send_keys(EMAIL) 
    elem.send_keys(Keys.RETURN)
    wait_for(5)

    # Find and fill in the password field
    elem1 = driver.find_element_by_name('passwd')
    elem1.clear()
    elem1.send_keys(PASSWORD)
    elem1.send_keys(Keys.ENTER)
    wait_for(5)
    
except Exception as e:
    print(e)
    wait_for(4)

# Base URL for Bing search
url_base = 'http://www.bing.com/search?q='
wait_for(5)

# Iterate through the list of words and perform searches
for num, word in enumerate(words_list[0], 1):  # Access the first (and only) sublist in words_list
    print(f'{num}. URL : {url_base + str(word)}')
    try:
        # Navigate to the search URL for the current word
        wait_for(10)
        driver.get(url_base + word)
        # Print the text of the first h2 element (usually the search result title)
        print(f'\t{driver.find_element_by_tag_name("h2").text}')
    except Exception as e1:
        print(e1)
    wait_for()

# Close the browser
driver.close()
driver.quit()