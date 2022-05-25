#!/usr/bin/env python
# coding: utf-8

# In[57]:


from hdfs import InsecureClient
import pandas as pd
import re
import pymongo

def web_metrics_cleaning(comp):
    company=comp
    file_name= company+"/"+company+"_semrush_test_df"
    hdfs_url = "http://localhost:9870/"
    hdfs_user = "chiheb"
    client = InsecureClient(hdfs_url, user=hdfs_user)
    with client.read(file_name, encoding = 'utf-8') as reader:
      df =  pd.read_csv(reader)

    file_name= company+"/"+company+"_spyfu_test_df"
    hdfs_url = "http://localhost:9870/"
    hdfs_user = "chiheb"
    client = InsecureClient(hdfs_url, user=hdfs_user)
    with client.read(file_name, encoding = 'utf-8') as reader:
      df1 =  pd.read_csv(reader)

    #backlinks
    top_Backlinks=[]
    Backlinks=df1.backlinkss[0]+','+df.backlinks[0]
    s=Backlinks.split(',')
    for i in s :
        top_Backlinks.append(i)
    new_list =[s.replace('[', '') for s in top_Backlinks]
    new_list2=[s.replace(']', '') for s in new_list]
    Top_Backlinks=[s.replace("'", "") for s in new_list2]
    Top_Backlinks=list( dict.fromkeys(Top_Backlinks))

                    #organic keywords

    Organics=[]
    Organic= df1.organic_keywordss[0]+df.organic_keywords[0]
    s=Organic.split(',')
    for i in s :
        Organics.append(i)
    new_list147 =[s.replace('[', '') for s in Organics]
    new_list2147=[s.replace(']', '') for s in new_list147]
    Organic_Keywords=[s.replace("'", "") for s in new_list2147]
    Organic_Keywords=list( dict.fromkeys(Organic_Keywords))

                    #organic competitors

    Organics=[]
    Organic= df1.organic_competitorsss[0]+df.organic_competitors[0]
    s=Organic.split(',')
    for i in s :
        Organics.append(i)
    new_list =[s.replace('[', '') for s in Organics]
    new_list2=[s.replace(']', '') for s in new_list]
    Organic_competitors=[s.replace("'", "") for s in new_list2]
    Organic_competitors=list( dict.fromkeys(Organic_competitors) )

                #Countries

    Countries=[]
    s=df.countries[0].split(',')
    for i in s :
        Countries.append(i)
    new =[s.replace('[', '') for s in Countries]
    new2=[s.replace(']', '') for s in new]
    Countries=[s.replace("'", "") for s in new2]

                #Paid_competitors

    Paid_competitors=[]
    s=df1.paid_competitorsss[0].split(',')
    for i in s :
        Paid_competitors.append(i)
    new_list1 =[s.replace('[', '') for s in Paid_competitors]
    new_list12=[s.replace(']', '') for s in new_list1]
    Paid_competitors=[s.replace("'", "") for s in new_list12]

                #Paid_keywordss


    Paid_keywordss=[]
    s=df1.paid_keywordss[0].split(',')
    for i in s :
        Paid_keywordss.append(i)
    new_list1 =[s.replace('[', '') for s in Paid_keywordss]
    new_list12=[s.replace(']', '') for s in new_list1]
    Paid_keywordss=[s.replace("'", "") for s in new_list12]

                    #countries_percentage
    countries_percentagess=[]
    s=df.countries_percentage[0].split(',')
    for i in s :
        countries_percentagess.append(i)
    new_list1 =[s.replace('[', '') for s in countries_percentagess]
    new_list12=[s.replace(']', '') for s in new_list1]
    countries_percentagess=[s.replace("'", "") for s in new_list12]
    countries_percentagess

    informations = ({'websites':df1.websites[0],'organic_search_traffic':df.organic_search_traffic[0],'Backlinks_number':df.Backlinks_number[0],'backlinks': Top_Backlinks, 'organic_keywords': Organic_Keywords,  'paid_keywords': Paid_keywordss, 'organic_competitors': Organic_competitors, 'paid_competitorsss':Paid_competitors,
                     'organic_keywrods_nbs':df1.organic_keywrods_nbs[0] , 'Est_Monthly_SEO_Clicks':df1.Est_Monthly_SEO_Clicks[0],'Est_Monthly_SEO_Click_changes':df1.Est_Monthly_SEO_Click_changes[0] , 
                     'Est_Monthly_PPC_Clicks':df1.Est_Monthly_PPC_Clicks[0] , 'Est_Monthly_Google_Ad_Budgets':df1.Est_Monthly_Google_Ad_Budgets[0], 'countries': Countries,'countries_percentages':countries_percentagess }) 
    df1=pd.DataFrame([informations])

    df1 = df1.assign(company=[company])

    def cleantext(text):
        text=re.sub("[^.,0-9,-]", '', text)
        text=text.replace(",",".")


        return text
    df1['Est_Monthly_Google_Ad_Budgets']= df1['Est_Monthly_Google_Ad_Budgets'].apply(cleantext)
    df1['Est_Monthly_PPC_Clicks']= df1['Est_Monthly_PPC_Clicks'].apply(cleantext)
    df1['Est_Monthly_SEO_Click_changes']= df1['Est_Monthly_SEO_Click_changes'].apply(cleantext)
    df1['Est_Monthly_SEO_Clicks']= df1['Est_Monthly_SEO_Clicks'].apply(cleantext)
    df1['organic_keywrods_nbs']= df1['organic_keywrods_nbs'].apply(cleantext)
    df1['Backlinks_number']= df1['Backlinks_number'].apply(cleantext)
    df1['organic_search_traffic']= df1['organic_search_traffic'].apply(cleantext)

    df1['countries_percentages'][0] = [elem.rstrip("% ") for elem in df1['countries_percentages'][0]]

    df1 = df1.astype({'organic_keywrods_nbs':'float','Est_Monthly_SEO_Clicks':'float','Est_Monthly_SEO_Click_changes':'float','Est_Monthly_PPC_Clicks':'float'
                   ,'Est_Monthly_Google_Ad_Budgets':'float','organic_search_traffic':'float'})
    for i in range (len (df1['countries_percentages'][0])):
        df1['countries_percentages'][0][i]=float(df1['countries_percentages'][0][i])
    data = df1.to_dict('records')
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Competitive"]
    mycol = mydb["web_metricsfortest"]
    x = mycol.insert_many(data)
    print(x.inserted_ids)

