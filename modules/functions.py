import os
import requests

from modules import app
from os.path import join, dirname
from dotenv import load_dotenv
from firebase_admin import storage
from modules.frame import bool2binary


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)





def save_poster(form_pic):
    f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = f_name + f_ext
    picture_path = os.path.join(app.root_path, 'Extra/Images', picture_fn)
    form_pic.save(picture_path)
    return print('Saved to Static/img')





def remove_img(path, img_name):
    os.remove(path + '/' + img_name)
    if os.path.exists(path + '/' + img_name) is False:
        return True





def MovieInfo(query):

    url1 = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/"+query
    url2 = "https://youtube-search-results.p.rapidapi.com/youtube-search/"

    querystring = {"q":query + " Trailer"}

    headers1 = {
        'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com",
        'x-rapidapi-key' : os.getenv("API_KEY_1")
        }
    headers2 = {
    'x-rapidapi-key': os.getenv("API_KEY_2"),
    'x-rapidapi-host': "youtube-search-results.p.rapidapi.com"
    }

    response1 = requests.request("GET", url1, headers=headers1)
    response2 = requests.request("GET", url2, headers=headers2, params=querystring)
    store1 = response1.json()
    store2 = response2.json()

    count = 0
    actors = list()
    for i in store1["cast"]:
        if count > 2:
            break
        actors.append(i['actor'])
        count += 1

    MovieDetails = {
        'year'  : store1['year'],
        'actors': actors,
        'trailer': store2['items'][1]['link']
    }

    return MovieDetails







def upload_review(input_data, app_fb, firebase):

    result = firebase.get('Reviews','')
    res = list(result.values())

    save_poster(input_data.image.data)
    f_name,f_ext = os.path.splitext(input_data.image.data.filename)
    picture_fn = f_name + f_ext
    filePath = 'Extra/Images/' + picture_fn
    bucket = storage.bucket(app=app_fb)
    blob = bucket.blob(picture_fn)
    blob.upload_from_filename(filePath)
    blob.make_public()
    
    dets = MovieInfo(input_data.name.data)

    DB_entry = {
        'ID' : len(res) + 1,
        'Name': input_data.name.data,
        'Review': input_data.review.data,
        'Instagram': 0,
        'Netflix': bool2binary(input_data.netflix.data),
        'Prime': bool2binary(input_data.prime.data),
        'Year': int(dets['year']),
        'Director': input_data.director.data,
        'Lead': str(dets['actors'][0]) + ', ' + str(dets['actors'][1]),
        'Acting': float(input_data.acting.data),
        'Story': float(input_data.story.data),
        'Execution': float(input_data.execution.data),
        'Profundity': float(input_data.profundity.data),
        'Overall': float(input_data.overall.data),
        'Poster': picture_fn,
        'Genre1': input_data.genre1.data,
        'Genre2': input_data.genre2.data,
        'Links': input_data.link.data,
        'Image': blob.public_url,
        'Trailer': dets['trailer']
    }

    result = firebase.post('/Reviews',DB_entry)
    print(result)
    remove_img('Extra/Images', picture_fn)




def update_review(update_data, update_id, app_fb, firebase):

    pathway = 'Reviews/' + str(update_id)
    updated_list = {
        'Name' : update_data.name.data,
        'Review' : update_data.review.data,
        'Netflix' : bool2binary(update_data.netflix.data),
        'Prime' : bool2binary(update_data.prime.data),
        'Director' : update_data.director.data,
        'Acting': update_data.acting.data,
        'Story': update_data.story.data,
        'Execution': update_data.execution.data,
        'Profundity': update_data.profundity.data,
        'Overall': update_data.overall.data,
        'Genre1': update_data.genre1.data,
        'Genre2': update_data.genre2.data,
        'Links': update_data.link.data,
    }

    if update_data.image.data is None:
        for i in updated_list:
            firebase.put(pathway, i, updated_list[i])
    else:

        data = firebase.get(pathway, '')
        old_img = data['Poster']
        bucket = storage.bucket(app=app_fb)
        blob = bucket.blob(old_img)
        blob.delete()

        save_poster(update_data.image.data)
        f_name,f_ext = os.path.splitext(update_data.image.data.filename)
        picture_fn = f_name + f_ext
        filePath = 'Extra/Images/' + picture_fn
        bucket = storage.bucket(app=app_fb)
        blob = bucket.blob(picture_fn)
        blob.upload_from_filename(filePath)
        blob.make_public()

        updated_list['Poster'] = picture_fn
        updated_list['Image'] = blob.public_url

        for i in updated_list:
            firebase.put(pathway, i, updated_list[i])
        remove_img('Extra/Images', picture_fn)