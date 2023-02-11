#!/usr/bin/env python
# coding: utf-8

# # IPL Data Analysis (2008-2020)

# In[1]:


#Importing Required Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ## Loading Datasets

# In[2]:


match_data = pd.read_csv("C:/Users/dharp/IPL Matches 2008-2020.csv")
ball_data = pd.read_csv("C:/Users/dharp/IPL Ball-by-Ball 2008-2020.csv")


# # Displaying data 

# In[3]:


# Top 5 rows of match_data
match_data.head()
# Bottom 5 rows of match_data
match_data.head(-5)


# In[4]:


#Top 5 rows of ball_data
ball_data.head()
#Bottom 5 rows of ball_data
ball_data.head(-5)


# ## Checking Null Values

# In[5]:


match_data.isnull().sum()


# In[6]:


ball_data.isnull().sum()


# In[7]:


match_data.shape


# In[8]:


ball_data.shape


# In[9]:


match_data.columns


# In[10]:


ball_data.columns


# ## Total no. of matches played so far

# In[11]:


print('Matches played so far:', match_data.shape[0])


# ## Venues of all IPL matches

# In[12]:


print('venues of matches:', match_data['city'].unique())


# ## Name of all IPL Teams 

# In[13]:


print('Teams participated:', match_data['team1'].unique())


# In[14]:


#Extracting year values from date column and adding these year values in the separated column 'season'
import warnings
warnings.simplefilter(action='ignore')
match_data['Season'] = pd.DatetimeIndex(match_data['date']).year
match_data.head()


# In[15]:


match_per_season = match_data.groupby(['Season'])['id'].count().reset_index().rename(columns={'id':'matches'})
match_per_season


# In[16]:


sns.countplot(data = match_data['Season'])
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel('Season', fontsize=10)
plt.ylabel('Count', fontsize=10)
plt.title('Total matches played in each season', fontsize = 10, fontweight = "bold")
plt.show()


# In[17]:


season_data = match_data[['id', 'Season']].merge(ball_data, left_on = 'id', right_on = 'id', how = 'left').drop('id', axis = 1)
season_data.head()


# In[18]:


season = season_data.groupby(['Season'])['total_runs'].sum().reset_index()
p = season.set_index('Season')
ax = plt.axes()
ax.set(facecolor = 'black')
sns.lineplot(data=p,palette='magma')
plt.title('Total runs in each season',fontsize=12,fontweight='bold')
plt.show()


# In[19]:


runs_per_season=pd.concat([match_per_season,season.iloc[:,1]],axis=1)
runs_per_season['Runs scored per match']=runs_per_season['total_runs']/runs_per_season['matches']
runs_per_season.set_index('Season',inplace=False)
runs_per_season


# In[20]:


toss=match_data['toss_winner'].value_counts()
ax=plt.axes()
ax.set(facecolor='grey')
sns.set(rc={'figure.figsize':(15,10)},style='darkgrid')
ax.set_title('No.of tossses won by each team',fontsize=20,fontweight='bold')
sns.barplot(y=toss.index, x=toss, orient='h', palette='icefire',saturation=1)
plt.xlabel('# of tosses won')
plt.ylabel('Teams')
plt.show()


# In[21]:


ax=plt.axes()
ax.set(facecolor='grey')
sns.countplot(x='Season', hue='toss_decision', data=match_data, palette='magma', saturation=1)
plt.xticks(rotation=90,fontsize=10)
plt.yticks(fontsize=15)
plt.xlabel('\n Season',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.title('Toss decision across season',fontsize=12,fontweight='bold')
plt.show()


# In[22]:


match_data['result'].value_counts()


# In[23]:


match_data.venue[match_data.result!='runs'].mode()


# In[24]:


match_data.venue[match_data.result!='wickets'].mode()


# In[25]:


match_data.venue[match_data.toss_winner=='Mumbai Indians'][match_data.winner=='Mumbai Indians'].mode()


# In[26]:


match_data.winner[match_data.result!='wickets'].mode()


# In[27]:


match_data.winner[match_data.result!='runs'].mode()


# In[28]:


toss= match_data['toss_winner']== match_data['winner']
plt.figure(figsize=(10,5))
sns.countplot(toss)
plt.show()


# In[29]:


plt.figure(figsize=(12,4))
sns.countplot(match_data.toss_decision[match_data.toss_winner == match_data.winner])
plt.show()


# In[30]:


player=(ball_data['batsman']=='SK Raina')
df_raina=ball_data[player]
df_raina.head()


# In[31]:


df_raina['dismissal_kind'].value_counts().plot.pie(autopct='%1.1f%%',shadow=True,rotatelabels=True)
plt.title("Dismissal Kind",fontweight='bold',fontsize=15)
plt.show()


# In[32]:


def count(df_raina,runs):
    return len(df_raina[df_raina['batsman_runs']==runs])*runs


# In[33]:


print("Runs scored from 1's :",count(df_raina,1))
print("Runs scored from 2's :",count(df_raina,2))
print("Runs scored from 3's :",count(df_raina,3))
print("Runs scored from 4's :",count(df_raina,4))
print("Runs scored from 6's :",count(df_raina,6))


# In[34]:


match_data[match_data['result_margin']==match_data['result_margin'].max()]


# In[35]:


runs=ball_data.groupby(['batsman'])['batsman_runs'].sum().reset_index()
runs.columns=['Batsman', 'runs']
y = runs.sort_values(by='runs',ascending=False).head(10).reset_index().drop('index',axis=1)
y


# In[36]:


ax=plt.axes()
ax.set(facecolor='grey')
sns.barplot(x=y['Batsman'],y=y['runs'],palette='rocket',saturation=1)
plt.xticks(rotation=90,fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel('\n Player',fontsize=15)
plt.ylabel('Total Runs',fontsize=15)
plt.title('Top 10 run scorers in IPL',fontsize=15,fontweight='bold')
plt.show()


# In[37]:


ax=plt.axes()
ax.set(facecolor ='black')
match_data.player_of_match.value_counts()[:10].plot(kind='bar')
plt.xlabel('Players')
plt.ylabel('Count')
plt.title('Highest MOM award winners',fontsize=15,fontweight='bold')
plt.show()

