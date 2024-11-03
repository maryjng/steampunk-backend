from flask import Flask
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .config import Config
from .routes import api_bp
import openai
import os


# client = MongoClient(Config.CONNECTION_STRING, tlsCAFile=certifi.where())
# db = client['steampunk-backend-dev']

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
    
    CORS(app, resources={
        r"/api/*": {
            "origins": ALLOWED_ORIGINS,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    app.register_blueprint(api_bp, url_prefix='/api')

    
    # @app.before_request
    # def before_request():
    #     g.db = db
    
    # try:
    #     client.admin.command('ping')
    #     print("Pinged your deployment. You successfully connected to MongoDB!")
    # except Exception as e:
    #     print(e)

    return app