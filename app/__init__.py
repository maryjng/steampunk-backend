from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
from .config import Config
from .routes import api_bp

client = MongoClient(Config.CONNECTION_STRING, tlsCAFile=certifi.where())
db = client['steampunk-backend-dev']

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # from .auth.routes import auth_bp
    # from .main.routes import main_bp
    
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(main_bp, url_prefix='/')

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