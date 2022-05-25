from flask import Blueprint
from Controllers import chiheb,getSocialReach, getWebMetrics, getGdSentiments

user_bp = Blueprint("home_bp", __name__)

user_bp.route("/socialreach/<company>", methods=["GET"])(getSocialReach)
user_bp.route("/webmetrics", methods=["GET"])(getWebMetrics)
user_bp.route("/gdsentiment", methods=["GET"])(getGdSentiments)
user_bp.route("/scrapdetails", methods=["POST"])(chiheb)

""" user_bp.route("/del/<scrapdetails>", methods=["POST"])(chiheb) """