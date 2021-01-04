import json
from firebase import firebase

firebase = firebase.FirebaseApplication("https://movies-by-the-sea-ca0b5-default-rtdb.firebaseio.com/", None)

with open('reviews.json') as json_file:
    data = json.load(json_file)
    for item in data:

        DB_entry = {
            'ID' : item['ID'],
            'Name': item['Name'],
            'Review': item['Review'],
            'Instagram': item['Instagram'],
            'Netflix': item['Netflix'],
            'Prime': item['Prime'],
            'Year': item['Year'],
            'Director': item['Director'],
            'Lead': item['Lead'],
            'Acting': item['Acting'],
            'Story': item['Story'],
            'Execution': item['Execution'],
            'Profundity': item['Profundity'],
            'Overall': item['Overall'],
            'Poster': item['Poster'],
            'Genre1': item['Genre1'],
            'Genre2': item['Genre2'],
            'Links': item['Links'],
            'Image': item['Image-url'],
            'Trailer': item['Trailer']
        }
        result = firebase.post('/Reviews',DB_entry)
        print(result)