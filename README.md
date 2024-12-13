# openclassroom_project
This repository is created to aid the project course "Python Basics for Market Analysis" form openclassroom sponsored by Guild. The readme file should have all the details.

########################################3
### REQUIREMENTS 
### Ensure your python environment
##  For this exercise we have installed beautifulsoup,csv,urllib,re pip packages.

#-----------------------------------------------------------------------
#------------------- EXTENSIVE LIST OF ALL OF CATALOGUE ---------------
#----------------------------------------------------------------------
To obtain the extensive list of the catalgoue with all the required fields of books.to.scrape.com download "project_etl_final.py".Execute in your environment. 

#-----------------------------------------------------------------------
#------------------- IMAGES DOWNLOAD ---------------
#----------------------------------------------------------------------
To obtain the images repo in your local environment.Execute "proj_dwnld_img.py".This script will create a subfolder in your current working directory and save all the images in that subfolder however, a csv detailing all the titles and image links with name "csvlist_of_images.csv" in your working directory.
#-----------------------------------------------------------------------
#------------------- 1 BOOK DOWNLOAD-------------- ---------------
#----------------------------------------------------------------------
To obtain 1 book details execute "project_onebook.py". if you want to test other books kindly change the "book_url" field value as required.

#-----------------------------------------------------------------------
#------------------- 1 CATEGORY DETAILS------------- ---------------
#----------------------------------------------------------------------
To obtain 1 category details execute "project_onecategory.py" The script is slated to detail the required reporting columns to category =Nonfiction. if needs to be changed to an another, use any value from the output of defined function:get_url_per_cate and assign to the variable = category_name

