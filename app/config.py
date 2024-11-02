import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')
    CONNECTION_STRING=os.getenv('CONNECTION_STRING')
    OPENAI_SECRET_KEY=os.getenv('OPENAI_SECRET_KEY')
    STABILITY_SECRET_KEY=os.getenv('STABILITY_SECRET_KEY')
    REPLICATE_API_KEY=os.getenv('REPLICATE_API_KEY')