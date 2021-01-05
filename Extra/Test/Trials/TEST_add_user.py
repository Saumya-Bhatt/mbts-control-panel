import os
import pyrebase
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

firebase = pyrebase.initialize_app(os.getenv('PYREBASE_CONFIG'))
auth = firebase.auth()
email = 'saumi10600@gmail.com'
password = 'ThisIsMyMBTS1'

user = auth.create_user_with_email_and_password(email, password)
print('success!!')