#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 
from time import sleep
import time 
from hdfs import InsecureClient

def linkedin(comp):
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

    def get_posts_details(soupe):
        poste_date =[] 
        post_text = []
        post_nbreagi = []
        post_nb_comm = []
        post_nb_partage = []
        post_video_link = []
        containers =soupe.find_all('div', {'class':'occludable-update ember-view'})

        for container in containers:
            try:
                his=container.find('span', class_ ="visually-hidden")
        #         print(his.get_text().strip())
                poste_date.append(his.get_text().strip())
            except:
                poste_date.append('none')
            try:
                text=container.find('span', class_ ="break-words")
        #         print(text.get_text().strip())
                post_text.append(text.get_text().strip())
            except:
                post_text.append('none')
            try:
                nbreagi=container.find('span', class_ ="social-details-social-counts__reactions-count")
        #         print(nbreagi.get_text().strip())
                post_nbreagi.append(nbreagi.get_text().strip())
            except:
                post_nbreagi.append('none')  
            try:       
                nb_comm=container.find('button',class_="t-black--light t-12 hoverable-link-text")
        #         print(nb_comm.get_text().strip())
                post_nb_comm.append(nb_comm.get_text().strip())
            except:
                post_nb_comm.append('none')        

            try:        
                nb_partage=container.find('li',class_="social-details-social-counts__item social-details-social-counts__item--with-social-proof")
        #         print(nb_partage.get_text().strip())
                post_nb_partage.append(nb_partage.get_text().strip())
            except:
                post_nb_partage.append('none')
        return poste_date,post_text,post_nbreagi,post_nb_comm,post_nb_partage

    def get_video_details(soupe):
        post_video_link = []
        containers =soupe.find_all('div', {'class':'occludable-update ember-view'})    
        for container in containers :
            try:
                video_link=container.find('video',class_="vjs-tech")
                videolink= video_link['src']
                post_video_link.append(videolink)
            except:
                post_video_link.append('none')
        return post_video_link        

    def get_Articles_details(soupe):
        articles = [] 
        containers =soupe.find_all('div', {'class':'occludable-update ember-view'})    
        for container in containers :
            try : 
                article_link = container.find("article")
                articles.append(article_link.a['href'])
            except:
                articles.append('none')
        return articles        

    def get_images_details(soupe):
        images = []
        containers =soupe.find_all('div', {'class':'occludable-update ember-view'})    
        for container in containers : 
            try:
                spans = container.find_all('img')
                image = spans[1]['src']
                images.append(image)  
            except :
                images.append('None') 
        return images


    company = comp
    page = "https://www.linkedin.com/company/"+company+"/"
    # driver=webdriver.Chrome(r'C:\\Users\\jchih\\\Documents\\selenium\\chromedriver.exe')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    connect_to_linkedin ()
    x=''
    y=''
    for i in ["videos", "articles","images"]:
        try :
            driver.get(page+"posts/?feedView="+i) 
            scrolling_function ()
            src =driver.page_source
            soupe =BeautifulSoup(src, 'lxml')
            data1 = get_posts_details(soupe)
            if i == 'videos':
                data2 = tuple(get_video_details(soupe))
                data = data1 + data2
                VideoData = pd.DataFrame(
                {'PostDate': data[0],
                 'PostText': data[1],
                 'PostLikes': data[2],       
                 "PostComments":data[3],
                 "PostShares": data[4],
                 "Postlink":data[5],
                 "Postype" : "video",
                })
            elif i == 'articles':
                data2 = tuple(get_Articles_details(soupe))
                data = data1 + data2
                ArticlesData = pd.DataFrame(
                {'PostDate': data[0],
                 'PostText': data[1],
                 'PostLikes': data[2],       
                 "PostComments":data[3],
                 "PostShares": data[4],
                 "Postlink":data[5],
                 "Postype" : "article",
                })
            elif i == 'images':
                data2 = tuple(get_images_details(soupe))
                data = data1 + data2
                ImagesData = pd.DataFrame(
                {'PostDate': data[0],
                 'PostText': data[1],
                 'PostLikes': data[2],       
                 "PostComments":data[3],
                 "PostShares": data[4],
                 "Postlink":data[5],
                 "Postype" : "image",
                })




        except :
            print('we have an error')


    Posts = pd.concat([ImagesData, ArticlesData, VideoData],axis=0)

    company=comp
    file_name= company+'_linkedin_df'
    hdfs_url = "http://localhost:9870/"
    hdfs_user = "chiheb"
    c = InsecureClient(hdfs_url, user=hdfs_user)
    c.makedirs("/user/chiheb/"+company) 
    with c.write(company+'/'+file_name, encoding = 'utf-8') as writer:
        Posts.to_csv(writer,index=False)

