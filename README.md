# Social-Media-Scrapper

There are two scrappers in this repo.
1. Reddit Scrapper (Using PRAW API)
2. YouTube Scrapper (Using Selenium + BeautifulSoup)

1. <ins>Reddit Scrapper</ins>: Given a serach term it will scrap comments from all the posts under that term. The serach term returns the result based on relevance. The comments are extracted up to a depth of 15 for nested comments. The comments are saved into a `csv` file.

2. <ins>YouTube Scrapper</ins>: Firstly, Selenium has been used to dynamically load the content (videos) of the target page (based on the search). From there approximately 150-200 videos are saved using BeautifulSoup. Then, comments are extracted for each of the video and are saved into a `csv` file.
