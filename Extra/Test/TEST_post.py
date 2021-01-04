from firebase import firebase

firebase = firebase.FirebaseApplication("https://movies-by-the-sea-ca0b5-default-rtdb.firebaseio.com/", None)
DB_entry = {
    'Name': 'TESTING2',
}
result = firebase.post('/Reviews',DB_entry)
print(result)