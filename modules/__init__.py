from flask import Flask
from firebase import firebase as FB
from os.path import join, dirname
from dotenv import load_dotenv

import firebase_admin
import ast
import os


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
certi = ast.literal_eval(os.environ["FIREBASE_CREDS"])


firebase = FB.FirebaseApplication(os.getenv("FIREBASE_RDB"), None)
cred = firebase_admin.credentials.Certificate(certi)
app_fb = firebase_admin.initialize_app(cred, {'storageBucket': os.getenv('STORAGE_BUCKET'),}, name='storage')

app = Flask('__name__')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

from modules import routes