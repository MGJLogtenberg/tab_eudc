#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Import packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[123]:


def scorefinder(url):
    response = requests.get(url) #Get access to URL
    soup = BeautifulSoup(response.text, "html.parser")
    if str(response) == '<Response [404]>': #If page does not exist, return NaNs
        return np.nan, np.nan, np.nan

    for idx, i in enumerate(soup.findAll('small')): #For each page, find all small text on the page
        r1 = re.findall(r"\d",str(i))[-3:] #Find numbers constituting room number
        roundn = re.findall(r"\d",str(i))[0] #Find round number

        room = ''
        for j in r1: #Append room numbers together
            room += j

    scores = []
    for idx, i in enumerate(soup.findAll('li')): #For each overview page, find all scores on page

        #Score sheets
        if idx in [10,13,16,19]: #Locations of total team score for that round
            r2 = re.findall(r"\d",str(i))[:-1] #Find numbers (Exclude last bc decimal)
            n = ''
            for j in r2: #Append to string
                n += j
            scores.append(n) #Append string to scores
            
    return roundn, room, scores #Return all


# In[124]:


rounds = {} #Initiate dicts
rooms = {}
scoress = {}

for debate in range(1,530): #Iterate through all inrounds
    l = list(scorefinder('https://eudc2023.calicotab.com/_/results/debate/'+str(debate)+'/scoresheets/')) #Find scores
    rounds[debate] = l[0] #Append to dicts
    rooms[debate] = l[1]
    scoress[debate] = l[2]
    if debate % 50 == 0: #Print updates
        print('Debates processed:',debate)


# In[161]:


df = pd.DataFrame.from_dict(scoress).T
df.columns = ['OG','OO','CG','CO']
df['Round'] = rounds.values()
df['Room'] = rooms.values()
df.dropna(inplace=True)
df = df.astype('int32')
df.reset_index(inplace=True)


# In[174]:


df.drop(df[df['Room'] < 100].index, inplace = True)
floor = {}
for idx,i in enumerate(df['Room']):
    floor[idx] = str(i)[0]
    
df['Floor'] = floor.values()


# In[224]:


avgs = {}
for i in df.T:
    avgs[i] = (df.loc[i,'OG'] + df.loc[i,'OO'] + df.loc[i,'CG'] + df.loc[i,'CO']) / 4
df['Average Teampoints'] = avgs.values()


# In[ ]:


avgs = {}
for i in df.T:
    avgs[i] = (df.loc[i,'CG'] + df.loc[i,'CO']) / 2
df['Closing Teampoints'] = avgs.values()


# In[ ]:


df['Round_day'] = (df['Round'] % 3)
df['Round_day'].replace(0,3,inplace=True)


# In[237]:


df.to_excel('EUDC_tab.xlsx')


# In[3]:


df = pd.read_excel('EUDC_tab.xlsx',index_col=0)
sns.barplot(data=df, x="Floor", y="Average Teampoints", order=[1,2,3,4])
plt.ylim(145, 162)


# In[5]:


sns.barplot(data=df, x= 'Round_day', y="Average Teampoints")
plt.ylim(140, 157)

