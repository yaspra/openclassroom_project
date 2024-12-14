# As per assignment requirements, we need to extract all the information of source page books_tp_Scrape. 
# I will have to print this information in a csv file
# product_page_url,* universal_ product_code (upc), book_title, price_including_tax, price_excluding_tax, quantity_available,product_description, category, review_rating, image_url

###################################################################################################################################################################################
###   step1 : Using the pip -request, csv, beautiful soup, "books to scrape. 
###  Ingest the URL into env
#################################################################################################################################################################################

import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import csv
import re


booksite_url = "https://books.toscrape.com/"
wpage = requests.get(booksite_url)
btcsoup = BeautifulSoup(wpage.content,'html.parser')

###################################################################################################################################################################################
###   #1.a count number of pages 
###################################################################################################################################################################################

def get_pg_cnt(url):
    pg_count = btcsoup.find('ul',class_ = 'pager')
 #   print(pg_count)    
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

##################################################################################################################################################################################################################    
#                                              STEP 2 : define the column names array to be populated and  create the loop to read each page and each book
##################################################################################################################################################################################################################

all_count = []
url =[]
comp_url = []
upc_all = []
title_all = []
prc_w_tax = []
prc_n_tax =[]
qnt_avail = []
prd_des =[]
cate =[]
rev_rat =[]
img_url =[]
pg_num = []
bk_num_in_pg = []

#3.c - initiate the loop for the page =1 to the total number of pages per step #2.b
p_num = 1
while p_num <=total_count_pages:
    url_for_page= get_page_url(booksite_url,p_num)
    ipage = requests.get(url_for_page)
    soup = BeautifulSoup(ipage.content,'html.parser')
    j = 1
    #--------------------------------------------------------------------------------------------------------------------------------#
    #---------------------- 3.c.i -Create the article tag for the page number url and get the individual book url--------------------#
    #---------------------------------------------------------------------------------------------------------------------------------#
    for artcl_tag in soup.find_all('article',class_ = 'product_pod'):   
            book_page_url = urljoin(url_for_page,artcl_tag.h3.a.get('href'))
            bookpage = requests.get(book_page_url) 
            booksoup = BeautifulSoup(bookpage.content,'html.parser')
            #--------------------------------------------------------------------------------------------------------------------------#
            #--------- 3.c.ii - Create tag1 : to define category (subcategory in HTML script) using class = breadcrumb
            #--------------------------------------------------------------------------------------------------------------------------#
            tags1 = booksoup.find(class_='breadcrumb')
            if tags1:
                li_tags = tags1.find_all('li')
                if li_tags[2]:  
                    category = li_tags[2].find('a').get_text(strip=True) 
            ## ---------------------------------------------------------------------------------------------------------------------##
            ## ------------3.c.iii-  Created Book article tag with class = product_page 
            # -------------- to retrive all required fields: UPC, product description, price including and excluding tags,
            #                                                           quantity avaiable, review counts,image source, title ,rating
            #--------------------------------------------------------------------------------------------------------------------------#       
            book_article_tag = booksoup.find('article',class_ ='product_page')
            img_src = book_article_tag.find('img').get('src')
            image_source = urljoin(book_page_url,img_src)
            title = book_article_tag.find('h1').get_text(strip=True)
            p_string = book_article_tag.find('i').find_next(class_ ='icon-star').find_previous('p').get('class',[])
            rating = p_string[1]
            if (book_article_tag.find('h2').get_text(strip=True) == 'Product Description'):
                prod_descp = book_article_tag.find('h2').find_next('p').get_text(strip=True)
            else:
                prod_descp = "No Description Available"    
            table_tag = book_article_tag.find('table',class_ = 'table table-striped')
            upc = table_tag.find_next('td').get_text(strip=True)
            price_exclu_tax = table_tag.find('th',string ='Price (excl. tax)').find_next('td').get_text(strip=True)
            price_inclu_tax = table_tag.find('th',string='Price (incl. tax)').find_next('td').get_text(strip=True)
            tax_added = table_tag.find('th',string='Tax').find_next('td').get_text(strip=True)
            qa = table_tag.find('th',string = 'Availability').find_next('td').get_text(strip=True)
            quantity_available =  re.sub(r'\D', '', qa)
            review_count = table_tag.find('th',string = 'Number of reviews').find_next('td').get_text(strip=True)
            
            row_cnt = j
            col0 = all_count.append(row_cnt)
            col1 = comp_url.append(book_page_url)
            col2 =upc_all.append(upc)
            col3 = title_all.append(title)
            col4 = prc_w_tax.append(price_inclu_tax)
            col5 = prc_n_tax.append(price_exclu_tax)
            col6 = qnt_avail.append(quantity_available)
            col7 = prd_des.append(prod_descp)
            col8 = cate.append(category)
            col9 = rev_rat.append(rating)
            col10 = img_url.append(image_source)
            col11 = pg_num.append(p_num)
            j = j+1        
    p_num = p_num +1            


headers = ['Product_Page_Url','Universal_ Product_Code (UPC)','Book_Title','Price_Including_Tax','Price_Excluding_Tax','Quantity_Available','Product_Description','Category','Review_Rating','Image_Url']


##################################################################################################################################################################################################################    
#                                             STEP 3: Export the arrays to a csv
##################################################################################################################################################################################################################
with open('Catalogue_BooksToScrape.csv','w',newline='',encoding='utf-8')  as csvfile :

    writer= csv.writer(csvfile, delimiter= ',')
    writer.writerow(headers)
    for p in range(len(upc_all)):
     row = [comp_url[p],upc_all[p],title_all[p],prc_w_tax[p],prc_n_tax[p],qnt_avail[p],prd_des[p],cate[p],rev_rat[p],img_url[p]]
     writer.writerow(row)
     
     
"""     
references : https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters

"""