# Overview
1. This repository is created to aid the project course "Python Basics for Market Analysis" form openclassroom sponsored by Guild.
1. This project involves web scrapping "books.toscrape.com" to extract columns specified in project requirements document to aid price monitoring system.

## Prerequisites
1. Python is installed.Refer to references (python installation) for installation gudiance.
1. pip package manager for python.
1. Internet connection to access the targeted website.

## Clone the repository
1. In the directory of your prefrence clone the repository in your environment -->`git clone https://github.com/yaspra/openclassroom_project.git`
1. If planning to use virtual environment(in the same directory): Create your virtual environment. -->`python -m venv [name you intend to give your virtual environment]
1. Activate virtual environment. You can activate your virtual environment. --> For CMD -->`env/Scripts/activate.bat` For Powershel --> `env/Scripts/Activate.ps1`
1. You use the refer the documentation in the references below for detailed instructions

## pip installation
1. Refer to the requirements.txt cloned from repository.Check if you have them installed.
1. If not, install all pip dependcies required using requirements.txt using the command --> `pip install -r requirements.txt`
1. you can check pip versions by --> `pip --version`
1. Ensure you have uninterrupted web access as the scripts need to refer to the webpage during execution.

## RUN INSTRUCTIONS
1. Any script you want to execute:
2.   in the command prompt or shell run the command `python {nameofthescript}.py 
3.   if you have all the packages installed the output should be in the working directory
4.   if you are missing any package using the command `pip install (name of missing package)`

## Reference
1. Python installation - [https://www.python.org/downloads/]
1. Pip install - [https://packaging.python.org/en/latest/tutorials/installing-packages/]
1. Python Virtual Environment - [https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/]

