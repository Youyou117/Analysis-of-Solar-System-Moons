#!/usr/bin/env python
# coding: utf-8

# # Analysis of Solar System Moons

# The data for this project is a list of the recognized moons of the planets and of the largest potential dwarf
# planets of the Solar System. Data is available at: https://en.wikipedia.org/wiki/List_of_natural_satellites#List.
# Here we will do some data cleaning and exploration on this dataset.

# ## Background

# The Solar System's planets, and its most likely dwarf planets, are known to be orbited by at least 219 natural satellites, or moons. 19 of them are large enough to be gravitationally rounded; of these, all are covered by a crust of ice except for Earth's Moon and Io. Several of the largest ones are in hydrostatic equilibrium and would therefore be considered dwarf planets or planets if they were in direct orbit around the Sun.
# 
# Moons are classed in two separate categories according to their orbits: regular moons, which have prograde orbits (they orbit in the direction of their planets' rotation) and lie close to the plane of their equators, and irregular moons, whose orbits can be pro- or retrograde (against the direction of their planets' rotation) and often lie at extreme angles to their planets' equators. Irregular moons are probably minor planets that have been captured from surrounding space. Most irregular moons are less than 10 kilometres (6.2 mi) in diameter.
# 
# (All these information are imported from https://en.wikipedia.org/wiki/List_of_natural_satellites#List)

# ## Import the Dataset

# In[478]:


#import the data from website
import pandas as pd
df = pd.read_html('https://en.wikipedia.org/wiki/List_of_natural_satellites#List',match='Image',header=0)[0]
#show first ten raws
df.head(10)


# This is a list of the recognized moons of the planets and of the largest potential dwarf planets of the Solar System, ordered by their official Roman numeral designations. Sidereal period differs from semi-major axis because a moon's speed depends both on the mass of its primary and its distance from it.

# ## Data Cleaning

# ### 1. Rename the columns with clear names

# we want to rename the columns with clear names so that someone unfamiliar with the data
# set would understand the meaning of the column.

# In[448]:


#rename the columns of the dataframe
df.rename(columns={"Parent": "Parent Planet", "Name": "Moon name","Numeral":"Numeric moon name",
                   "Semi-major axis (km)":"Mean distance(km)",
                   "Sidereal period (d) (r = retrograde)":"Orbital period(days)"
                  },inplace=True)
df.head(10)


# ### 2. Delete unnessary columns

# There are two unnessary columns such as "Image" and "Ref(s)" that can be deleted to make the Dataframe clearer to read.

# In[449]:


#delete columns
del df["Image"]
del df["Ref(s)"]
df.head(10)


# ### 3. Reorder the columns 

# We want to reorder the columns in a way that makes the DataFrame easy to read/understand.
# 

# In[450]:


#reorder the columns
column_names = ["Numeric moon name", "Moon name", "Discovery year","Discovered by","Mean radius (km)","Notes","Parent Planet",
                "Mean distance(km)","Orbital period(days)"
                ]

df = df.reindex(columns=column_names)
df.head(10)


# In the new DataFrame, from the first 6 columns we can see some main characteristics of the specific moon, including its names, mean radius, discovery year, the person who discovered it and some important notes. The contents of the last three columns consist of the name of the parent planet around which the moon orbits, mean distance between the moon and the planet(equlas 1/2 of longest diameter of its elliptical orbit path), and the time the moon takes to complete one full orbit around the planet.
# 
# In this way we can first have a more general understaning of the moon itself and then lean more about its orbital condition, which is more logical and easier to understand.

# ### 4. Reset the index

# Set an index for the DataFrame using an appropriate column or set of columns, such that each observation in the data set can be identified.

# In[451]:


#set new hierarchical index
df=df.set_index(keys=['Numeric moon name','Moon name']).sort_index(level=[0,1])
df.head(10)


# Hierarchical indexing in pandas allows us to have multiple index levels on an axis (e.g., row or column). This functionality provides us with the ability to work with higher dimensional data, but also be able to select observations in our data more directly.
# 
# Here I will set "Numeric moon name" as the first level of the index and "Moon name" as the second level of the index since different moons can have the same numeric name. These two columns together serve as the multiple index unique identifier of each specific moon. 

# ### 5. Deal with the time data

# We will reorder the dataset by column "Discovery year" to display the discovered moons from most recent to the past. Then we want to explore the distribution of the number of discovered moons in each year range. To realize it, we have to first convert the data type to numeric.

# In[452]:


#describe year data
df['Discovery year'].describe()


# In order to convert the data type 'object' to 'numeric', we have to first make sure in the column there are no strings that can not be converted into numeric values. From the column we can see there are two strings-"Prehistoric"and "1975/2000". Since their values are uncertain and there are only two of them, I will treat them as outliers and drop them out of the dataset.

# In[453]:


#drop the raws by filtering
df=df[(df['Discovery year'] != 'Prehistoric') & (df['Discovery year']!= '1975/2000')]
df.head()


# In[454]:


#change the data type to numeric
df["Discovery year"] = pd.to_numeric(df["Discovery year"])
#describe the data
df['Discovery year'].describe()


# In[455]:


#sort the dataset
df.sort_values(by="Discovery year",ascending=False,inplace=True)
df.head(10)


# Sometimes, numerical data would benefit from being discretized into range based categories.Here I will discretize "Discovery year" data by grouping them into different time bins in order to explore the distribution of the number of discovered moons in each year range.

# In[456]:


#create time bins
import numpy as np
bins=np.linspace(start=1590,stop=2020,num=11)
bins


# In[457]:


#bin the year values based on previously created bins
df['Year bin']=pd.cut(df['Discovery year'],bins)
df.head(10)


# ### 6.  Learn more about the relative distance 

# The distances between the moon and the orbited planet are different. I am curious about which moon is closer to its parent planet. In other words, I would like to compare the relative distances between the moons and the parent planets. In order to do this, I will rank the values of relative distance and convert numbers into levels.

# In[458]:


#create a new rank column
df["Mean distance rank"]=df['Mean distance(km)'].rank(axis=0,method='min',ascending=True)
del df['Mean distance(km)']
df.head(10)


# After ranking it becomes much easier for us to see which moon is closer to its parent planet and which moon is farther from its parent planet. Higher the rank, bigger the distance between the two bodies.

# ### 7. Change the unit of orbital period from day to year

# From the dataset we can see the number of days for each orbital period is really large and in order to get a better sense of how long it takes for each moon to orbit its own parent planet, I will convert the unit of orbital period from day to year.

# In[459]:


#extract numbers from the columns
df["Orbital period(days)"] = df["Orbital period(days)"].str.extract('(\d+\,?\d+\.?\d+)')


# In[460]:


#delete all commas 
df["Orbital period(days)"] = df["Orbital period(days)"].str.replace(",","")


# In[461]:


#convert data type to float
df["Orbital period(days)"]= df["Orbital period(days)"].astype(float)
df["Orbital period(days)"] .descrie()


# In[462]:


# change the unit of orbital period from day to year
df["Orbital period(yrs)"] = df["Orbital period(days)"]/365
del df["Orbital period(days)"]
df.head()


# In[463]:


#reorder the dataset
#reorder the columns
column_names2 = ["Discovery year","Year bin","Discovered by","Mean radius (km)","Notes","Parent Planet",
                "Mean distance rank","Orbital period(yrs)"
                ]

df = df.reindex(columns=column_names2)
df.head(10)


# ## Data Exploration 

# In this part I want to explore the distribution of the number of discovered moons in each year range.
# 
# Here are some questions to be answered:

# 1. What's the total number of discovered moons in each year range? 

# In[472]:


#count the unique values of discovered moons for each year bin.
df['Year bin'].value_counts()


# In[473]:


#calculate the percentages of discovered moons for each year bin.
df['Year bin'].value_counts()/len(df['Year bin'])


# From the data we can see more than 85% of the moons were discovered from the time period 1977-2020. 
# 
# This might due to the rapid advancement of technologies which support us searching for new moons and the successful production of spaceships which allow people go into the space and explore more of the universe.
# 
# 

# 2. What's the total number of discovered moons whose orbital period is less than 3 years in each year range? 

# In[470]:


# find the discovered moons whose orbital period is less than 3 years
df2=df[df['Orbital period(yrs)']<3]
df2.head(10)


# In[474]:


#count the unique values of discovered moons whose orbital period is less than 3 years for each year bin.
df2['Year bin'].value_counts()


# Comparing to result for the first question, we can see that only the number for year bin (1977.0, 2020.0] decreases by 34 with all the other numbers unchanged. 
# 
# This indicates that most of these discovered moons have orbital period more than 3 years.

# 3. What's the total number of discovered moons whose distrance from the parent planets are among the first 100 shortest in each year range? 

# In[476]:


# find the discovered moons whose distrance from the parent planets are among the first 100 shortest
df3=df[df['Mean distance rank']<100]
df3.head(10)


# In[477]:


#count the unique values of discovered moons whose distrance from the parent planets are among the first 100 shortest.
df3['Year bin'].value_counts()


# Comparing to result for the first question, we can see that the number for year bin (1977.0, 2020.0] decreases more than half of its original number.
# 
# This indicates that comparing to moons which were discovered in the past, the distances between the moons discovered in the last half century and their parent planets are shorter.

# ## Data Visulization

# Here I want to plot a bar graph which displays the different number of discovered moons in each year range.

# In[281]:


#plot the bar graph
import matplotlib.pyplot as plt
import seaborn as sns

ax = df['Year bin'].value_counts().plot(kind='barh', rot=0)                                  
ax.set_title("Count of discovered moons for each year bin", fontsize=16)
ax.set_xlabel("Number of discovered moons", fontsize=16)
ax.set_ylabel("Year range", fontsize=16)


# set individual bar lables using above list
for i in ax.patches:
    ax.text(i.get_width()+.1, i.get_y()+.31,             str(round((i.get_width()), 2)), fontsize=14, color='dimgrey')


# From the bar chart we can see most of the moons were discovered from the time period 1977-2020, which supports the results found above.
