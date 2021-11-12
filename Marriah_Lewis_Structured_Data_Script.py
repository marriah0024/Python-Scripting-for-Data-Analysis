# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 20:44:27 2021

@author: lewis
"""

#Import libraries; using pandas for dataframes and matplot lib for graphs 

import pandas as pd 
from matplotlib import pyplot as plt 
import matplotlib.gridspec as gridspec

donors= pd.read_csv('C:/Users/lewis/OneDrive/Documents/data/donors_data .csv')
#print(donors)
#Show the top five rows 
print(donors.head())
#Provide a summary of stats pertaining to the df
print(donors.describe())

#Clean the df 
donors_clean= pd.concat([donors['homeowner dummy'],
                         donors['NUMCHLD'], 
                         donors['INCOME'],
                         donors['gender dummy'], 
                         donors['WEALTH'],
                         donors['HV'],
                         donors['Icmed'],
                         donors['Icavg'],
                         donors['IC15'],
                         donors['NUMPROM'],
                         donors['RAMNTALL'],
                         donors['MAXRAMNT'],
                         donors['LASTGIFT'],
                         donors['totalmonths'],
                         donors['TIMELAG'], 
                         donors['AVGGIFT']
                         ],
                        axis=1, 
                        keys=['homeowner',
                              'numchildren',
                              'income_d',
                              'gender',
                              'wealth_d',
                              'homevalue',
                              'income_med',
                              'income_avg',
                              'lowincome_perc',
                              'numpromos', 
                              'donations_total',
                              'donations_max',
                              'donations_last',
                              'donations_months_since_last',
                              'donations_months_between_first_second',
                              'donations_avg'])
print(donors_clean)
print(donors_clean.describe())

#Question 1: Does the amount of promotions determine the amount donated  
plt.plot(donors_clean.numpromos, donors_clean.donations_total,'o')
plt.title('Promotions vs Amount of Donations')
plt.xlabel('Promotions')
plt.ylabel('Total Donation Amount')
plt.show()

#there is an outlier, why is the outlier so huge; time to test 
#test= donors_clean[donors_clean.donations_total< 2500] #based on the plot only adding items to the df if the donation total is less than 2500
#creating a visual to re-examine
#plt.plot(test.donations_total)
#still some huge outliers; 1500 seems like a nice median 
test= donors_clean[donors_clean.donations_total<= 1500]
#Created a boxplot visual to provide more clarity
#plt.boxplot(test.donations_total)
#plt.show
print(test.count())

#reassigning variable 
donors_clean= test
#print(donors_clean.count())

#Continuing with Question 1 
plt.plot(donors_clean.numpromos, donors_clean.donations_total, 'o')
plt.title('Number of Promo vs Amount of Donations')
plt.xlabel('Promo')
plt.ylabel('Total amount of Donations')
plt.show()

#Question 2: Does the number of promotions sent determine the frequency of donations?
donation_frequency= donors_clean.donations_total/donors_clean.donations_avg
#plot promotions vs frequency 
plt.plot(donors_clean.numpromos, donation_frequency,'o')
plt.title('Number of Promotions vs Frequency')
plt.xlabel('Promo')
plt.ylabel('Donation Freq.')
plt.show()

#Question 3: Does the number of children impact the number of donations 
plt.plot(donors_clean.donations_total, donors_clean.numchildren, 'o')
plt.title('Amount of donations vs Number of Children')
plt.xlabel('Amount of donations')
plt.ylabel('Number of children') 
plt.show()

#Question 4: Does the number of promotions sent impact the time since the last donation 
plt.plot(donors_clean.numpromos, donors_clean.donations_months_since_last, 'o')
plt.title('Number of Promotions vs Time since Donation')
plt.xlabel('Promo')
plt.ylabel('Months since last donation')
plt.show()



