# As per assignment requirements, we need to extract all the information of 1 category. I choose 'Non-Fiction' for this exercise and below are the columns needed. 
# I will have to print this information in a csv file
# product_page_url,* universal_ product_code (upc), book_title, price_including_tax, price_excluding_tax, quantity_available,product_description, category, review_rating, image_url

#step1 : Using the pip -request, csv, beautiful soup, re and urllin to read the page "books to scrape. Print it to validate
import requests 
from bs4 import BeautifulSoup

booksite_url = "https://books.toscrape.com"
wpage = requests.get(booksite_url)
bs4soup = BeautifulSoup(wpage.content,'html.parser')
#step 2 - print all the sub categories
side_cate = bs4soup.select('.side_categories ul.nav-list ul li a')
print("side categories list is as below:")
for cat in side_cate:
    print(cat.get_text(strip = True))
#step 3 - get all subcategories URL 
def get_url_per_cate(category_name):
    side_categories = bs4soup.select('.side_categories ul.nav-list ul li a')
    for category  in side_categories :
     if category.get_text(strip = True).lower()== category_name.lower():
         return category['href']
    return None   
#step  4 - chk for NonFiction
category_name = "Nonfiction"
category_url = get_url_per_cate(category_name) 
if category_url:
      print(f"The URL for the '{category_name}' category is {category_url}")
else:
    print(f"URL not found for {category_name}")
#step 5- create the URL to open for Nonfiction 
# for this we need urljoin to create the total url

from urllib.parse import urljoin

product_pag_url = urljoin(booksite_url,category_url)    
#print(f"total_page_url for {category_name} = ",product_pag_url)
bpage = requests.get(product_pag_url)  
pagesoup = BeautifulSoup(bpage.content,'html.parser')

#count number of pages in this category
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
#print(f"product_page for {category_name} =" , product_pag_url)
#print(f"total number of pages in {category_name}=",total_pages_count)   

# ----------------------------------------------------------------#
# STEP 7 
#get the coulmns information by loop total pages count
#do for page number 1 first and then loop it
# --------------------------------------------------------------#
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

def get_page_url(base_url,page_number):
     if page_number == 1:
         return base_url
     else:
         return base_url.replace("index.html",f"page-{page_number}.html")
#print the results
p_num = 1
while p_num <= total_pages_count:
    print("page_number = ",p_num)
    url_for_page= get_page_url(product_pag_url,p_num)
    print(f"Page iteration = {p_num} URL: {url_for_page}")
    ipage = requests.get(url_for_page)
    soup = BeautifulSoup(ipage.content,'html.parser')
    j = 1
    #print("iteration =",j)    
    for artcl_tag in soup.find_all('article',class_ = 'product_pod'):
        img_line = soup.find('img') 
        if img_line:
            image_source = img_line.get('src')
        for a_tag in artcl_tag.find_all('a',href = True):
            book_url = a_tag.get('href')    
            book_page_url = urljoin(product_pag_url,book_url)
            #print("Book Page Url =",book_page_url)
            bookpage = requests.get(book_page_url) 
            #if bookpage.status_code == 200:
             #  print("able to open the page and read its contents")
            booksoup = BeautifulSoup(bookpage.content,'html.parser')
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
                            """
                    print("Product Page URL =",product_pag_url)
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
                    print("page_number = ",p_num)"""
                    row_cnt = j
                    col0 = all_count.append(row_cnt)
                    col1 = comp_url.append(product_pag_url)
                    col2 =upc_all.append(upc)
                    col3 = title_all.append(title)
                    col4 = prc_w_tax.append(price_inclu_tax)
                    col5 = prc_n_tax.append(price_exclu_tax)
                    col6 = qnt_avail.append(quantity_available)
                    col7 = prd_des.append(product_description)
                    col8 = cate.append(sub_category)
                    col9 = rev_rat.append(rating)
                    col10 = img_url.append(image_source)
                    col11 = pg_num.append(p_num)
        j = j+1        
    p_num = p_num +1

headers = ['page_number','Product_Page_Url','Universal_ Product_Code (UPC)','Book_Title','Price_Including_Tax','Price_Excluding_Tax','Quantity_Available','Product_Description','Category','Review_Rating','Image_Url']

import csv

with open(f'Books_of_Category-{category_name}.csv','w',newline='') as csvfile:

    writer= csv.writer(csvfile, delimiter= ',')
    writer.writerow(headers)
    for p in range(len(comp_url)):
     row = [pg_num[p],comp_url[p],upc_all[p],title_all[p],prc_w_tax[p],prc_n_tax[p],qnt_avail[p],prd_des[p],cate[p],rev_rat[p],img_url[p]]
     writer.writerow(row)