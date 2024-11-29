"""
This Script 
is the main python script to extract, load and create the output for the website "Books To Scrape". 

"""

#step1 : Using the pip -request read the page "books to scrape. Print it to validate

import requests
url = "https://books.toscrape.com"
wpage = requests.get(url)
print(wpage.content)

import requests 
from bs4 import BeautifulSoup

import csv
from bs4 import BeautifulSoup

url = "https://books.toscrape.com"
wpage = requests.get(url)
bs4page = BeautifulSoup(wpage.content,'html.parser')

#Below are tests of the page.
#Extract the page Name/Title of page
title_page= bs4page.title
#print(bs4page)
print(title_page)

printedtitles = bs4page.find_all("h3")
for pt in printedtitles:
    print(pt.string)
# but the above would not give me all of the title it would give me only what is printed on the page
h3_lines = bs4page.find('h3')
if h3_lines:
    a_lines = h3_lines.find('a')
    if a_lines:
         alltitle = a_lines.get('title')
print(f'alltile:{alltitle}')

# but above would give me only the complete result of 1st book on webpage
# creating a loop to ensure all names are extracted and printed
#additional variable added to count the total count of books
i = 1
for cnt in bs4page.find_all('h3'):
   #print(i)
    finda=cnt.find('a')
    if finda:
         get_title =finda.get('title')
    print(f'{i},{get_title}')
    
    i = i+1

# replicating the same and trying to append the results to each other
# as per instructions in course
all_titles =[]
all_count = []
j= 1
for h3_tag in bs4page.find_all('h3'):
 print("j=",j)
 a_tag=h3_tag.find('a')
 if a_tag:
         title_ext =a_tag.get('title')
         cnt= j
         title1 = title_ext
         print("results")
         print("total & count",cnt,title1)
         f0 = all_count.append(cnt)
         f1 = all_titles.append(title1)  
         print("appended_count=",all_count)       
         print("appended_title =",all_titles)
         headers = ['Row_No.','Title of the Book']         
         print("HEADERS",headers)
 j = j+1
 
 print("f1=",f1)
 lix = len(all_titles)
 print("total columns",lix)
#Step 3 to print the results of the titles and count above to a csv file.

with open('title_list.csv','w',newline='') as csvfile:
    writer= csv.writer(csvfile, delimiter= ',')
    writer.writerow(headers)
    for p in range(len(all_titles)):
       row = [all_count[p],all_titles[p]]
       writer.writerow(row)

# As per assignment requirements, we need to extract all the information of atleast 1 book.
# I choose "" for this exercise and below are the columns needed. I will have to print this information in a csv file
#     product_page_url, universal_ product_code (upc), book_title, price_including_tax, price_excluding_tax, quantity_available
#  product_description , category, review_rating, image_url
#
"""
Below is the HTML script for reference for Book - "a-light-in-the-attic-1000"
  <article class="product_pod">
        
            <div class="image_container">
                
                    
                    <a href="catalogue/a-light-in-the-attic_1000/index.html"><img src="media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg" alt="A Light in the Attic" class="thumbnail"></a>
                    
                
            </div>
        

        
            
                <p class="star-rating Three">
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                </p>
            
        

        
            <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a></h3>
        

        
            <div class="product_price">
                






    
        <p class="price_color">£51.77</p>
    

<p class="instock availability">
    <i class="icon-ok"></i>
    
        In stock
    
</p>

                
                    






    
    <form>
        <button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button>
    </form>


                
            </div>
        
    </article>

</li>
                    
                        <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">


"""
all_titles =[]
all_count = []
j= 1
for h3_tag in bs4page.find_all('h3'):
 print("j=",j)
 a_tag=h3_tag.find('a')
 if a_tag:
         title_ext =a_tag.get('title')
         cnt= j
         title1 = title_ext
         print("results")
         print("total & count",cnt,title1)
         f0 = all_count.append(cnt)
         f1 = all_titles.append(title1)  
         print("appended_count=",all_count)       
         print("appended_title =",all_titles)
         headers = ['Row_No.','Title of the Book']         
         print("HEADERS",headers)
 j = j+1
 
 print("f1=",f1)
 lix = len(all_titles)
 print("total columns",lix)