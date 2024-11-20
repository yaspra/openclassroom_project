"""
This Script is the main python script to extract, load and create the output for the website "Books To Scrape". 

"""

#step1 :Install requests and beautiful soup.

pip install requests
pip install bs4

#step2 : Using the pip -request read the page "books to scrape. Print it to validate

import requests
url = "https://books.toscrape.com"
page = requests.get(url)
print(page.content)


