"""
This Script 
is the main python script to extract, load and create the output for the website "Books To Scrape". 

"""

#step1 : Using the pip -request read the page "books to scrape. Print it to validate
import requests
from bs4 import BeautifulSoup
import csv


#step 2 : ingest webpage into soup

url = "https://books.toscrape.com"
wpage = requests.get(url)
bs4page = BeautifulSoup(wpage.content,'html.parser')

#step3 : creating a loop to ensure all names are extracted and printed
#additional variable added to count the total count of books
all_titles =[]
all_count = []
j= 1
for h3_tag in bs4page.find_all('h3'):
    a_tag=h3_tag.find('a')
    if a_tag:
        title_ext =a_tag.get('title')
        cnt= j
        title1 = title_ext
        f0 = all_count.append(cnt)
        f1 = all_titles.append(title1)  
        headers = ['Row_No.','Title of the Book']         
        j = j+1
 
#lix = len(all_titles)
 
#Step 4 : print the results of the titles and count above to a csv file.

with open('title_list.csv','w',newline='') as csvfile:
    writer= csv.writer(csvfile, delimiter= ',')
    writer.writerow(headers)
    for p in range(len(all_titles)):
       row = [all_count[p],all_titles[p]]
       writer.writerow(row)
