#!/usr/bin/env python
# coding: utf-8

# In[43]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from urllib.request import urlopen
#import scrapy
import re
from splinter import Browser


# ###### MARS NEWS

# In[4]:


url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
response = requests.get(url)

print(response.text)


# In[5]:


#Create object
soup = BeautifulSoup(response.content, 'html.parser')


# In[6]:


#Extract content titles from html
title_results = soup.find_all("div", class_="content_title")
len(title_results)
title_results


# In[7]:


#Loop through extracted titles to get the stripped text
titles = []
for title_result in title_results:
    text_titles = title_result.find('a').text.strip("\n")
    titles.append(text_titles)
titles


# In[8]:


#Extract description paragraphs from html
p_results = soup.find_all("div", class_="rollover_description_inner")
len(p_results)
p_results


# In[9]:


#Loop through extracted paragraphs to get the stripped text
paragraphs = []
for p_result in p_results:
    text_paragraphs = p_result.text.strip("\n")
    paragraphs.append(text_paragraphs)
paragraphs


# ###### FEATURED IMAGE

# In[10]:


url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
img_response = requests.get(url)
print(img_response.text)


# In[11]:


#Create object
img_soup = BeautifulSoup(img_response.content, 'html.parser')


# In[12]:


#Extract base URL for site
base_url = img_soup.find_all("div", class_="jpl_logo")
base_url = str(base_url[0].a["href"].strip("//"))
base_url


# In[13]:


#Extract article from html to access image url
img_results = img_soup.find_all("article")
img_results


# In[14]:


#Extract url path for featured imagee
url = str(img_results[0]["style"].split(" ")[1].strip("url(';')"))
url


# In[15]:


#Concantenatet base url and featured image to get final path
featured_image_url = base_url + url
featured_image_url


# ###### MARS WEATHER

# In[18]:


url = "http://twitter.com/marswxreport"
response = requests.get(w_url)
print(response.text)


# In[19]:


#Create object
soup = BeautifulSoup(response.content, 'html.parser')


# In[21]:


tweets = w_soup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
tweets


# In[222]:


mars_weather = tweets[0].text


# In[223]:


mars_weather = 'InSight sol 556 (2020-06-19) low -90.8ºC (-131.4ºF) high -6.5ºC (20.4ºF) winds from the W at 7.3 m/s (16.3 mph) gusting to 21.3 m/s (47.6 mph)'


# ###### MARS FACTS

# In[36]:


url = "https://space-facts.com/mars/"
tables = pd.read_html(url)
mars_facts = tables[0]
mars_facts = mars_facts.rename(columns = {0: "Criteria", 1: "Value"})
mars_facts = mars_facts.set_index("Criteria")
mars_facts


# In[37]:


html_table = mars_facts.to_html()
html_table = html_table.replace('\n', '')
html_table


# ###### MARS HEMISPHERES

# In[106]:


url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


# In[84]:


h_response = requests.get(url)


# In[85]:


h_soup = BeautifulSoup(h_response.content, 'html.parser')
h_soup


# In[134]:


#Base URL
base_url = h_soup.find_all("div", class_="left")
base = base_url[0].a["href"].strip("/search")
base_url = "h"+ base
base_url


# In[102]:


imgs_count = h_soup.find_all("div", class_="item")
imgs_count


# In[159]:


links = []
img_names = []
for img in imgs_count:
    img_names.append(img.h3.text)
    links.append(img.a["href"])
links
img_names


# In[136]:


results_list = []
for link in links:
    url = base_url+link
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all("div", class_="downloads")
    results_list.append(results)


# In[158]:


img_urls = []
for result in results_list:
    lists = result[0].find_all("li")
    #print(lists)
    for l in lists:
        if l.a.text == "Original":
            img_urls.append(l.a["href"])
        #img_urls.append(result[0].li.a["href"])
img_urls


# In[196]:


img_names


# In[208]:


#Make a list of the keys I will need
keys =["title", "img_url"] 


# In[217]:


#Set values in one list
values = []

for i in range(0,len(img_names)):
    values.append(img_names[i])
    values.append(img_urls[i])
    
values


# In[227]:


hemisphere_image_urls = []

for v in zip(values[::2], values[1::2]):
    hemisphere_image_urls.append(dict(zip(keys, v)))
hemisphere_image_urls


# In[ ]:




