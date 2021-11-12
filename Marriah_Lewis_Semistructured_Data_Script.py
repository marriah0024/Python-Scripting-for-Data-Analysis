# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 16:21:59 2021

@author: lewis
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import json 
import matplotlib.pyplot as plt 

#top 1000, United States-English in ascending order from IMDb (1990-2020)
url= 'https://www.imdb.com/search/title/?release_date=1990-01-01,2020-12-31&groups=top_1000&countries=us&languages=en&my_ratings=exclude&count=100'
response= requests.get(url)
    #print(response.text[:500])
soup=BeautifulSoup(response.text, 'html.parser')
    #print(type(soup))
movie_containers= soup.find_all('div', class_='lister-item mode-advanced')#Select all the 100 movie containers from a single page 
# print(type(movie_containers))
#print(len(movie_containers))  
#print(soup.find_all('div'))

first_movie= movie_containers[0]
#print(first_movie.h3.a.text) # access the text from with the tag 
#List to store the scraped data in 
title= []
years= []
imdb_ratings= []
metascores= []
votes=[]
#Extract data from movie container
for container in movie_containers:
    if container.find('div', class_= 'ratings-metascore') is not None:
        name= container.h3.a.text
        title.append(name)
        #the year 
        year= container.h3.find('span', class_='lister-item-year').text
        years.append(year)
        #rating
        imdb= float(container.strong.text)
        imdb_ratings.append(imdb)
        #metascore
        score=container.find('span', class_= 'metascore').text
        metascores.append(int(score))
        #votes
        vote=container.find('span', attrs= {'name': 'nv'})['data-value']
        votes.append(int(vote))


#Test to see if the data collected was scraped successfully 
movie_df= pd.DataFrame({'titles': title,
                        'year': years,
                        'imdb': imdb_ratings,
                        'metascore': metascores,
                        'votes': votes}) 
movie_df['year'].unique() #Avoid Value Errors; converting all values in the year to intergers 
#print(movie_df.info()) #100 entries as expected and no null values
movie_df.loc[:, 'year'] = movie_df['year'].str[-5:-1].astype(int)
#print(movie_df['year'].head(3))
#print(movie_df.describe().loc[['min', 'max'], ['imdb', 'metascore']])
movie_df['n_imdb'] = movie_df['imdb'] * 10 # multiple the imdb score by 10 to help with normalization 
#print(movie_df.head(3))

#Save the df as a json file 
movie_df.to_json (r'C:\Users\lewis\OneDrive\Desktop\Export_DataFrame.json')


#Throwing off JSON format; try something different 
# #Function to convert csv to json 
# def make_json(csvFilePath, jsonFilePath):
#     #create a dictionary 
#     data= {}
#     #open csv reader called DictReader
#     with open(csvFilePath, encoding='utf-8') as csvf:
#         csvReader= csv.DictReader(csvf)
#         #convert each row into dictionary
#         for rows in csvReader:
#             key= rows[""]
#             data[key]= rows
#     #open Json writer
#     with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
#         jsonf.write(json.dumps(data, indent=4))
        

#Put JSON into a df; in order to make sure my json file was formmatted correctly I used JSON Formatter 
df = pd.read_json(r'C:/Users/lewis/Downloads/data.json')
print(df)
print(df.info())
#Analyzing JSON Data 
fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (16,4))
plot1, plot2, plot3 = fig.axes
plot1.hist(df['imdb'], bins = 10, range = (0,10)) # bin range = 1
plot1.set_title('IMDB rating')
plot2.hist(df['metascore'], bins = 10, range = (0,100)) # bin range = 10
plot2.set_title('Metascore')
plot3.hist(df['n_imdb'], bins = 10, range = (0,100), histtype = 'step')
plot3.hist(df['metascore'], bins = 10, range = (0,100), histtype = 'step')
plot3.legend(loc = 'upper left')
plot3.set_title('The Normalized Distributions metascore and imdb')
for axmovie in fig.axes:
    axmovie.spines['top'].set_visible(False)
    axmovie.spines['right'].set_visible(False)
plt.show()

