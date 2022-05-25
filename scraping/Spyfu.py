#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os, random, sys, time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from hdfs import InsecureClient
# from selenium import webdriver
# from bs4 import BeautifulSoup
# from time import sleep 
# from selenium.webdriver.common.keys import Keys
# import pandas as pd
from getpass import getpass
from time import sleep 
from selenium.common.exceptions import NoSuchAttributeException
# from msedge.selenium_tools import Edge, EdgeOptions
import csv
import re
def spyfu(comp):
    k=comp+'.com'
    websites=[]
    websites.append(k)
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    sleep(2)
    browser.get('https://www.spyfu.com/overview/domain?query='+k)
    sleep(3)
    browser.maximize_window()
    sleep(1)
    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')
    sleep(1)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(1)
    backlinkss=[]
    backlinks=[]
    organic_keywordss=[]
    organic_keywords=[]
    paid_keywords=[]
    paid_keywordss=[]
    organic_competitorss=[]
    organic_competitorsss=[]
    paid_competitorss=[]
    paid_competitorsss=[]
    organic_keywrods_nbs=[]
    paid_keywrod_nbs=[]
    Est_Monthly_SEO_Clicks=[]
    Est_Monthly_SEO_Click_changes=[]
    Est_Monthly_PPC_Clicks=[]
    Est_Monthly_Google_Ad_Budgets=[]

    for website in websites:

            #organic keywords numbers
        try :
            keywords=soup.find_all('a',({'class':'keyword-count margin-bottom'}))
            organic_keywrods_nb=keywords[0].get_text().strip()
            organic_keywrods_nbs.append(organic_keywrods_nb)
        except :
            organic_keywrods_nbs='none'

            #paid keywords numbers
        try :
            paid_keywrod_nb=keywords[1].get_text().strip()
            paid_keywrod_nbs.append(paid_keywrod_nb)
        except :
            paid_keywrod_nbs='none'

            #number of clicks

        clicks=soup.find_all('div',({'class':'click-count'}))
        try :
            Est_Monthly_SEO_Click=clicks[0].get_text().strip()
            Est_Monthly_SEO_Clicks.append(Est_Monthly_SEO_Click)
        except :
            Est_Monthly_SEO_Clicks='none' 
        try :
            Est_Monthly_SEO_Click_change=clicks[1].get_text().strip()
            Est_Monthly_SEO_Click_changes.append(Est_Monthly_SEO_Click_change)
        except :
            Est_Monthly_SEO_Clicks='none'     
        try :
            Est_Monthly_PPC_Click=clicks[2].get_text().strip()
            Est_Monthly_PPC_Clicks.append(Est_Monthly_PPC_Click)
        except :
            Est_Monthly_PPC_Clicks='none'     
        try :
            Est_Monthly_Google_Ad_Budget=clicks[3].get_text().strip()
            Est_Monthly_Google_Ad_Budgets.append(Est_Monthly_Google_Ad_Budget)
        except :
            Est_Monthly_Google_Ad_Budgets='none' 

            #organic competitors

        try :
            organic_competetion=soup.find('div',({'class':'competitor-panel sf-panel sf-global-component tw-shadow'}))
            organic_competitors=organic_competetion.find_all('label',({'class':'sf-simple-tornado-chart-label ellipsis'}))
            for i in range(5):
                organic_competitorss.append(organic_competitors[i].get_text().strip())
            organic_competitorsss.append(organic_competitorss)
        except :
            organic_competitorsss='none' 

            #paid competitors

        try :
            paid_competetion=soup.find_all('div',({'class':'competitor-panel sf-panel sf-global-component tw-shadow'}))
            paid_competitors=paid_competetion[1].find_all('label',({'class':'sf-simple-tornado-chart-label ellipsis'}))
            for i in range(5):
                paid_competitorss.append(paid_competitors[i].get_text().strip())
            paid_competitorsss.append(paid_competitorss)
        except :
            paid_competitorsss='none'    

        xk=soup.find_all('div',({'class':'sf-grid-cell tablet-6'}))

            #organic keywords

        try :
            hh=soup.find_all('td',({'class':'term-cell sf-global-component sf-table-cell'}))
            for i in range(5):
                organic_keywords.append(hh[i].get_text().strip())
            organic_keywordss.append(organic_keywords)
        except :
            organic_keywordss='none' 
            #paid keywords
        try :
            for i in range(5,10):  
                paid_keywords.append(hh[i].get_text().strip())
            paid_keywordss.append(paid_keywords)
        except :
            paid_keywordss='none' 

            #backlinks

        try :
            s='spyfu'
            elems=browser.find_elements_by_css_selector("[target='_blank']")
            for elem in elems :
                h=str(elem.get_attribute('href'))
                if (k not in h) and (s not in h):
                    backlinks.append(h) 
            backlinkss.append(backlinks)
        except :
            backlinkss='none'


    informations = ({'websites':websites,'backlinkss': backlinkss, 'organic_keywordss': organic_keywordss,  'paid_keywordss': paid_keywordss, 'organic_competitorsss': organic_competitorsss, 'paid_competitorsss':paid_competitorsss ,
                     'organic_keywrods_nbs':organic_keywrods_nbs , 'Est_Monthly_SEO_Clicks':Est_Monthly_SEO_Clicks,'Est_Monthly_SEO_Click_changes':Est_Monthly_SEO_Click_changes , 
                     'Est_Monthly_PPC_Clicks':Est_Monthly_PPC_Clicks , 'Est_Monthly_Google_Ad_Budgets':Est_Monthly_Google_Ad_Budgets }) 
    df = pd.DataFrame(informations)
    browser.close()
    
    company=comp
    file_name= company+'_spyfu_test_df'
    hdfs_url = "http://localhost:9870/"
    hdfs_user = "chiheb"
    c = InsecureClient(hdfs_url, user=hdfs_user)
    c.makedirs("/user/chiheb/"+company) 
    with c.write(company+'/'+file_name, encoding = 'utf-8') as writer:
        df.to_csv(writer,index=False)


# In[ ]:




