#!/usr/bin/env python
# coding: utf-8

# In[5]:


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd 
from time import sleep
import time 
import csv
from hdfs import InsecureClient


def linkedinJ(comp):
    company=comp
    def connect_to_linkedin ():
        driver.get("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")
        time.sleep(5)
    #     username = driver.find_element_by_id("username")
        username = driver.find_element(By.ID,"username")
        username.send_keys("chiheb.jamazi@esprit.tn")
    #     pword = driver.find_element_by_id("password")
        pword = driver.find_element(By.ID,"password")
        pword.send_keys("Seawaymn2011&&")
    #     driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def scrolling_function ():
        SCROLL_PAUSE_TIME = 1.5
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #uncomment to limit the number of scrolls
            #scroll_number += 1
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        return 

    Job_post_date =[] 
    company_name = []
    job_title = []
    job_links = []
    Number_applicants = []
    location = []
    working_Place = []
    def get_linkedin_jobs (soup):

        containers = soup.find_all(class_='jobs-search-results__list-item occludable-update p0 relative ember-view')
        for container in containers:
            try:              
                his=container.find(class_='job-card-container__listed-time job-card-container__footer-item')  
                Job_post_date.append(his.get_text(strip =True))
            except:
                Job_post_date.append('none')
            try:
                text=container.find(class_='job-card-container__link job-card-container__company-name ember-view')
                company_name.append(text.get_text(strip =True))
            except:
                company_name.append('none')
            try:
                desc=container.find(class_='disabled ember-view job-card-container__link job-card-list__title')
                job_title.append(desc.get_text(strip =True))
            except:
                job_title.append('none')  
            try:       
                desc=container.find(class_='disabled ember-view job-card-container__link job-card-list__title')
                descs = 'https://www.linkedin.com'+desc['href']
                job_links.append(descs)
            except:
                job_links.append('none')        

            try:        
                nb_applic=container.find(class_='job-card-container__applicant-count job-card-container__footer-item job-card-container__footer-item--highlighted t-bold inline-flex align-items-center')
                Number_applicants.append(nb_applic.get_text(strip= True))
            except:
                Number_applicants.append('none')

            try:        
                loca=container.find(class_='job-card-container__metadata-item')
                location.append(loca.get_text(strip= True))
            except:
                location.append('none')
            try:        
                working=container.find(class_='job-card-container__metadata-item job-card-container__metadata-item--workplace-type')
                working_Place.append(working.get_text(strip= True))
            except:
                working_Place.append('none')

    company = comp
    page = "https://www.linkedin.com/jobs/search/?geoId=105015875&keywords="+company+"%20jobs"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.set_window_size(900,800)
    connect_to_linkedin ()
    for numb in range(10):
        sleep(1)
        driver.get(page+'&start='+str(numb*25)) 
        sleep(1)
        scrolling_function ()
        sleep(2)
        src =driver.page_source
        soup =BeautifulSoup(src, 'lxml')
        get_linkedin_jobs (soup)

    jobs = pd.DataFrame(
            {'Job_post_date': Job_post_date,
             'company_name': company_name,
             'job_title': job_title, 
             "Number_applicants": Number_applicants,
             "Location": location,
             "working_Place": working_Place,
             "job_links":job_links,

            })

    company=comp
    file_name= company+'_linkedin_jobs_df'
    hdfs_url = "http://localhost:9870/"
    hdfs_user = "chiheb"
    c = InsecureClient(hdfs_url, user=hdfs_user)
    c.makedirs("/user/chiheb/"+company) 
    with c.write(company+'/'+file_name, encoding = 'utf-8') as writer:
        jobs.to_csv(writer,index=False)


# In[ ]:




