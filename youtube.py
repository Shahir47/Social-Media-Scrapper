from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import collections
import time
import csv
import re

collections.Callable = collections.abc.Callable


initial_link = 'https://www.youtube.com/results?search_query=vaccine+hesitancy'
link_storage = []

#open a csv file
file = open('YouTube_scrapper.csv', 'w', newline='')
writer = csv.writer(file)

writer.writerow(['links', 'Comments'])

#This will extract approximately 150-200 youtube video links in a page
def extract_link():
    global link_storage, initial_link

    #initialize the driver
    service = Service("chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    #load the url
    driver.get(initial_link)
    time.sleep(10)

    #initially scrolling
    driver.execute_script('window.scrollTo(0, 1000);') #scrollTo is method of window object

    #scroll 20 more times to load contents
    for i in range(20):
        driver.execute_script('window.scrollTo(0, 100000);')
        time.sleep(10)

    #load the page into BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "lxml")

    if soup:
        time.sleep(10)

        #extract all the target links
        for a_tag in soup.find_all('a'):
            link = a_tag.get('href')
            if link and re.search('^/watch', link) != None:
                link_modified = 'https://www.youtube.com' + link

                if re.search('(.+)&', link_modified) != None:
                    link_modified = re.findall('(.+)&', link_modified)[0]

                if link_modified not in link_storage:
                    link_storage.append(link_modified)

    for link in link_storage:
        print(link)

    driver.quit()

#preprocess text
def preprocess(txt):
    #remove links
    txt = re.sub('https.+', '', txt)
    #take only ascii characters
    txt = ''.join([ch if ord(ch)<=127 else '' for ch in txt])

    return txt

#extract all the head comments from a given link
def comment_extractor(lnk):
    global writer

    try:
        #initialize the driver
        service = Service("chromedriver-win64/chromedriver.exe")
        driver = webdriver.Chrome(service=service)

        #load the url
        driver.get(lnk)
        time.sleep(10)

        #initially scrolling
        driver.execute_script('window.scrollTo(0, 1000);') #scrollTo is method of window object

        #continuous scrolling until the end
        old_position = driver.execute_script('return document.getElementById("comments").scrollHeight;')
        while True:
            driver.execute_script('window.scrollTo(0, 100000);')
            time.sleep(10)
            new_position = driver.execute_script('return document.getElementById("comments").scrollHeight;')

            if old_position == new_position:
                break

            old_position = new_position

        #extract comments
        comments = driver.find_elements(By.CSS_SELECTOR, '#content-text')
        print(len(comments))
        for comment in comments:
            txt = preprocess(comment.text)
            print(txt)
            if txt:
                writer.writerow([lnk, txt])

        #close the driver
        driver.quit()
                    
    except:
        print(f'Failed -> {lnk}')


def main():
    extract_link()
    skip = 0
    #skip first ten links
    for link in link_storage:
        if skip<10:
            skip += 1
        else:
            time.sleep(4)
            print(f'Working with -> {link}')
            comment_extractor(link)

if __name__ == "__main__":
    main()