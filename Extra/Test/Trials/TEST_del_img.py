from firebase import firebase as FB
from firebase_admin import storage
import firebase_admin


firebase = FB.FirebaseApplication('https://movies-by-the-sea-ca0b5-default-rtdb.firebaseio.com/', None)
cred = firebase_admin.credentials.Certificate("mbts-storage.json")
app_fb = firebase_admin.initialize_app(cred, {'storageBucket': 'movies-by-the-sea-ca0b5.appspot.com',}, name='storage')

bucket = storage.bucket(app=app_fb)
blob = bucket.blob('111.png')
blob.delete()