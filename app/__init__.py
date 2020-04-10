from dotenv import load_dotenv
from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

from app import routes