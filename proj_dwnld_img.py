# As per assignment requirements, we need to extract all the information of source page books_tp_Scrape. 
#

###################################################################################################################################################################################
###   step1 : Using the pip -request, csv, beautiful soup, "books to scrape. 
###  Ingest the URL into env
#################################################################################################################################################################################

import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import csv
import os


booksite_url = "https://books.toscrape.com/"
wpage = requests.get(booksite_url)
bsoup = BeautifulSoup(wpage.content,'html.parser')
curnt_dir = os.getcwd()
sub_fldr = "images"
img_path = os.path.join(curnt_dir,sub_fldr)
os.makedirs(img_path,exist_ok=True)
###################################################################################################################################################################################
##    1.a Calculate the number of page in the URL - defined a function - get_pg_cnt
###################################################################################################################################################################################
def get_pg_cnt(url):
    pg_count = bsoup.find('ul',class_ = 'pager')
    if pg_count:
        this_page = pg_count.find('li',class_='current')
        if this_page:
            text = this_page.get_text(strip =True)
            parts = text.split()
            if len(parts) >= 3:
                total_numof_pages = int(parts[-1])
            return total_numof_pages
    return 1
total_count_pages = get_pg_cnt(booksite_url)    

###################################################################################################################################################################################
##    1.b Generate the URL based on the page number . Defined a function : get_url_of_page
###################################################################################################################################################################################
def get_page_url(base_url,page_number):
    if page_number == 1:
        return base_url
    else:
        return f'{base_url}/catalogue/page-{page_number}.html'
##################################################################################################################################
# step2 : create 2 functions:
#             a. to remove the speecial char and restrict to 100 char to use as a name
#             b. create function to define to download image URL
#################################################################################################################################################################################

def char_string_name(bookname):
    chr_str = re.sub(r'[^A-Za-z0-9]','',f'{bookname}')
    chr_str_fn = chr_str[:100]
    return chr_str_fn

def img_dwlnd(image_link,save_as):
    img = requests.get(image_link)
    with open(f"{img_path}/{save_as}",'wb')as i_file:
        i_file.write(img.content)
  
##################################################################################################################################
# step3 : create loop to get the titles of the books and their image source download
####################################################################################################################################

title_all =[]
img_url = []
saveas = []
p_num = 1
while p_num <= total_count_pages:
    url_for_page= get_page_url(booksite_url,p_num)
    ipage = requests.get(url_for_page)
    soup = BeautifulSoup(ipage.content,'html.parser')
    j = 1
    for artcl_tag in soup.find_all('article',class_ = 'product_pod'):   
            book_page_url = urljoin(url_for_page,artcl_tag.h3.a.get('href'))
            bookpage = requests.get(book_page_url) 
            booksoup = BeautifulSoup(bookpage.content,'html.parser')
            ## ---------------------------------------------------------------------------------------------------------------------##
            ## ------------3.i  Created Book article tag with class = product_page 
            # -------------- to retrive all required title and image_url
            #--------------------------------------------------------------------------------------------------------------------------#       
            book_article_tag = booksoup.find('article',class_ ='product_page')
            img_src = book_article_tag.find('img').get('src')
            image_source = urljoin(book_page_url,img_src)
            title = book_article_tag.find('h1').get_text(strip=True)
                        
            bookname_print=char_string_name(title)
            save_as = bookname_print + ".jpg"
            image_exmaple = img_dwlnd(image_source,save_as)

                   
            row_cnt = j
            col1 = title_all.append(title)
            col2 = saveas.append(bookname_print)
            col3 = img_url.append(image_source)
            j = j+1        
    p_num = p_num +1            

headers = ['TITLE','SAVED_AS','IMAGE_LINK']
##################################################################################################################################
# step4 : create csv file for validation
####################################################################################################################################

with open('csvlist_of_images.csv','w',newline='',encoding='utf-8')  as csvfile :
    writer= csv.writer(csvfile, delimiter= ',')
    writer.writerow(headers)
    for p in range(len(title_all)):
        row = [title_all[p],saveas[p],img_url[p]]
        writer.writerow(row)
     