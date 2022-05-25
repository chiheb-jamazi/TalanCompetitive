#!/usr/bin/env python
# coding: utf-8

# In[13]:


import re
import csv
from getpass import getpass
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from hdfs import InsecureClient
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def twitter(comp):
    company=comp
    def get_tweet_data(card):
        """Extract data from tweet card"""
        username = card.find_element_by_xpath('.//span').text
        try:
            handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
        except NoSuchElementException:
            return

        try:
            postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException:
            return

        comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    #     text = comment + responding
        reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
        retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
        like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text

        # get a string of all emojis contained in the tweet
        """Emojis are stored as images... so I convert the filename, which is stored as unicode, into 
        the emoji character."""
        list_img = card.find_elements_by_class_name('css-9pa8cd')
        for img in list_img:
            images = img.get_attribute("src")

        tweet = (username, handle, postdate, comment,responding, images, reply_cnt, retweet_cnt, like_cnt)
        return tweet 

    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    sleep(3)
    #Login
    driver.get('https://twitter.com/login')
    sleep(5)
    username = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[5]/label').send_keys('jamazichiheb')
    driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[6]').click()
    sleep(3)
    password = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys('Seawaymn2011&&')
    sleep(3)
    driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]').click()
    sleep(4)


    
    page = "https://twitter.com/"+company+"/"
    driver.get(page)


    # get all tweets on the page
    data = []
    tweet_ids = set()
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True

    while scrolling:
        page_cards = driver.find_elements_by_xpath('//article[@data-testid="tweet"]')
        for card in page_cards[-15:]:
            tweet = get_tweet_data(card)
            if tweet:
                tweet_id = ''.join(tweet)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)

        scroll_attempt = 0
        while True:
            # check scroll position
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(2)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # end of scroll region
                if scroll_attempt >= 3:
                    scrolling = False
                    break
                else:
                    sleep(2) # attempt another scroll
            else:
                last_position = curr_position
                break

    # close the web driver
    driver.close()


    company=comp
    file_name= company+'_twitter_df'
    hdfs_url = "http://localhost:9870/"
    hdfs_user = "chiheb"
    c = InsecureClient(hdfs_url, user=hdfs_user)
    c.makedirs("/user/chiheb/"+company) 
    with c.write('accenture/'+file_name, encoding = 'utf-8') as f:
        header = ['UserName', 'Handle', 'Timestamp',  'comment','responding', 'images', 'Comments', 'Likes', 'Retweets']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

