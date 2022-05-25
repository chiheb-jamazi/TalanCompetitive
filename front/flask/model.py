
import mongoengine

class web_metrics(mongoengine.Document):
    mongoengine.StringField(required=True)
    websites = mongoengine.StringField(required=True)
    organic_search_traffic = mongoengine.IntField(required=True)
    Backlinks_number=mongoengine.IntField(required=True)
    backlinks = mongoengine.ListField(required=True)
    organic_keywords = mongoengine.ListField(required=True)
    paid_keywords = mongoengine.ListField(required=True)
    organic_competitors = mongoengine.ListField(required=True) 
    paid_competitorsss = mongoengine.ListField(required=True)
    organic_keywrods_nbs = mongoengine.IntField(required=True)
    Est_Monthly_SEO_Clicks= mongoengine.IntField(required=True)
    Est_Monthly_SEO_Click_changes= mongoengine.IntField(required=True)
    Est_Monthly_PPC_Clicks= mongoengine.IntField(required=True)
    Est_Monthly_Google_Ad_Budgets= mongoengine.IntField(required=True)
    countries = mongoengine.ListField(required=True)
    countries_percentages =mongoengine.ListField(required=True)
    company =mongoengine.StringField(required=True)
    
class social_reach(mongoengine.Document):
    overview=mongoengine.StringField(required=True)
    website=mongoengine.StringField(required=True)
    Industry=mongoengine.StringField(required=True)
    Company_size=mongoengine.IntField(required=True)
    linkedin_Reach=mongoengine.IntField(required=True)
    facebook_Reach=mongoengine.IntField(required=True)
    Twitter_Reach=mongoengine.IntField(required=True)
    Twitter_num_tweets=mongoengine.IntField(required=True)
    Instagram_reach=mongoengine.IntField(required=True)
    Insta_num_posts=mongoengine.IntField(required=True)
    company=mongoengine.StringField(required=True)

class sentiment_glassdoor(mongoengine.Document):
    Positive=mongoengine.FloatField(required=True)
    Neutral=mongoengine.FloatField(required=True)
    Negative=mongoengine.FloatField(required=True)

class scrapclass(mongoengine.Document):
    scraplist = mongoengine.DictField(companyName=mongoengine.StringField,
    Facebook=mongoengine.BooleanField,Twitter=mongoengine.BooleanField,LinkedInP=mongoengine.BooleanField,
    Instagram =mongoengine.BooleanField,Indeed=mongoengine.BooleanField,Glassdoor = mongoengine.BooleanField,
    LinkedInJ=mongoengine.BooleanField, WebMetrics=mongoengine.BooleanField)


class youtube(mongoengine.Document):
    competitor=mongoengine.StringField(required=True)
    poste_date=mongoengine.DateTimeField(required=True)
    viewCount=mongoengine.IntField(required=True)
    likeCount=mongoengine.IntField(required=True)
    commentCount=mongoengine.IntField(required=True)
    id_video=mongoengine.StringField(required=True)