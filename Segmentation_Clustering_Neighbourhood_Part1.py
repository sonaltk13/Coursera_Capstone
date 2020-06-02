#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd


# In[2]:


source_url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
source = requests.get(source_url).text


# In[3]:


source


# In[4]:


source_soup = BeautifulSoup(source, 'xml')


# In[5]:


table=source_soup.find('table')


# In[6]:


table


# In[7]:


#dataframe will consist of three columns: PostalCode, Borough, and Neighborhood
column_names = ['Postalcode','Borough','Neighborhood']
df = pd.DataFrame(columns = column_names)


# In[8]:


df


# In[9]:


# Search all the postcode, borough, neighborhood 
for tr_cell in table.find_all('tr'):
    row_data=[]
    for td_cell in tr_cell.find_all('td'):
        row_data.append(td_cell.text.strip())
    if len(row_data)==3:
        df.loc[len(df)] = row_data


# In[10]:


df.head()


# In[15]:


df=df[df['Borough']!='Not assigned']
df.head()


# In[16]:


temp_df=df.groupby('Postalcode')['Neighborhood'].apply(lambda x: "%s" % ', '.join(x))
temp_df=temp_df.reset_index(drop=False)
temp_df.rename(columns={'Neighborhood':'Neighborhood_joined'},inplace=True)


# In[17]:


df_merge = pd.merge(df, temp_df, on='Postalcode')


# In[18]:


df_merge.drop(['Neighborhood'],axis=1,inplace=True)


# In[19]:


df_merge.drop_duplicates(inplace=True)


# In[20]:


df_merge.rename(columns={'Neighborhood_joined':'Neighborhood'},inplace=True)


# In[21]:


df_merge.head()


# In[22]:


df_merge.shape


# In[ ]:




