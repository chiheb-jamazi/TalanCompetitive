#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os, random, sys, time
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep 
from selenium.webdriver.common.keys import Keys
import pandas as pd
from getpass import getpass
from time import sleep 
from selenium.common.exceptions import NoSuchAttributeException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from hdfs import InsecureClient
import csv
import re

def semrush(comp):
    xx=comp+".com"
    websites=[]
    websites.append(xx)
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    sleep(2)
    browser.maximize_window()
    sleep(3)
    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')
    browser.get('https://www.semrush.com/analytics/overview/?searchType=domain&q='+websites[0])
    sleep(7)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    username='omhiri43@gmail.com'
    password='omar20mhiri'
    browser.find_element_by_css_selector('#srf-limit-popup > div > div > div > div > div.sso-limit-inner > div.sso-block.sso-block_state_limit-popup > div > div > div > div.sso-tabs > div:nth-child(2)').click()
    elementID = browser.find_element_by_name('email')
    elementID.send_keys(username)
    sleep(2)
    elementID = browser.find_element_by_name('password')
    elementID.send_keys(password)
    sleep(2)
    elementID.submit()
    sleep(7)
    Backlinks_number=browser.find_element_by_css_selector('#domain-overview-app > div > div > div.report\.module__reportCnt___1cf7L > div.___SBoxSizing_1tphm-red-team.summary_desktop\.module__summary___tY5bb.___SCard_wa8fh_gg_ > div > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > a > span').text
    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')
    kui=soup.find_all('span',({'class':'___SText_ey63k_gg_ _size_200_ey63k_gg_ __color_ey63k_gg_'}))
    countries_percentage=[]
    countries_percentages=[]
    for i in range(1,5) :
        k=kui[i].get_text().split()[0]
        countries_percentage.append(k)
    countries_percentages.append(countries_percentage)
    sleep(2)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(1)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    organic_search_traffics=[]
    organic_search_traffic=browser.find_element_by_css_selector('#domain-overview-app > div > div > div.report\.module__reportCnt___1cf7L > div.___SBoxSizing_1tphm-red-team.summary_desktop\.module__summary___tY5bb.___SCard_wa8fh_gg_ > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > a > span').text
    organic_search_traffics.append(organic_search_traffic)
    organic_competitorss=[]
    organic_competitors=[]
    k=[]
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(1)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    try : 
        pi=browser.find_elements_by_class_name('___SText_13ebd_gg_')
        for i in pi [30:60] :
            k.append(i.text)
        for i in k : 
            if (i[0].isalpha()) and (i[:2]!='ht') and (i[:2]!='Vi') and ('.' in i):
                organic_competitors.append(i)
    except : pass
    organic_competitorss.append(organic_competitors)
    sleep(1)
    organic_keywordss=[]
    organic_keywords=[]
    keywords=[]
    try : 
                pi =browser.find_elements_by_class_name('___SText_13ebd_gg_')
                for i in pi[15:30] :
                        keywords.append(i.text)
                for i in keywords : 
                        if (i[0].isalpha()) and (i[:2]!='ht') and (i[:2]!='Vi') and((i[:2]!='Sh')):
                            organic_keywords.append(i)
    except : pass
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    organic_keywordss.append(organic_keywords)
    backlinkss=[]
    backlinks=[]
    p_keywords=[]
    try : 
                pi =browser.find_elements_by_class_name('___SText_13ebd_gg_')
                for i in pi :
                        p_keywords.append(i.text)
                for i in p_keywords : 
                        if (i[:2]=='ht') and ( websites[0] not in i):
                            backlinks.append(i)
    except : pass
    backlinkss.append(backlinks)
    countriess=[]
    countries=[]
    try : 
                khh= browser.find_elements_by_css_selector("[data-at='country-code']")
                for i in khh :
                    countries.append(i.text)
    except : pass
    countriess.append(countries)
    ###
    ###
    ###
    informations = ({'wesbtites': websites, 'organic_search_traffic': organic_search_traffics,'Backlinks_number':Backlinks_number, 'countries': countriess,'countries_percentage':countries_percentages, 'backlinks': backlinkss, 
                     'organic_keywords': organic_keywordss, 'organic_competitors':organic_competitorss}) 
    df = pd.DataFrame(informations)
    browser.close()
     	
    company=comp
    file_name= company+'_semrush_test_df'
    hdfs_url = "http://localhost:9870/"
    hdfs_user = "chiheb"
    c = InsecureClient(hdfs_url, user=hdfs_user)
    c.makedirs("/user/chiheb/"+company) 
    with c.write(company+'/'+file_name, encoding = 'utf-8') as writer:
        df.to_csv(writer,index=False)


# In[ ]:




