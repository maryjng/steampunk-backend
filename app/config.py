import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')
    CONNECTION_STRING=os.getenv('CONNECTION_STRING')