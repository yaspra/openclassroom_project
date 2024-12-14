###########################################################################################
# As per assignment requirements, we need to extract all the information of source page books_to_Scrape. 
# I will have to print this information in 50 csv files for each of 50 category
##########################################################################################



##########################################################################################
#     import the required pip packages and create soup for home page
##########################################################################################


import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import csv

booksite_url = "https://books.toscrape.com/"
wpage = requests.get(booksite_url)
bs4soup = BeautifulSoup(wpage.content,'html.parser')



##########################################################################################
#     Create arrays to load the category names and URLs to loop later in the script
##########################################################################################

categories_array = []
url_array = []
for side_categories in bs4soup.select('.side_categories ul.nav-list ul li a'):
        category_list = side_categories.get_text(strip = True)
        url_of_category = side_categories.get('href')
        comp_url_category = urljoin(booksite_url,url_of_category)
        category_col = categories_array.append(category_list)
        url_col = url_array.append(comp_url_category)


##################################################################################################################################################################################################################    
#                                           Define funtions to:
#                                                    1) remove the special chars and truncate to length 100
#                                                    2) create working url of based on the page number
#                                                    3) calculate total page count in a given url
##################################################################################################################################################################################################################

def char_string_name(bookname):
    chr_str = re.sub(r'[^A-Za-z0-9]','',f'{bookname}')
    chr_str_fn = chr_str[:100]
    return chr_str_fn

def get_page_url(base_url,page_number):
    if page_number == 1:
        return base_url
    else:
       return base_url.replace("index.html",f"page-{page_number}.html")

def get_total_page_cnt(soup,url):
    page_cnt = soup.find('ul',class_ = 'pager')
    if page_cnt:
        current_page = page_cnt.find('li',class_='current')
        if current_page:
            txt = current_page.get_text(strip =True)
            parts = txt.split()
            if len(parts) >= 3:
                total_pages = int(parts[-1])
            return total_pages
    return 1
 



   
i =0
while i < len(categories_array):
    #--------------------------------------------------------------------------------------------------------------------------------#
    #---------------------- Define empty array to ensure clean array for every category. these arrays are exported                  --#
    #---------------------------------------------------------------------------------------------------------------------------------#    
    prod_url_array = []
    title_all_array = []
    upc_array = []
    pric_inc_tax_array = []
    pric_exc_tax_array =[]
    availability_string = []
    qunt_avail_array = []
    prod_desc = []
    categ_array = []
    rev_rating_array = []
    img_array = []
    img_sav_as_array = []
    prod_desc_array = []    
    #--------------------------------------------------------------------------------------------------------------------------------#
    #---------------------- Start the category selection and populate the arrays with the  values required-------------------#
    #---------------------------------------------------------------------------------------------------------------------------------#   
    category_name = categories_array[i]
    category_url = url_array[i]
    catepage = requests.get(category_url)
    categorysoup = BeautifulSoup(catepage.content,'html.parser')
    #-------------------------------------------------------
    #pages count per category and loop as per the page count
    #-------------------------------------------------------
    pag_pr_cate = get_total_page_cnt(categorysoup,category_url)
    j = 1
    while j <= pag_pr_cate:
        page_url = get_page_url(category_url,j)
        page = requests.get(page_url)
        pagesoup = BeautifulSoup(page.content,'html.parser')
        #--------------------------------------------------------------------------
        # Read individual books per page to soup read and populate fields and array
        #--------------------------------------------------------------------------
        
        for artcl_tag in pagesoup.find_all('article',class_ = 'product_pod'):
            bk_lnk = artcl_tag.a.get('href')
            book_page_url = urljoin(category_url,artcl_tag.a.get('href'))
            bookpage = requests.get(book_page_url)             
            booksoup = BeautifulSoup(bookpage.content,'html.parser')
           
            ## ---------------------------------------------------------------------------------------------------------------------##
            ## ------------3.c.iii-  Created Book article tag with class = product_page for all of the book page
            # -------------- to retrive all required fields: UPC, product description, price including and excluding tags,
            #                                                           quantity avaiable, review counts,image source, title ,rating
            #--------------------------------------------------------------------------------------------------------------------------#  
            book_article_tag = booksoup.find('article',class_ ='product_page')
            img_src = book_article_tag.find('img').get('src')
            image_link = urljoin(book_page_url,img_src)
            title = book_article_tag.find('h1').get_text(strip=True)
            savd_as = char_string_name(title)+".jpg"
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
            avail_string = table_tag.find('th',string = 'Availability').find_next('td').get_text(strip=True)
            quantity_available = re.sub(r'\D', '', avail_string)
            review_count = table_tag.find('th',string = 'Number of reviews').find_next('td').get_text(strip=True)
            
            col0 = prod_url_array.append(book_page_url)
            col1 = upc_array.append(upc)
            col2 = title_all_array.append(title)
            col3 = pric_inc_tax_array.append(price_inclu_tax)
            col4 = pric_exc_tax_array.append(price_exclu_tax)
            col5 = qunt_avail_array.append(quantity_available)
            col6 = prod_desc_array.append(prod_descp)
            col7 = categ_array.append(category_name)
            col8 = rev_rating_array.append(review_count)
            col9 = img_array.append(image_link)
            col10 = img_sav_as_array.append(savd_as)
            col11 = availability_string.append(avail_string) 
        j = j+1
        headers = ['PRODUCT_PAGE_URL','UNIVERSAL_PRODUCT_CODE(UPC)','BOOK_TITLE','PRICE_INCLUDING_TAX','PRICE_EXCLUDING_TAX','AVAIL_CHK_AS_PER_HTML','QUANTITY_AVAILABLE','PRODUCT_DESCRIPTION','CATEGORY','REVIEW_RATING','IMAGE_URL','SAVED_AS']
        #################################################################################################################
        ####  STEP 3 : Export the data into .csv file per category
        #################################################################################################################
        with open(f'Catalog_For_{category_name}.csv','w',newline='',encoding='utf-8') as csvfile:
            writer= csv.writer(csvfile, delimiter= ',')
            writer.writerow(headers)
            for p in range(len(prod_url_array)):
                row =[prod_url_array[p],upc_array[p],title_all_array[p],pric_inc_tax_array[p],pric_exc_tax_array[p],availability_string[p],qunt_avail_array[p],prod_desc_array[p],categ_array[p],rev_rating_array[p],img_array[p],img_sav_as_array[p]]
                writer.writerow(row)   
    i = i+1


     
"""     
references : https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters

"""