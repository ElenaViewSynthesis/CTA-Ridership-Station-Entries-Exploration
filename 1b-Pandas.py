#!/usr/bin/env python
# coding: utf-8

# # Lecture 1b. Data Exploration Primer
# 
# Here we will explore the basics of Pandas with an example dataset from the Chicago Data Portal at https://data.cityofchicago.org. You should take some time to explore the portal and find your own datasets of interest to explore!
# 
# Recall from the first notebook that you can use the Pandas load_csv function. We've included that here but commented out that line and have loaded a local file instead to allow 

# In[1]:


import pandas as pd

# Use this line as an example to load data directly from the City of Chicago Portal.
# df = pd.read_csv('https://data.cityofchicago.org/api/views/5neh-572f/rows.csv?accessType=DOWNLOAD')

# We have saved the file locally so that you can load the file locally.
df = pd.read_csv('../data/cta-ridership.csv')


# ## Basic Exploration
# 
# Let's first take a quick look at what this data looks like.
# 
# ### What's in the data?

# In[3]:


df.head(5)


# Immediately from looking at this, we can get an understanding of the type of data we're looking at.  There's a station identifier and name, a date on which the statistic takes place, the day type, and the number of rides for that date.
# 
# It's not immediately clear what A/W, is, but looking at the description of the dataset here:
# https://data.cityofchicago.org/Transportation/CTA-Ridership-L-Station-Entries-Daily-Totals/5neh-572f
# 
# tells us that this column indicates that we are looking at a weekday, weekend, or holiday.
# 
# We can then explore some basic characteristics of the data, including the size of the dataset, min/max/etc. to explore outliers, etc. This basic exploration allows us to spot potential outliers and mistakes in the data.
# 
# ### What are some basic statistics about the data?

# In[3]:


df.shape


# In[4]:


df.describe()


# Some basic statistics: There is a station with no rides (minimum is zero!). Also, the station with the maximum number of rides appears to be about 10x the mean and median. Let's have a look at what those stations are.

# In[5]:


df['stationname'].value_counts()


# ### Selection Based on Conditionals

# Let's see which stations have the most and fewest rides, overall, and for particular types of days.

# #### Station with the most rides

# In[6]:


df[df['rides'] == max(df['rides'])].head(1)


# Interesting. The station that had the most number of rides was Belmont-North, on June 28, 2015. **What might have caused that?** (Hint: Do a quick Web search for June 28, 2015 to find out what happened on that date in Chicago.)
# 
# #### Station with the Least Rides

# In[7]:


df[df['rides'] == 0].shape


# Oops! There are 12,209 station-date combinations with zero rides! Let's have a quick look to understand this further.

# In[8]:


zero = df[df['rides'] == 0]
zero.head(5)


# Looks like a lot of weekends and holidays.  We can group by columns and types to get a better understanding of what might be going on. We can count how many dates a station had zero rides in the dataset and sort these in descending order.

# In[9]:


zerogroups = zero.groupby(['stationname','daytype']).count()
zerogroups.sort_values(by=['date'],ascending=False)


# **Note:** It should be clear from a little bit of research why some of the stations at the top of the list report zero dates. Do a little homework on some of them to find out!

# ### Exploring Temporal Patterns

# First, let's figure out the date range that we're dealing with.

# In[10]:


min(df['date'])


# In[11]:


max(df['date'])


# #### Create a Time Index
# 
# So we have all rides from January 1, 2001 to December 31, 2019. Let's do some statistics that group ride statistics by date. First we need to tell Pandas that the date column is in fact a date. So, we convert the column to a proper 'DateTime' type, and then set the index to this column.
# 
# This step takes a little bit of time!

# In[12]:


df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)


# Let's see what this does to our data.  Now we can see that the date column is indexed, but the rows are not sorted.

# In[13]:


df.head(10)


# #### Sort the Dataframe by Date

# In[14]:


# Sort the columns by date
rides_by_date = df.sort_values(by='date')
rides_by_date.head(10)


# #### Sanity Checking
# 
# Looks good!  Now let's have a quick look at data for specific stations: the Garfield station at the Red Line and the Green lines, respectively.

# In[15]:


garfield_red = rides_by_date[rides_by_date['stationname']=='Garfield-Dan Ryan']
garfield_red.head(14)


# In[16]:


garfield_green = rides_by_date[rides_by_date['stationname']=='Garfield-South Elevated']
garfield_green.head(14)


# ## Visualizing Timeseries Data

# In[17]:


import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


sns.set(rc={'figure.figsize':(11, 4)})
garfield_green['rides'].plot(linewidth=0.5)


# In[18]:


garfield_red['rides'].plot(linewidth=0.5)


# Interesting!  You can see a jump in ridership at the Garfield Green Line ridership right at the same time there's a dip in the Garfield Red Line ridership. What happened?  Here's a clue: https://www.transitchicago.com/redsouth/

# Let's now go back and see what happened to the Madison/Wabash station. And why there were so many zero values in the data.

# In[19]:


rides_by_date[rides_by_date['stationname']=='Madison/Wabash']['rides'].plot(linewidth=0.5)


# How do we know whether this is just a glitch in the dataset, or a real event? A little web searching can tell you a bit about this station. https://en.wikipedia.org/wiki/Madison/Wabash_station
# 
# "Madison/Wabash closed on March 16, 2015, after Sunday service in the Loop ceased for the night. The entrances were boarded up by morning-time, and trains started bypassing the station when Monday morning service started."
