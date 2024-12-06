# As per assignment requirements, we need to extract all the information of source page books_tp_Scrape. 
# I will have to print this information in a csv file
# product_page_url,* universal_ product_code (upc), book_title, price_including_tax, price_excluding_tax, quantity_available,product_description, category, review_rating, image_url

#step1 : Using the pip -request, csv, beautiful soup, "books to scrape. Print it to validate
import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin

booksite_url = "https://books.toscrape.com/index.html"
wpage = requests.get(booksite_url)
finalsoup = BeautifulSoup(wpage.content,'html.parser')
#count number of pages 
def get_pg_cnt(url):
    pg_count = finalsoup.find('ul',class_ = 'pager')
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
print(f"total number of pages in {booksite_url} = ",total_count_pages)   

def get_url_of_page(homepage,num):
  if num == 1:
    return homepage
  else:
    return homepage.replace("index.html",f"catalogue/page-{num}.html")
#print the results
required_url = get_url_of_page(booksite_url,23)
print(required_url)

# ----------------------------------------------------------------#
# STEP 2
#get the coulmns information by loop total pages count
#do for page number 1 first and then loop it
# --------------------------------------------------------------#
complete_url = []
upc_string = []
title_string = []
price_with_tax = []
price_without_tax =[]
quant_avail = []
prod_desp =[]
categry =[]
review_rates =[]
imge_lnk =[]
page_numb = []
buk_num_in_page = []

page_num = 1
while page_num <= total_count_pages:
    #print("page_number = ",page_num)
    url_for_page= get_url_of_page(booksite_url,page_num)
    print(f"Page iteration = {page_num} URL: {url_for_page}")
    page = requests.get(url_for_page)
    pagesoup = BeautifulSoup(page.content,'html.parser')
    j = 1
    #print("iteration =",j)    
    for artcl_tag in pagesoup.find_all('article',class_ = 'product_pod'):
        img_line = pagesoup.find('img') 
        if img_line:
            image_source = img_line.get('src')
        for a_tag in artcl_tag.find_all('a',href = True):
            book_url = a_tag.get('href')    
            book_page_url = urljoin(booksite_url,book_url)
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
                    row_cnt = j
                    col1 = complete_url.append(book_page_url)
                    col2 =upc_string.append(upc)
                    col3 = title_string.append(title)
                    col4 = price_with_tax.append(price_inclu_tax)
                    col5 = price_without_tax.append(price_exclu_tax)
                    col6 = quant_avail.append(quantity_available)
                    col7 = prod_desp.append(product_description)
                    col8 = categry.append(sub_category)
                    col9 = review_rates.append(rating)
                    col10 = imge_lnk.append(image_source)
                    col11 = page_numb.append(page_num)
    j = j+1        
page_num = page_num +1

headers = ['page_number','Product_Page_Url','Universal_ Product_Code (UPC)','Book_Title','Price_Including_Tax','Price_Excluding_Tax','Quantity_Available','Product_Description','Category','Review_Rating','Image_Url']

import csv

with open('Books_of_Scrape.csv','w',newline='') as csvfile:

    writer= csv.writer(csvfile, delimiter= ',')
    writer.writerow(headers)
    for p in range(len(complete_url)):
     row = [page_numb[p],complete_url[p],upc_string[p],title_string[p],price_with_tax[p],price_without_tax[p],quant_avail[p],prod_desp[p],categry[p],review_rates[p],imge_lnk[p]]
     writer.writerow(row)
