# As per assignment requirements, we need to extract all the information of 1 category. I choose 'Non-Fiction' for this exercise and below are the columns needed. 
# I will have to print this information in a csv file
# product_page_url,* universal_ product_code (upc), book_title, price_including_tax, price_excluding_tax, quantity_available,product_description, category, review_rating, image_url
##################################################################################################################################################################################################
#Requirements : Using the pip -request, csv, beautiful soup, urljoin to read the page "books to scrape. Print it to validate
###################################################################################################################################################################################################
import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
####################################################################################################################################################################################################
##                                       STEP 1                                                                                                                                                  ##
##       1.a Ingest the main URL into env. 
##       1.b Get the list of all categories - printed in side of the homepage
##       1.c  Define a function to get the number of pages per category - Nonfiction
#####################################################################################################################################################################################################

booksite_url = "https://books.toscrape.com/"
wpage = requests.get(booksite_url)
bs4soup = BeautifulSoup(wpage.content,'html.parser')

#step 1.b - print all the sub categories
side_cate = bs4soup.select('.side_categories ul.nav-list ul li a')
print("side categories list is as below:")
for cat in side_cate:
    print(cat.get_text(strip = True))
    
#step 1.c - get all subcategories URL 
def get_url_per_cate(category_name):
    side_categories = bs4soup.select('.side_categories ul.nav-list ul li a')
    for category  in side_categories :
     if category.get_text(strip = True).lower()== category_name.lower():
         return category['href']
    return None  
 
#Below is the check for pages for category_name = Nonfiction.
category_name = "Nonfiction"
category_url = get_url_per_cate(category_name) 
if category_url:
      print(f"The URL for the '{category_name}' category is {category_url}")
else:
    print(f"URL not found for {category_name}")
    
##################################################################################################################################################################################################################    
#                                              STEP 2
#          2.a Create URL for Nonfiction using urlJoin for this we need urljoin to create the total url
#          2.b  Count the number of pages per this category and use the output to loop
##################################################################################################################################################################################################################
#step 2.a
product_pag_url = urljoin(booksite_url,category_url)    
#print(f"total_page_url for {category_name} = ",product_pag_url)
bpage = requests.get(product_pag_url)  
pagesoup = BeautifulSoup(bpage.content,'html.parser')

#step2.b count number of pages in this category
def get_total_page_cnt(url):
    page_cnt = pagesoup.find('ul',class_ = 'pager')
 #   print(page_cnt)    
    if page_cnt:
        current_page = page_cnt.find('li',class_='current')
        if current_page:
            txt = current_page.get_text(strip =True)
            parts = txt.split()
            if len(parts) >= 3:
                total_pages = int(parts[-1])
            return total_pages
    return 1
total_pages_count = get_total_page_cnt(product_pag_url)  
print(f"product_page for {category_name} =" , product_pag_url)
print(f"total number of pages in {category_name}=",total_pages_count)   

def get_page_url(base_url,page_number):
    if page_number == 1:
        return base_url
    else:
        return f'{base_url}/catalogue/page-{page_number}.html'
print('page_number_23',get_page_url(booksite_url,40))   

##################################################################################################################################################################################################################    
#                                              STEP 3
#          2.a define the column names array to be populated
#          2.b create the loop to read each page and each book
##################################################################################################################################################################################################################
#step 3.a

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

#2.b - initiate the loop for the page =1 to the total number of pages per step #2.b
p_num = 1
while p_num <= total_pages_count:
    print("page_number = ",p_num)
    url_for_page= get_page_url(product_pag_url,p_num)
    print(f"Page iteration = {p_num} URL: {url_for_page}")
    ipage = requests.get(url_for_page)
    soup = BeautifulSoup(ipage.content,'html.parser')
    j = 1
    print("iteration =",j)  
    #--------------------------------------------------------------------------------------------------------------------------------#
    #---------------------- 3.c.i -Create the article tag for the page number url and get the individual book url--------------------#
    #---------------------------------------------------------------------------------------------------------------------------------#
    for artcl_tag in soup.find_all('article',class_ = 'product_pod'):
            print("chk_url =",urljoin(product_pag_url,artcl_tag.h3.a.get('href')))     
            book_page_url = urljoin(product_pag_url,artcl_tag.h3.a.get('href'))
            print("Book Page Url =",book_page_url)
            bookpage = requests.get(book_page_url) 
            if bookpage.status_code == 200:
                print("able to open the page and read its contents")
            booksoup = BeautifulSoup(bookpage.content,'html.parser')
            #--------------------------------------------------------------------------------------------------------------------------#
            #--------- 3.c.ii - Create tag1 : to define category (subcategory in HTML script) & title of book from book page
            #--------------------------------------------------------------------------------------------------------------------------#
            tags1 = booksoup.find(class_='breadcrumb')
            if tags1:
                li_tags = tags1.find_all('li')
                if li_tags[1]:
                    CAT1 = li_tags[1].find('a').get_text(strip=True)
                if li_tags[2]:  
                    category = li_tags[2].find('a').get_text(strip=True) 
                if li_tags[3]:  
                    title = li_tags[3].get_text(strip=True)
            ## ---------------------------------------------------------------------------------------------------------------------##
            ## ------------3.c.iii-  Created Book article tag with class = product_page 
            # -------------- to retrive all required fields: UPC, product description, price including and excluding tags,
            #                                                           quantity avaiable, review counts
            #--------------------------------------------------------------------------------------------------------------------------#       
            book_article_tag = booksoup.find('article',class_ ='product_page')
            prod_descp = book_article_tag.find(class_ = 'sub-header').find_next_sibling('p').get_text(strip=True)
            table_tag = book_article_tag.find('table',class_ = 'table table-striped')
            upc = table_tag.find_next('td').get_text(strip=True)
            price_exclu_tax = table_tag.find('th',string ='Price (excl. tax)').find_next('td').get_text(strip=True)
            price_inclu_tax = table_tag.find('th',string='Price (incl. tax)').find_next('td').get_text(strip=True)
            tax_added = table_tag.find('th',string='Tax').find_next('td').get_text(strip=True)
            quantity_available = table_tag.find('th',string = 'Availability').find_next('td').get_text(strip=True)
            review_count = table_tag.find('th',string = 'Number of reviews').find_next('td').get_text(strip=True)           
            ## ---------------------------------------------------------------------------------------------------------------------##
            ## ------------3.c.iv-  Create a tag class = product_pod-
            # -------------- to retrive all required fields: image link and rating
            #--------------------------------------------------------------------------------------------------------------------------#    
            book_article_tag2 = booksoup.find('article',class_ ='product_pod')
            img_src = book_article_tag2.find('img').get('src')
            image_source = urljoin(book_page_url,img_src)
            rating_string = book_article_tag2.find('p').get('class',[])
            rating = rating_string[1]
            print('Category=',category,'title=',title)
            print(upc,price_exclu_tax,price_inclu_tax,quantity_available,review_count)
            print(prod_descp)  
            print(rating)
            print(image_source)
            print(img_src)
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


headers = ['page_number','Product_Page_Url','Universal_ Product_Code (UPC)','Book_Title','Price_Including_Tax','Price_Excluding_Tax','Quantity_Available','Product_Description','Category','Review_Rating','Image_Url']

print("upc",upc_all)
import csv

with open(f'BookDetails_of_Category-{category_name}.csv','w',newline='') as csvfile:

    writer= csv.writer(csvfile, delimiter= ',')
    writer.writerow(headers)
    for p in range(len(comp_url)):
     row = [pg_num[p],comp_url[p],upc_all[p],title_all[p],prc_w_tax[p],prc_n_tax[p],qnt_avail[p],prd_des[p],cate[p],rev_rat[p],img_url[p]]
     writer.writerow(row)