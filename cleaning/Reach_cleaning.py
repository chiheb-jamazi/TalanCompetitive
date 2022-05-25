#!/usr/bin/env python
# coding: utf-8

# In[73]:


from hdfs import InsecureClient
import pandas as pd
import re
import pymongo

def reach_clean(comp):
    company= comp
    file_name= company+"/"+company+"_social_reach_df"
    hdfs_url = "http://localhost:9870/"
    hdfs_user = "chiheb"
    client = InsecureClient(hdfs_url, user=hdfs_user)
    with client.read(file_name, encoding = 'utf-8') as reader:
      df =  pd.read_csv(reader)
    
    df = df.assign(company=[company])
    
    def cleantext(text):
        text = re.sub(r' people', '', text)
        text=re.sub(r'K Followers','',text)
        text=re.sub(r'K Tweets','',text)
        text=re.sub(r'k','',text)
        text=text.replace(",",".")

        return text
    df['facebook_Reach']= df['facebook_Reach'].apply(cleantext)
    df['Twitter_Reach']= df['Twitter_Reach'].apply(cleantext)
    df['Twitter_num_tweets']= df['Twitter_num_tweets'].apply(cleantext)
    df['linkedin_Reach']= df['linkedin_Reach'].apply(cleantext)
    df['Instagram_reach']= df['Instagram_reach'].apply(cleantext)

    def cleantext2(text):
        text=re.sub("[^.,0-9]", '', text)
        text=text.replace(",",".")


        return text
    df['Company_size']= df['Company_size'].apply(cleantext2)
    df['Insta_num_posts']= df['Insta_num_posts'].apply(cleantext2)
    df['linkedin_Reach']= df['linkedin_Reach'].str.slice(0,8)
    df = df.astype({'Company_size':'float','linkedin_Reach':'float','facebook_Reach':'float','Twitter_Reach':'float'
                   ,'Twitter_num_tweets':'float','Insta_num_posts':'float'})
    data =df.to_dict('records')
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Competitive"]
    mycol = mydb["social_reach"]
    x = mycol.insert_many(data)
    print(x.inserted_ids)

