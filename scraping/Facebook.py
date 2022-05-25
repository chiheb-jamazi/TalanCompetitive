#!/usr/bin/env python
# coding: utf-8

# In[17]:


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
def facebook(comp):
    company=comp
    def connect_to_facebook():
        #open the webpage
        driver.get("http://www.facebook.com")

        #target username
        username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
        password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

        #enter username and password
        username.clear()
        username.send_keys("chihebjamazi@gmail.com")
        password.clear()
        password.send_keys("Seawaymn2022&&")

        #target the login button and click it
        button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    def scrolling_function():
        start = time.time()
        initialScroll = 0
        finalScroll = 1000

        while True:
            driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
            initialScroll = finalScroll
            finalScroll += 1000
            end = time.time()
            if round(end - start) > 30:
                break 
    dates =[]
    likes=[]
    descriptions=[]
    comments=[]
    shares=[]
    images=[]
    article_links= []
    def get_facebook_posts(soup):
        containers =soup.find_all(class_='du4w35lb l9j0dhe7')
        for container in containers :
            try :
                date = container.find(class_="tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41")
                x = date.find('a')
                dates.append(x['aria-label'])
    #             print(dates)
            except :
                dates.append('none')
            ###Description######
            try :
                description = container.find(class_="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q")
                descriptions.append(description.get_text())
    #             print(descriptions)
            except :
                descriptions.append('none')
            ###Likes######
            try:
                reaction = container.find(class_ = 'pcp91wgn')
                likes.append(reaction.get_text())
    #             print(likes)
            except :
                likes.append('none')
            ###comments_count######
            try :
                reaction = container.find(class_ = 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db gfeo3gy3 a3bd9o3v b1v8xokw m9osqain')
                comments.append(reaction[0].get_text())
    #             print(comments)
            except:
                comments.append('none')
            ###shares_count ######  
            try :
                reaction = container.find_all(class_ = 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db gfeo3gy3 a3bd9o3v b1v8xokw m9osqain')
                shares.append(reaction[1].get_text())
    #             print(shares)
            except :
                shares.append('none')
            ###images link ###### 
            try :
                reaction = container.find(class_ = 'i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm bixrwtb6')
                images.append(reaction['src'])
    #             print(images)
            except :
                images.append('none')
            try : 

                reaction = container.find(class_ = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 datstx6m k4urcfbm')
                article_links.append(reaction['href'])
    #             print(article_links)
            except :
                article_links.append('none')

        return dates, likes, descriptions, comments, shares, images, article_links

    
    page = "https://www.facebook.com/"+company+"/"
    # driver = webdriver.Chrome(r'C:\\Users\\jchih\\\Documents\\selenium\\chromedriver.exe')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    connect_to_facebook()
    time.sleep(2)
    driver.get(page + 'posts/')
    scrolling_function()
    company_page = driver.page_source
    soup =BeautifulSoup(company_page, 'lxml')
    data = get_facebook_posts(soup)
    driver.close()
    list_Data = pd.DataFrame(
                    {'PostDate': dates,
                     'PostText': descriptions,
                     'PostLikes': likes,       
                     "PostComments":comments,
                     "PostShares": shares,
                     "PostImages":images,
                     "PostArticles":article_links,
                    })
    
    company=comp
    file_name= company+'_facebook_df'
    hdfs_url = "http://localhost:9870/"
    hdfs_user = "chiheb"
    c = InsecureClient(hdfs_url, user=hdfs_user)
    c.makedirs("/user/chiheb/"+company) 
    with c.write(company+'/'+file_name, encoding = 'utf-8') as writer:
        list_Data.to_csv(writer,index=False)

