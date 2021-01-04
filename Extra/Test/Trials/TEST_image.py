
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import datetime


# Fetch the service account key JSON file contents
cred = credentials.Certificate("mbts-storage.json")
firebase_admin.initialize_app(cred)


# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'movies-by-the-sea-ca0b5.appspot.com',
}, name='storage')

bucket = storage.bucket(app=app)
blob = bucket.blob("1917.jpg")

print(blob.generate_signed_url(datetime.timedelta(days=99999), method='GET'))