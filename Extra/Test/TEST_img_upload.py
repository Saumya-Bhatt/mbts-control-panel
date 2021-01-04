
from firebase_admin import credentials, initialize_app, storage
# Init firebase with your credentials
cred = credentials.Certificate("mbts-storage.json")
initialize_app(cred, {'storageBucket': 'movies-by-the-sea-ca0b5.appspot.com'})

# Put your local file path 
filePath = "../../modules/mclaren.png"
fileName = 'mclaren.png'
bucket = storage.bucket()
blob = bucket.blob(fileName)
blob.upload_from_filename(filePath)

# Opt : if you want to make public access from the URL
blob.make_public()

print("your file url", blob.public_url)