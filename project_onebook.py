# As per assignment requirements, we need to extract all the information of 1 book. I choose "A Light in the Attic" for this exercise and below are the columns needed. 
# I will have to print this information in a csv file
# product_page_url,* universal_ product_code (upc), book_title, price_including_tax, price_excluding_tax, quantity_available,product_description, category, review_rating, image_url

#step1 : Using the pip -request, csv, beautiful soup, re and urllin to read the page "books to scrape. Print it to validate
import re
from urllib.parse import urljoin

import requests 
from bs4 import BeautifulSoup

book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
wpage = requests.get(book_url)
booksoup = BeautifulSoup(wpage.content,'html.parser')

#step 2 : identify the page and open the page of the book "A Light in the Attic"

for title_tag in booksoup.find('h1'):
        if title_tag:
         title = title_tag.text.strip() 
upc = booksoup.find('th',text = 'UPC').find_next_sibling('td').text
price_exclu_tax = booksoup.find('th',text = 'Price (excl. tax)').find_next_sibling('td').text 
price_inclu_tax = booksoup.find('th',text = 'Price (incl. tax)').find_next_sibling('td').text
tax_added = booksoup.find('th',text= 'Tax').find_next_sibling('td').text
review_count = booksoup.find('th',text= 'Number of reviews').find_next_sibling('td').text
meta_tag = booksoup.find('meta',attrs={'name':'description'})
if meta_tag:
    product_description = meta_tag.get('content','').strip()
quantity_available = booksoup.find('th',text = 'Availability').find_next_sibling('td').text
breadcrumb = booksoup.find('ul',class_ = 'breadcrumb')
if breadcrumb:
    li_tag = breadcrumb.find_all('li')
    if len(li_tag)> 1:
        category = li_tag[1].get_text(strip= True)
        if len(li_tag) > 2:    
         sub_category = li_tag[2].get_text(strip= True)
p_tag = booksoup.find('p',class_ = 'star-rating')
rating = "yet to know"
if p_tag:
    r_list = p_tag.get('class',[])
    if len(r_list) > 1:
        rating = r_list[1]  
im_tag = booksoup.find('img')
if im_tag:
    image_source = im_tag.get('src')        
print("Product Page URL =",book_url)
print("UPC = ",upc)
print("Book_Title=",title)
print("price excluding tax =",price_exclu_tax)
print("price_including_tax =",price_inclu_tax)
print("Tax Added =",tax_added)
print("review_count =",review_count)
print("Quantity_available=",quantity_available)
print("product_description =",product_description)
print("category =", category)
print("subcategory=",sub_category)
print("rating=",rating)
print("image_source =",image_source)

headers = ['Product_Page_Url','Universal_ Product_Code (UPC)','Book_Title','Price_Including_Tax','Price_Excluding_Tax','Quantity_Available','Product_Description','Category','Review_Rating','Image_Url']

import csv
with open ('one_book_details.csv','w',newline='') as csvfile:
    writer = csv.writer(csvfile,delimiter = ',')
    writer.writerow(headers)
    row = [book_url,upc,title,price_exclu_tax,price_inclu_tax,quantity_available,product_description,sub_category,rating,image_source]
    writer.writerow(row)
