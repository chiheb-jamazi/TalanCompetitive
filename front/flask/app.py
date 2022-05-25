from flask import  Flask, render_template, request, session
from flask_mongoengine import MongoEngine
from Routes import user_bp
from flask_cors import CORS

def createApp():
    app = Flask(__name__, template_folder="templates", static_folder="assets")
    CORS(app)
    cors =CORS(app, resources={r"": {"origins": ""}})
    # app configs
    app.config['MONGODB_SETTINGS'] = {
        "db": "Competitive",
    }

    # Mongo db
    db = MongoEngine(app)

    # routes
    app.register_blueprint(user_bp)
  

    return app, db




app, db = createApp()
if __name__ == "_main_":
    app.run(debug=True, port=5000)