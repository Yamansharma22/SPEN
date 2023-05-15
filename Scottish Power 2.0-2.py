#!/usr/bin/env python
# coding: utf-8

# # Python Session starts 

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

    
df = pd.read_csv('/Users/yamansharma/Downloads/Spen/london.csv')


# In[2]:



# Data Types 
print(df.dtypes) 
display(df)


# In[3]:


# Renaming for better understanding 
df = df.rename(columns={'downo': 'D_O_W','daytype': 'Day','SubSystem': 'T_System','StartStn': 'Start_Stn','EndStation': 'End_Stn','EntTime':'Ent_Time', 'ExTime': 'Ex_Time','ZVPPT' :'Zone', 'JNYTYP': 'JNY_TYP','FFare': 'Full_Fare', 'DFare': 'D_Fare', 'RouteID':'Route_ID', 'FinalProduct':'Mode_of_Pay', })
df.head() 


# In[4]:


# Check for null values
print(df.isnull().sum())

# Get the statistical summary of the data

print(df.describe())     


# In[5]:


# Checking the counts for each variables 
Day_count = df['D_O_W'].nunique()
Start_Stn_count = df['Start_Stn'].nunique()
End_Stn_count = df['End_Stn'].nunique()
T_System_count = df['T_System'].nunique()
Zone_count = df['Zone'].nunique()
Route_ID_count = df['Route_ID'].nunique()
Mode_of_Pay_count = df['Mode_of_Pay'].nunique()

# Print the unique counts
print("Unique values in Day:", Day_count)
print("Unique values in Start_Stn:", Start_Stn_count)
print("Unique values in End_Stn:", End_Stn_count)
print("Unique values in T_System:", T_System_count)
print("Unique values in Zone:", Zone_count)
print("Unique values in Route_ID:", Route_ID_count)
print("Unique values in Mode_of_Pay:", Mode_of_Pay_count)


# In[6]:


# Printing the Value counts for each variable
day_counts = df['Day'].value_counts()
print(day_counts)

T_System_counts = df['T_System'].value_counts()
print(T_System_counts)

Start_Stn_counts = df['Start_Stn'].value_counts()
print(Start_Stn_counts)

End_Stn_counts = df['End_Stn'].value_counts()
print(End_Stn_counts)

EntTimeHHMM_counts = df['EntTimeHHMM'].value_counts()
print(EntTimeHHMM_counts)

EXTimeHHMM_counts = df['EXTimeHHMM'].value_counts()
print(EXTimeHHMM_counts)

Zone_counts = df['Zone'].value_counts()
print(Zone_counts)

JNY_TYP_counts = df['JNY_TYP'].value_counts()
print(JNY_TYP_counts)

Route_ID_counts = df['Route_ID'].value_counts()
print(Route_ID_counts) 

Mode_of_Pay_counts = df['Mode_of_Pay'].value_counts()

print(Mode_of_Pay_counts)


# # Completed Journeys

# In[7]:


# Print top 10 Start and End Stations 
top_start_stations = df['Start_Stn'].value_counts().head(10)
print(top_start_stations) 
top_end_stations = df['End_Stn'].value_counts().head(10)
print(top_end_stations)   


# In[8]:


# Dropping unwanted Start and End Stations and Sations where Start and End are same

df = df[~df['Start_Stn'].isin(['Bus', 'Unstarted'])] 

df = df[df['Start_Stn'] != df['End_Stn']]

df = df[~df['End_Stn'].isin(['Bus', 'Unfinished', 'Not Applicable'])]


top10_start = df['Start_Stn'].value_counts().head(10) 

top10_end = df['End_Stn'].value_counts().head(10)

# Get the top 10 Start and End Stations

print(top10_start) 
print(top10_end)


unique_count = df['Start_Stn'].nunique()
unique_count1 = df['End_Stn'].nunique()
print("Number of unique values in Start Station:", unique_count)
print("Number of unique values in End Station:", unique_count1)


# # Feature engineering
# 
# create a new category called "JourneyTime", which is the total journey time in minutes, as the difference between "ExTime" and "EntT

# In[9]:


# To create a Journey Time 

df['JourneyTime'] = ((df['Ex_Time']) - (df['Ent_Time']))

print(df['JourneyTime']) 

top20_starttime = df['EntTimeHHMM'].value_counts().head(20)
top20_endtime = df['EXTimeHHMM'].value_counts().head(20)

print(top20_starttime)
print(top20_endtime)


# In[10]:


display(df)

 


# In[11]:


df[[ 'Full_Fare', 'D_Fare', 'JourneyTime']].describe()


# # Step - 2 EDA

# In[12]:


# create a new column with the combination of start and end stations
df['Route'] = df['Start_Stn'] + ' to ' + df['End_Stn']

# group the data by the new column and count the number of occurrences
route_counts = df.groupby('Route').size().reset_index(name='Counts')

# sort the data in descending order and take the top 10 routes
top_routes = route_counts.sort_values(by='Counts', ascending=False).head(10)

# plot the bar graph
plt.bar(top_routes['Route'], top_routes['Counts'])
plt.xticks(rotation=90)
plt.xlabel('Route')
plt.ylabel('Number of journeys')
plt.title('Top 10 Start-End Station Routes')
plt.show()


# In[13]:



# Bar Plot for the Total Journeys on Weekdays and Weekends 
df['is_weekend'] = df['Day'].apply(lambda x: 'Weekend' if x in ['Sat', 'Sun'] else 'Weekday')

total_journeys = len(df)

journeys_weekday = len(df[df['is_weekend'] == 'Weekday'])
journeys_weekend = len(df[df['is_weekend'] == 'Weekend'])

percent_weekday = (journeys_weekday / total_journeys) * 100
percent_weekend = (journeys_weekend / total_journeys) * 100

sns.barplot(x=['Weekday', 'Weekend'], y=[percent_weekday, percent_weekend])
plt.xlabel('Day')
plt.ylabel('Percentage of Journeys')
plt.title('Percentage of Journeys Taken on Weekdays vs Weekends')
plt.show()

day_counts = df['Day'].value_counts()
day_counts.plot(kind='bar')
plt.xlabel('Day')
plt.ylabel('Totals Journeys')
plt.title('Journeys Taken through Week')
plt.show()


# In[14]:


# count the frequency of each Zone code
df['Zone'] = df['Zone'].replace('-------', 'X')
zv_counts = df['Zone'].value_counts()

# create a bar plot of the counts
plt.figure(figsize=(12, 6))
sns.barplot(x=zv_counts.index, y=zv_counts.values)
plt.title('Frequency of Zone Codes')
plt.xlabel('Zone Code')
plt.ylabel('Frequency')
plt.show()

# Removing the 1st ----- value 
# get value counts of ZVPPT
Zone_counts = df['Zone'].value_counts()

# remove the most common ZVPPT
Zone_counts = Zone_counts[1:]

# create a barplot
sns.barplot(x=Zone_counts.index, y=Zone_counts.values)

# set x-axis labels to 45 degrees
plt.xticks(rotation=45)

# show the plot
plt.show()


# In[ ]:





# In[ ]:





# In[15]:


# Group data by start station and count the number of occurrences
start_stations = df.groupby('Start_Stn')['Start_Stn'].count().sort_values(ascending=False)

# Select the top 10 start stations
top_start_stations = start_stations[:10]

# Plot the bar graph
plt.figure(figsize=(12,6))
sns.barplot(x=top_start_stations.values, y=top_start_stations.index, palette='viridis')
plt.title('Top 10 Most Popular Start Stations')
plt.xlabel('Number of Occurrences')
plt.ylabel('Start Station')
plt.show()


# In[16]:


# Get the top 10 most popular end stations
top_end_stations = df['End_Stn'].value_counts().nlargest(10)

# Create a bar plot of the top end stations
plt.figure(figsize=(10,6))
sns.barplot(y=top_end_stations.index, x=top_end_stations.values, palette='viridis')
plt.title('Top 10 Most Popular End Stations')
plt.xlabel('Number of Journeys')
plt.ylabel('End Station')
plt.xticks(rotation=0)
plt.show()


# In[17]:



# Create the histogram
ax = sns.histplot(data=df, x='JourneyTime', bins=50)


average = df['JourneyTime'].mean()
print(average)
ax.axvline(x=average, color='red', linestyle='--')

plt.show()


# In[18]:


# Count the number of occurrences for each T_system
ts_counts = df['T_System'].value_counts()

# Calculate percentages
ts_percents = (ts_counts / ts_counts.sum()) * 100

# Create a horizontal bar chart
plt.figure(figsize=(8, 5))
sns.barplot(x=ts_percents.values, y=ts_percents.index, color='steelblue')

# Add chart title and axis labels
plt.title('Distribution of T_system')
plt.xlabel('Percentage')
plt.ylabel('T_system')
plt.show()


# In[19]:


# To optimise the resources we can allocate them from Least popular stations to most popular stations

# Get the counts of each station
start_station_counts = df['Start_Stn'].value_counts()
end_station_counts = df['End_Stn'].value_counts()

# Add the counts together and get the top 10 stations
top_station_counts = start_station_counts.add(end_station_counts, fill_value=0).nlargest(10)

# Get the least 10 stations
bottom_station_counts = start_station_counts.add(end_station_counts, fill_value=0).nsmallest(10)

# Create a horizontal bar chart for the top 10 stations
plt.subplot(1,2,1)
sns.barplot(x=top_station_counts.values, y=top_station_counts.index, color='steelblue')
plt.title('Most Popular Stations')
plt.xlabel('Count')
plt.ylabel('Station')

# Create a horizontal bar chart for the least 10 stations
plt.subplot(1,2,2)
sns.barplot(x=bottom_station_counts.values, y=bottom_station_counts.index, color='steelblue')
plt.title('Least Popular Stations')
plt.xlabel('Count')
plt.ylabel('Station')

# Adjust layout and display the chart
plt.tight_layout()
plt.show()


# In[34]:



# get the top 10 start stations on weekends
top_start_stations_weekend = weekend_df['Start_Stn'].value_counts().head(10)

# get the top 10 start stations on weekdays
top_start_stations_weekday = weekday_df['Start_Stn'].value_counts().head(10)

# create subplots
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(15, 6))

# plot top 10 start stations on weekends
sns.barplot(x=top_start_stations_weekend.values, y=top_start_stations_weekend.index, palette='viridis', ax=ax1)
ax1.set_xlabel('Count')
ax1.set_ylabel('Start Station')
ax1.set_title('Top 10 Start Stations on Weekends')

# plot top 10 start stations on weekdays
sns.barplot(x=top_start_stations_weekday.values, y=top_start_stations_weekday.index, palette='viridis', ax=ax2)
ax2.set_xlabel('Count')
ax2.set_ylabel('Start Station')
ax2.set_title('Top 10 Start Stations on Weekdays')

# adjust spacing between subplots
plt.subplots_adjust(wspace=0.3)

# display the plot
plt.show()


# # STEP - 3 Data Preprocessing

# In[20]:


df.drop('D_O_W', axis=1, inplace=True)
df.drop('Ent_Time', axis=1, inplace=True)
df.drop('Ex_Time', axis=1, inplace=True)
df.drop('JNY_TYP', axis=1, inplace=True)
df.drop('DailyCapping', axis=1, inplace=True)
df.drop('Route_ID', axis=1, inplace=True)


display(df)
df.describe()  


# In[21]:


# display(df)
 
df.to_csv('output.csv', index=False)


# In[ ]:




