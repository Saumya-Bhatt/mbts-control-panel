from firebase import firebase

firebase = firebase.FirebaseApplication('https://movies-by-the-sea-ca0b5-default-rtdb.firebaseio.com/', None)
result = firebase.get('Reviews','')
res = list(result.values()) 
print(res[0])