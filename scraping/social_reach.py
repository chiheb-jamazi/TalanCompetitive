#!/usr/bin/env python
# coding: utf-8

# In[29]:


from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 
from time import sleep
import time 
from hdfs import InsecureClient
def reach(comp):
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

    def connect_to_instagram():
        #target username
        driver.get("https://www.instagram.com/accounts/login/")

        username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        #enter username and password
        username.clear()
        username.send_keys("chiheb_jamazi")
        password.clear()
        password.send_keys("Seawaymn2011&&")

        #target the login button and click it
        button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

        #We are logged in!
        not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
        not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
        
    overview =[]
    website =[]
    Industry =[]
    Company_size =[]
    linkedin_Reach =[]
    def get_data(soupe):
        # def get_linkedin_details(soupe):
        container =soupe.find('section', {'class':'artdeco-card p5 mb4'}) 
        try:
            overviews= container.find('p', {'class':'break-words white-space-pre-wrap mb5 text-body-small t-black--light'})
            overview.append(overviews.get_text())
        except:
            pass
        try:
            websites = container.find('dd', {'class':'mb4 text-body-small t-black--light'})
            website.append(websites.get_text(strip=True))
        except:
            pass
        try:
            Industrys = container.find_all('dd', {'class':'mb4 text-body-small t-black--light'})
            Industry.append(Industrys[1].get_text(strip=True))
        except:
            pass
        try:
            Company_sizes= container.find('dd', {'class':'text-body-small t-black--light mb1'})
            Company_size.append(Company_sizes.get_text(strip=True))
        except:
            pass
        try:
            linkedin_Reachs= container.find('dd', {'class':'text-body-small t-black--light mb4'})
            linkedin_Reach.append(linkedin_Reachs.get_text(strip=True))
        except:
            pass

        return overview, website,Industry , Company_size , linkedin_Reach
    page = "https://www.linkedin.com/company/"+company+"/about"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    connect_to_linkedin ()
    driver.get(page)
    sleep(3)
    src =driver.page_source
    soupe =BeautifulSoup(src, 'lxml')
    get_data(soupe)

    driver.get("https://www.facebook.com/"+company+"/about/?ref=page_internal")
    sleep(3)
    src =driver.page_source
    soupe =BeautifulSoup(src, 'lxml')
    container =soupe.find('div', {'class':'je60u5p8'}) 
    facebook_Reach= []
    like = container.find('span',{'class':'d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua jq4qci2q a3bd9o3v b1v8xokw oo9gr5id'})
    facebook_Reach.append(like.get_text())

    driver.get("https://twitter.com/"+company+"?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor")
    sleep(4)
    src =driver.page_source
    soupe =BeautifulSoup(src, 'lxml')
    container =soupe.find('div', {'class':'css-1dbjc4n'}) 

    Twitter_numb_tweets= []
    follow = container.find('div',{'class':'css-901oao css-bfa6kz r-14j79pv r-37j5jr r-n6v787 r-16dba41 r-1cwl3u0 r-bcqeeo r-qvutc0'})
    Twitter_numb_tweets.append(follow.get_text())

    Twitter_Reach= []
    follow = container.find_all('a',{'class':'css-4rbku5 css-18t94o4 css-901oao r-18jsvk2 r-1loqt21 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0'})
    Twitter_Reach.append(follow[1].get_text())
    
    connect_to_instagram()
    driver.get("https://www.instagram.com/"+company+"/?hl=en")

    instagram_reach=[]
    instagram_reach.append(driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div/span').text)
    insta_numb_posts=[]
    insta_numb_posts.append(driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/div/span').text)

    driver.close()
    Social_Reach = pd.DataFrame(
                {'overview': overview,
                 'website': website,
                 'Industry': Industry,       
                 "Company_size":Company_size,
                 "linkedin_Reach":linkedin_Reach,
                 "facebook_Reach": facebook_Reach,
                 "Twitter_Reach":Twitter_Reach,
                 "Twitter_num_tweets":Twitter_numb_tweets,
                 "Instagram_reach":instagram_reach,
                 "Insta_num_posts":insta_numb_posts,
                })
    company=comp
    file_name= company+'_social_reach_df'
    hdfs_url = "http://localhost:9870/"
    hdfs_user = "chiheb"
    c = InsecureClient(hdfs_url, user=hdfs_user)
    c.makedirs("/user/chiheb/"+company) 
    with c.write(company+'/'+file_name, encoding = 'utf-8') as writer:
        Social_Reach.to_csv(writer,index=False)

