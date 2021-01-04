import requests

def userInput(query):
    url = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/"+query

    headers = {
        'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com",
        'x-rapidapi-key' : "42a81c1684msh89e08ede69c15b4p1df539jsn876cffad9666"
        }

    response = requests.request("GET", url, headers=headers)
    store = response.json()

    count = 0
    actors = list()
    for i in store["cast"]:
        if count > 5:
            break
        actors.append(i['actor'])
        count += 1

    MovieDetails = {
        'year'  : store['year'],
        'actors': actors
    }
    print(MovieDetails)

# userInput('Get Out')

import requests

url = "https://youtube-search-results.p.rapidapi.com/youtube-search/"

querystring = {"q":"The Girl with the dragon tattoo Trailer"}

headers = {
    'x-rapidapi-key': "313c32bd8cmsh267a7d2977b0b69p1e33d5jsnccd8af3b0eb7",
    'x-rapidapi-host': "youtube-search-results.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

store2 = response.json()
print(store2['items'][1]['link'])