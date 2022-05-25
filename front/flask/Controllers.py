from requests import request
from model import web_metrics, social_reach , sentiment_glassdoor, scrapclass
from flask import jsonify
from flask.globals import request
import importlib.util

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
Facebook = module_from_file("Facebook", "/home/chiheb/TalanProject/scraping/Facebook.py")
Twitter = module_from_file("Twitter", "/home/chiheb/TalanProject/scraping/Twitter.py")
Linkedin = module_from_file("Linkedin", "/home/chiheb/TalanProject/scraping/Linkedin.py")
Indeed = module_from_file("Indeed", "/home/chiheb/TalanProject/scraping/Indeed.py")
LinkedinJ = module_from_file("LinkedinJ", "/home/chiheb/TalanProject/scraping/LinkedinJ.py")
Semrush = module_from_file("Semrush", "/home/chiheb/TalanProject/scraping/Semrush.py")
Spyfu = module_from_file("Spyfu", "/home/chiheb/TalanProject/scraping/Spyfu.py")
web_metrics_clea= module_from_file("web_metrics_clea", "/home/chiheb/TalanProject/cleaning/web_metrics_clea.py")

""" .only('linkedin_Reach', 'Twitter_Reach','Instagram_reach') """

def getSocialReach(company: str):
    Soacial = social_reach.objects(company=company)
    return jsonify(Soacial), 200

def getWebMetrics():
    webmetric = web_metrics.objects()
    return jsonify(webmetric), 200

def getGdSentiments():
    sentiment = sentiment_glassdoor.objects()
    return jsonify(sentiment), 200



def chiheb():
    companyName=request.json["companyName"]
    Facebook=request.json["Facebook"]
    Twitter=request.json["Twitter"]
    LinkedInP=request.json["LinkedInP"]
    Instagram=request.json["Instagram"]
    Indeed=request.json["Indeed"]
    Glassdoor=request.json["Glassdoor"]
    LinkedInJ=request.json["LinkedInJ"]
    WebMetrics=request.json["WebMetrics"]

    scrapdict={}

    scrapdict["companyName"]=companyName
    scrapdict["Facebook"]=Facebook
    scrapdict["Twitter"]=Twitter
    scrapdict["LinkedInP"]=LinkedInP
    scrapdict["Instagram"]=Instagram
    scrapdict["Indeed"]=Indeed
    scrapdict["Glassdoor"]=Glassdoor
    scrapdict["LinkedInJ"]=LinkedInJ
    scrapdict["WebMetrics"]=WebMetrics

    scrapobject = scrapclass(scraplist=scrapdict)
    """ scrapobject.save() """
    comp=scrapobject.scraplist['companyName']
    try :
        if (scrapobject.scraplist['Facebook']== True):
            Facebook.facebook(comp)
    except:
        pass
    try :
        if (scrapobject.scraplist['Twitter']== True):
            Twitter.twitter(comp)
    except:
        pass
    try :
        if (scrapobject.scraplist['LinkedInP']== True):
            Linkedin.linkedin(comp)
    except:
        pass

    try :
        if (scrapobject.scraplist['Indeed']== True):
            Indeed.indeed(comp)
    except:
        pass
    try :
        if (scrapobject.scraplist['LinkedInJ']== True):
            LinkedinJ.linkedinJ(comp)
    except:
        pass
    try :
        if (scrapobject.scraplist['WebMetrics']== True):
            Semrush.semrush(comp)
            Spyfu.spyfu(comp)
            web_metrics_clea.web_metrics_cleaning(comp)
    except:
        pass

    return jsonify(scrapobject),200