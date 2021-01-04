from firebase import firebase as FB
from firebase_admin import credentials
from firebase_admin import storage
import firebase_admin

import datetime
import json

firebase = FB.FirebaseApplication('https://movies-by-the-sea-ca0b5-default-rtdb.firebaseio.com/', None)
result = firebase.get('Reviews','')
res = list(result.values())


# Fetch the service account key JSON file contents
cred = credentials.Certificate("mbts-storage.json")
firebase_admin.initialize_app(cred)


app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'movies-by-the-sea-ca0b5.appspot.com',
}, name='storage')

bucket = storage.bucket(app=app)


for review in res:
    blob = bucket.blob(review['Poster'])
    review['Image-url'] = blob.generate_signed_url(datetime.timedelta(days=99999), method='GET')

with open('reviews.json','w') as student_dumped :
    json.dump(res,student_dumped)