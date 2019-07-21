# Import all the relevant libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from time import time
from IPython.core.display import clear_output # To Clear out the display
import requests #For Downloading the images
import os

# Creata a function to get the list of all top 250 films
def get_film_list():
	
	# Create the driver
	driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

	# Hyperlink of top 250 websites
	url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'

	driver.get(url)

	# Get the html code
	soup = BeautifulSoup(driver.page_source, 'lxml')

	table = soup.find('table', class_  = 'chart')

	film_rank = []
	film_title = []
	film_year = []
	film_link  = []

	#Monitoring of loop
	start_time = time()
	request = 0

	for td in table.find_all('td', class_ = 'titleColumn'):
		request += 1
		elapsed_time = time() - start_time
		print('Request:{}; Frequency: {} requests/s'.format(request, request/elapsed_time))
		clear_output(wait = True)

		full_title =  td.text.strip().replace('\n','').replace('      ', '')
		print(full_title)

		rank = full_title.split('.')[0]
		# print(rank)
		film_rank.append(rank)

		title = full_title.split('.')[1].split('(')[0]
		# print(title)
		film_title.append(title)

		year = full_title.split('(')[1][:-1]
		# print(year)
		film_year.append(year)

		link = 'https://www.imdb.com' + td.find('a')['href']
		# print(link)
		film_link.append(link)

	driver.quit()

    # Creating a dataframe of films list
	film_list = pd.DataFrame({'Rank': film_rank,
							 'Title': film_title,
							  'Year': film_year,
							  'Link':film_link})

	return film_list

# Calling the function to get the data frame of top 250 films
film_list = get_film_list()

print(film_list)

#Storing it as csv file
film_list.to_csv('film_list.csv')
                    
# Function to download the posters of all the films
def download_all_posters(film_list):

    driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

    # Create directory if not exisits
    if not os.path.exists('movies_images'):
        os.makedirs('movies_images') 

    for index, row in film_list.iterrows():

        url = row['Link']
        print(url)        

        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'lxml')

        div = soup.find('div', class_ = 'poster')

        a = div.find('a')

        url  = 'https://www.imdb.com' + a['href']

        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'lxml')

        all_div = soup.find_all('div', class_= 'pswp__zoom-wrap')

        all_img = all_div[1].find_all('img')

        #print (all_img[1]['src'])
        f = open('movies_images\{0}.jpg'.format(row['Title'].replace(':','')), 'wb')
        f.write(requests.get((all_img[1]['src'])).content)
        f.close()

    driver.quit()

download_all_posters(film_list)
