#!/usr/bin/env python
# coding: utf-8

# In[36]:


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
import csv
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from hdfs import InsecureClient

def indeed(comp):
        oppa=comp
        global websites 
        websites=[]
        websites.append(oppa)
        s=websites[0]
        company=s
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        sleep(2)
        browser.get('https://www.indeed.com/cmp/'+s)
        sleep(5)
        browser.maximize_window()
        sleep(1)
        src = browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        global jobss
        jobss=[]
        jobs=[]
        jobs_number=[]
        src = browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        h=soup.find_all('a',{'class':'css-ku00p5 emf9s7v0'})
        r=0
        for k in h:
            try :
                s=h[r].find_all('div')
                for i in s[0] :
                    jobs.append(i.get_text().strip())
                r=r+1
            except : pass
        jobs
        for i in range(len(jobs)):
            if i%2==0:
                jobss.append(jobs[i])
            else :
                jobs_number.append(jobs[i])   
        browser.get('https://www.indeed.com/cmp/'+company+'/jobs')
        sleep(1)
        src = browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        jobListItem_title=[]
        jobListItem_location=[]
        jobListItem_tags=[]
        for i in range(1):
            try :
                    src = browser.page_source
                    soup = BeautifulSoup(src, 'lxml')
                    s=browser.find_elements_by_css_selector("[data-testid='jobListItem-title']")
                    for i in s:
                        jobListItem_title.append(i.text)
                    src = browser.page_source
                    soup = BeautifulSoup(src, 'lxml')
                    s=browser.find_elements_by_css_selector("[data-testid='jobListItem-location']")
                    for i in s:
                        jobListItem_location.append(i.text)
                    src = browser.page_source
                    soup = BeautifulSoup(src, 'lxml')
                    s=browser.find_elements_by_css_selector("[data-testid='jobListItem-tags']")
                    for i in s:
                        jobListItem_tags.append(i.text)
            except : pass
        browser.get('https://www.indeed.com/cmp/'+company+'/reviews'+'?fcountry=ALL')
        sleep(1)
        src = browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        try : 
            s=soup.find('div',{'data-testid':'reviewsList'})
            kh=s.find_all('div')
        except : pass
        ################################reviews:
        browser.get('https://www.indeed.com/cmp/'+company+'/reviews'+'?fcountry=ALL')
        sleep(1)
        src = browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        global reviewsss
        global ratingsss
        global author_reviewsss
        reviewsss=[]
        ratingsss=[]
        authors_reviewsss=[]
        reviewss=[]
        ratingss=[]
        reviewss=[]
        authors_reviewss=[]
        reviews_headlines=[]
        reviews_description=[]
        try : 
            for xyz in range(10) : 
                try :
                    #reviews:
                    ratings=[]
                    s=soup.find_all('div',{'class':'css-1h3aion eu4oa1w0'})
                    for i in s:
                        k=i.get_text().strip()
                        ratingss.append(k[0:3])
                    ssh=browser.find_elements_by_css_selector("[data-testid='title']")
                    for i in ssh :
                        reviews_headlines.append(i.text)
                    ssh=browser.find_elements_by_css_selector("[data-tn-component='reviewDescription']")
                    for i in ssh :
                        reviews_description.append(i.text)
                    sx=soup.find_all('span',{'class':'css-xvmbeo e1wnkr790'})
                    for i in sx:
                        if len(i)>=10:
                            authors_reviewss.append(i.get_text().strip())
                    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    browser.find_element_by_css_selector("[title='Next']").click()
                    sleep(1)
                except : break
        except : pass
        reviewsss.append(reviewss)
        ratingsss.append(ratingss)
        authors_reviewsss.append(authors_reviewss)
        browser.get('https://www.indeed.com/cmp/'+company+'/salaries')
        sleep(1)
        src = browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        try :
            ssh=browser.find_element_by_css_selector("[data-tn-section='salary-category-summary-v2']").text
        except : pass
        global jobs_names
        jobs_names=[]
        try:
            k=soup.find_all('span',{'class':"cmp-SalaryCategoryCard-title css-153b0q2 e1wnkr790"})
            for i in k :
                jobs_names.append(i.get_text().strip())
        except : pass 
        global jobs_salaries
        jobs_salaries=[]
        try : 
            k=soup.find_all('span',{'class':"css-1s341tc e1wnkr790"})
            for i in k :
                jobs_salaries.append(i.get_text().strip())
        except : pass 
        interviews = ({'ratings': ratingss,'reviews_headlines': reviews_headlines,'reviews_description': reviews_description, 'authors_reviews': authors_reviewss })
        available_jobs = ({'jobListItem_title': jobListItem_title,'jobListItem_location': jobListItem_location,
                 'jobListItem_tags': jobListItem_tags})
        jobs_categories=({'jobs':jobss,'jobs_number':jobs_number})
        Salaries=({'jobs_names':jobs_names, 'jobs_salaries':jobs_salaries})       
        global df
        df = pd.DataFrame(interviews)
        global df1
        df1 = pd.DataFrame(available_jobs)
        global df3
        df3 = pd.DataFrame(jobs_categories)
        global df4
        df4 = pd.DataFrame(Salaries)
        
        company=comp
        file_name= company+'_ind_interviews_df'
        hdfs_url = "http://localhost:9870/"
        hdfs_user = "chiheb"
        c = InsecureClient(hdfs_url, user=hdfs_user)
        c.makedirs("/user/chiheb/"+company) 
        with c.write(company+'/'+file_name, encoding = 'utf-8') as writer:
            df.to_csv(writer,index=False)
            
        file_name2= company+'_ind_jobs_df'
        with c.write(company+'/'+file_name2, encoding = 'utf-8') as writer:
            df3.to_csv(writer,index=False)
        
        file_name3= company+'_ind_saleries_df'
        with c.write(company+'/'+file_name3, encoding = 'utf-8') as writer:
            df4.to_csv(writer,index=False)

