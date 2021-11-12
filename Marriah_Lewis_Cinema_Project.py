# -*- coding: utf-8 -*-
"""
Created on Thu Sep 9 18:52:17 2021

@author: lewis
"""

import csv 
import pandas as pd 
import re 
import statistics
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen


#Creating a function that groups by, counts, creates a new column from the index, drops the index and changes the column names
def groupby_count(df, groupby_column, count_column): 
    new_df = pd.DataFrame(df.groupby(groupby_column)[count_column].count())
    new_df.columns = ['count']
    new_df[groupby_column] = new_df.index.get_level_values(0)
    new_df.reset_index(drop = True, inplace = True)
    return(new_df)



url = 'https://en.wikipedia.org/wiki/Film_series'
html = urlopen(url) 
soup = BeautifulSoup(html, 'html.parser')
tables = soup.find_all('table')

#Create a function to process the string into an integer by using re.sub()
def process_num(num):
    return float(re.sub(r'[^\w\s.]','',num))
#test function
num1 = float(re.sub(r'[^\w\s.]','','1,156.30'))
#print(num1)

#Create array to hold the data extracted
gross=[]
year=[]
film=[]

for table in tables:
    rows = table.find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')
        
        if len(cells) > 1:
            Franchise = cells[1]
            film.append(Franchise.text.strip())
            
            Gross = cells[6]
            gross.append(process_num(Gross.text.strip()))    
            
            first = cells[7]
            year.append(int(first.text))
            
# put the data in the pandas dataframe 
movie_df= pd.DataFrame({'Gross': gross,
                        'first': year,
                        'Franchise': film
                        }) 
#print(movie_df) 
#print(movie_df.dtypes)
#movies_df_count = movie_df.groupby(["Franchise", "first"])["first"].count()         
#print(movies_df_count)

#WIKI_df=movie_df.groupby(["first"])["first"].count()  
#print(WIKI_df)
#WIKI_df.plot(kind='bar',x='first',y='count')
#plt.title("Most Movies Release count by Year(Top 68 on WIKI)",fontsize=20)

#TMDB Kaggle Data 
movies_TMDB_kaggle= pd.read_csv(r'C:/Users/lewis/OneDrive/Documents/MovieData/tmdb_5000_movies.csv', encoding= 'ISO-8859-1')
#print(len(movies_TMDB_kaggle)) #result 4803 and 20 columns 
#print(movies_TMDB_kaggle.isnull().sum()) #tagline and homepage has the most NaN, unnecessary columns

#Clean the dataframe, removed any unnecessary columns  
clean_TMDB_movies= movies_TMDB_kaggle.drop(columns=['homepage', 'id', 'overview', 'status', 'tagline', 'original_title'])
#print(clean_TMDB_movies) #result 4803 rows and 14 columns 
#print(clean_TMDB_movies.isnull().sum()) # NaNs in the release_date and runtime column
clean_TMDB_movies.dropna(inplace= True)
#print(clean_TMDB_movies.isnull().sum())

#Removing any movie that has a budget of 0 
clean_TMDB_movies = clean_TMDB_movies[clean_TMDB_movies['budget'] != 0]
#Removing any movie with a revenue of 0 
clean_TMDB_movies = clean_TMDB_movies[clean_TMDB_movies['revenue'] != 0]
#review the profit for each movie therefore a profit column was created 
clean_TMDB_movies['profit'] = clean_TMDB_movies['revenue'] - clean_TMDB_movies['budget']
#Creating a percent profit column  in order to compare profits. 
clean_TMDB_movies['percent_profit'] = clean_TMDB_movies['profit']/clean_TMDB_movies['budget']*100
#print the top five 
#print(clean_TMDB_movies.head())

#checking the data types 
#print(clean_TMDB_movies.dtypes)

#change release_date to the date/time and separate it by month, day, and year
clean_TMDB_movies['release_date'] = pd.to_datetime(clean_TMDB_movies['release_date'])
clean_TMDB_movies['month'], clean_TMDB_movies['day'] = clean_TMDB_movies['release_date'].dt.month, clean_TMDB_movies['release_date'].dt.day
#After new columns were added it is time to concat. 
cat = list(range(1,13))
#Changing the month data type from int to ordered category 
clean_TMDB_movies['month'] = pd.Categorical(clean_TMDB_movies['month'], ordered = True, categories = cat)
#confirmation
#print(clean_TMDB_movies.month.dtype)
#print(len(clean_TMDB_movies))
#print(clean_TMDB_movies.describe())
#print(clean_TMDB_movies.revenue.describe())
#print(clean_TMDB_movies.profit.describe())
#print(clean_TMDB_movies.vote_count.describe())
#print(clean_TMDB_movies.percent_profit.describe())

#discretize the budget column
categories = ["very_low", "low", "high", "very_high"]
#saving the clean_TMDB df as a discretized df 
movies_discretized = clean_TMDB_movies 
#creating a budget cutoff using pandas cut function 
movies_discretized["budget"] = pd.cut(movies_discretized["budget"], [0, 13000000, 30000000, 62192550, 400000000], labels = categories)
#repeat the step for revenue 
#print(movies_discretized.revenue.describe())
movies_discretized["revenue"] = pd.cut(movies_discretized["revenue"], [0, 21458200, 62954020, 187976900, 2887965000], labels = categories)

#profit
categories_profit = ["negative", "low", "high", "very_high"]
movies_discretized["profit"] = pd.cut(movies_discretized["profit"], [-165710100 , 0, 29314900, 140784100, 2560965000], labels = categories_profit)
#print(movies_discretized["profit"].head())

#Vote_average-very_low: vote averages less than 6, low are between 6 to 6.5, high between 6.5 and 7 and very_high 7 and 8.5
movies_discretized["vote_average"] = pd.cut(movies_discretized["vote_average"], [0, 6, 6.5, 7, 8.5], labels = categories)
#print(movies_discretized["vote_average"].head())

#Vote_count 
movies_discretized["vote_count"] = pd.cut(movies_discretized["vote_count"], [0, 440, 1151, 2522, 14000], labels = categories)
#print(movies_discretized["vote_count"].head())

#percent_profit 
movies_discretized["percent_profit"] = pd.cut(movies_discretized["percent_profit"], [-100, 0, 108, 436, 6528], labels = categories_profit)
movies_discretized["percent_profit"]

#Categorizing days into weeks 
#print(movies_discretized.day.describe())
categories_weeks = ["week_1", "week_2", "week_3", "week_4"]

movies_discretized["week"] = pd.cut(movies_discretized["day"], [0, 8, 15, 22, 32], labels = categories_weeks)
#print(movies_discretized["week"].head())

#day and release_date are no longer needed columns 
movies_discretized.drop(columns=['day', 'release_date'], inplace = True)
#print(movies_discretized.head())

#Do major production companies have an impact the profit margin? 
production_company = []
for movie in movies_discretized['production_companies']:
    if "Universal" in movie:
        production_company.append("Universal")
    elif "Sony" in movie: 
        production_company.append("Sony")
    elif "Fox" in movie: 
        production_company.append("Fox")
    elif "DreamWorks" in movie: 
        production_company.append("DW")
    elif "MGM" in movie: 
        production_company.append("MGM")
    elif "Paramount" in movie: 
        production_company.append("Paramount")
    elif "Disney" in movie: 
        production_company.append("Disney")
    elif "Warner Bros" in movie:
        production_company.append("WB")
    else:
        production_company.append("None")

movies_discretized["main_production"] = production_company
#print(movies_discretized["main_production"].head())
movies_discretized_count = movies_discretized.groupby(["main_production", "percent_profit"])["main_production"].count()
movies_discretized_count_df= pd.DataFrame(movies_discretized_count)
#print(movies_discretized_count_df)
#change the last column to count instead of main production 
movies_discretized_count_df.columns = ["counts"]
#print(movies_discretized_count_df.head())

#total count for the number of percent_profit counts for each main production.
movies_discretized_count_df["production_company"]=movies_discretized_count_df.index.get_level_values(0)
movies_discretized_count_df["percent_profit_category"] = movies_discretized_count_df.index.get_level_values(1)
#print(movies_discretized_count_df)

#drop the indexes to create another column with the sum of the counts of each production 
movies_discretized_count_df = movies_discretized_count_df.reset_index(drop = True)
#The sum of each production company category. 
production_company_discretized_count_df = movies_discretized_count_df.groupby(["production_company"])["counts"].sum()
#print(production_company_discretized_count_df)

#column with the overall counts for each production, construct a new column called production company count that replicates the production company, and then use the replace function to replace the 1s and 2s with the total count
movies_discretized_count_df["production_company_count"] = movies_discretized_count_df["production_company"] 
#Now replacing the income level with the total count for each income level 
movies_discretized_count_df["production_company_count"] = movies_discretized_count_df["production_company_count"].replace(["DW"], 82)
movies_discretized_count_df["production_company_count"] = movies_discretized_count_df["production_company_count"].replace(["Disney"], 116)
movies_discretized_count_df["production_company_count"] = movies_discretized_count_df["production_company_count"].replace(["Fox"], 298)
movies_discretized_count_df["production_company_count"] = movies_discretized_count_df["production_company_count"].replace(["MGM"], 87)
movies_discretized_count_df["production_company_count"] = movies_discretized_count_df["production_company_count"].replace(["None"], 1782)
movies_discretized_count_df["production_company_count"] = movies_discretized_count_df["production_company_count"].replace(["Paramount"], 235)
movies_discretized_count_df["production_company_count"] = movies_discretized_count_df["production_company_count"].replace(["Sony"], 42)
movies_discretized_count_df["production_company_count"] = movies_discretized_count_df["production_company_count"].replace(["Universal"], 282)
movies_discretized_count_df["production_company_count"] = movies_discretized_count_df["production_company_count"].replace(["WB"], 269)
#print(movies_discretized_count_df)

#percentage 
movies_discretized_count_df["percent"] = movies_discretized_count_df["counts"]/movies_discretized_count_df["production_company_count"] *100
#print(movies_discretized_count_df.head())
#dropping production_company_count and count column no longer needed 
movies_discretized_count_df.drop(["counts", "production_company_count"], axis = 1, inplace = True ) 

#graphing question 1 using Matplot lib
#graph = movies_discretized_count_df.pivot("production_company", "percent_profit_category","percent").plot(kind="bar", color= ['blue', 'green', 'purple', 'red'], title='Profit Margin amongst Production Companies') 
#change the x and y axis for graph
#plt.ylabel("Percent Profit")
#plt.xlabel("Production")
#plt.xticks(rotation = 0)
#position the legends underneath the graph; Now the graph looks beautiful
#plt.legend( loc = "lower center", bbox_to_anchor = (.5, -.4), ncol = 4, title = "Percent Profit Category")
#plt.show()

#Question 2: Is it true that the month in which a film is released has an impact on its profit margin?
movies_discretized_count_week = movies_discretized.groupby(["week", "percent_profit"])["week"].count()
movies_discretized_count_df_week = pd.DataFrame(movies_discretized_count_week)
#Checking the dataframe 
#print(movies_discretized_count_df_week)

#changing column that is labeled week to count 
movies_discretized_count_df_week.columns = ["counts"]
#total count for the number of % profit for each week   
movies_discretized_count_df_week["week"]=movies_discretized_count_df_week.index.get_level_values(0)
movies_discretized_count_df_week["percent_profit_category"] = movies_discretized_count_df_week.index.get_level_values(1)
#print(movies_discretized_count_df_week)
movies_discretized_count_df_week = movies_discretized_count_df_week.reset_index(drop = True) #drop the index
#what is the sum of each production 
sum_discretized_count_df_week = movies_discretized_count_df_week.groupby(["week"])["counts"].sum()
#print(sum_discretized_count_df_week) #the sums are centered around 700-800s 
movies_discretized_count_df_week["week_count"] = movies_discretized_count_df_week["week"] 
#Now replacing the income level with the total count for each income level 
movies_discretized_count_df_week["week_count"] = movies_discretized_count_df_week["week_count"].replace(["week_1"], 783)
movies_discretized_count_df_week["week_count"] = movies_discretized_count_df_week["week_count"].replace(["week_2"], 817)
movies_discretized_count_df_week["week_count"] = movies_discretized_count_df_week["week_count"].replace(["week_3"], 782)
movies_discretized_count_df_week["week_count"] = movies_discretized_count_df_week["week_count"].replace(["week_4"], 811)
#print(movies_discretized_count_df_week.head())

#received an error Object with dtype category cannot perform the numpy op true_divide
movies_discretized_count_df_week["week_count"]= movies_discretized_count_df_week["week_count"].astype(np.int64) 
#convert into percentage; counts/week_count * 100 
movies_discretized_count_df_week["percent"] = movies_discretized_count_df_week["counts"]/movies_discretized_count_df_week["week_count"] *100
#print(movies_discretized_count_df_week.head()) 

#dropping the week_count and count column since the percent column is there those columns are no longer needed  
movies_discretized_count_df_week.drop(["counts", "week_count"], axis = 1, inplace = True ) 
#Time to create a visual 
#graph_question_2 = movies_discretized_count_df_week.pivot("week", "percent_profit_category", "percent").plot(kind="bar", color = ["blue", "green", "purple", "red"], title = "Impact of Percent Profit by Week")
#plt.ylabel("Percent")
#plt.xlabel("Week")
#plt.xticks(rotation = 0)
#plt.legend( loc = "lower center", bbox_to_anchor = (.5, -.4), ncol = 4, title = "Percent Profit")
#plt.show()


#IMDb Kaggle Data 
movies_IMDb= pd.read_csv(r'C:/Users/lewis/OneDrive/Documents/MovieData/IMDb_movies.csv')
clean_IMDb= movies_IMDb.drop(columns=['imdb_title_id','original_title','description', 'reviews_from_users', 'reviews_from_critics'])
#print(clean_IMDb) #85,855 rows and 17 columns 
#print(clean_IMDb.isnull().sum())
clean_IMDb.dropna(inplace = True) #drop all the NaNs 
#print(clean_IMDb.isnull().sum()) #no more NaNs
#print(len(clean_IMDb)) #6635
#print(clean_IMDb.dtypes)

# QUESTION 3: How does budget impact vote average?
#plt.plot(clean_IMDb.budget, clean_IMDb.avg_vote, 'o')
#plt.title('How does Budget Impact Vote Average?')
#plt.xlabel('Budget')
#plt.ylabel('Vote Average')
#plt.show()

#print(clean_IMDb['budget'].head())

#print the top five 
#print(clean_IMDb.head())

#Using the groupby_count function that takes the following arguments (df, groupby_column, count_column)
IMDb_movies_genre = groupby_count(clean_IMDb, 'genre', 'genre')
#Sorting the df, so the bar graph will be in descending order
IMDb_movies_genre.sort_values(['count'], ascending=[False], inplace = True)



#Statista movie theatre revenue and prediction to 2025 post COVID saving to a pd dataframe
revenue_covid= pd.read_csv(r'C:/Users/lewis/OneDrive/Documents/MovieData/revenue_covid_impact.csv')
print(revenue_covid)
AMC_revenue= pd.read_csv(r'C:/Users/lewis/OneDrive/Documents/MovieData/AMC.csv')
#print(AMC_revenue)
#print(AMC_revenue.info())
print(AMC_revenue.head())

#During 2020, AMC Theatres reported annual revenues of 1.24 billion U.S. dollars, a dramatic decrease from previous years as a consequence of the COVID-19 pandemic.
plt.plot(AMC_revenue.Year, AMC_revenue.Money, 'o')
plt.title('AMC revenue over 15 years')
plt.xlabel('Year')
plt.ylabel('Revenue')
plt.show()

#Global box office revenue coronavirus impact 2020-2025
#revenue_covid.plot(x="Year", y=["Originalforecast", "Marchrevision", "Julyrevision"], kind="bar")
#plt.show()

