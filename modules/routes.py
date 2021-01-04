from flask import render_template, url_for, redirect, request, flash
from modules.functions import upload_review, update_review
from modules.frame import NavbarActive
from modules.forms import ReviewForm
from modules import app, firebase, app_fb

from firebase_admin import storage


@app.route('/')
def home():

    if isinstance(firebase.get('Contact-Us',''),None):
        general = {
            'reviews' : len(firebase.get('Reviews','')),
            'messages' : 0
        } 
    else:
        general = {
            'reviews' : len(firebase.get('Reviews','')),
            'messages' : len(firebase.get('Contact-Us',''))
        }
    ig_count = sum(
        i['Instagram'] == 1 for i in list(firebase.get('Reviews','').values())
    )
    activate = NavbarActive()
    activate.set_home()
    return render_template('home.html', info=general, ig_count=ig_count, activate=activate)



@app.route('/write',methods=['GET','POST'])
def entry():

    input_data = ReviewForm()

    if input_data.validate_on_submit():
        upload_review(input_data, app_fb, firebase)
        flash('New review entry was added to the database!')
        return redirect(url_for('table'))

    activate = NavbarActive()
    activate.set_write() 
    return render_template('dashboard.html', form=input_data, activate=activate)



@app.route('/Edit/<int:review_id>',methods=['GET','POST'])
def update(review_id):

    reviews = firebase.get('Reviews','')
    update_data = ReviewForm()

    data = {}
    update_id = ''
    for i in reviews:
        if reviews[i]['ID'] == review_id:
            data = reviews[i]
            update_id = i
        
    if update_data.validate_on_submit():
        update_review(update_data, update_id, app_fb, firebase)
        flash(f'Movie ID {update_id} was succesfully updated')
        return redirect(url_for('table'))

    activate = NavbarActive()
    return render_template('update.html', review=data, form=update_data, update_id=update_id, review_id=review_id, activate=activate)



@app.route('/table')
def table():

    result = firebase.get('Reviews','')
    res = list(result.values())

    total = len(res)
    res.reverse()
    activate = NavbarActive()
    activate.set_table()

    return render_template('tables.html', reviews=res, total=total, activate=activate)


@app.route('/messages')
def message():

    messages = firebase.get('Contact-Us','')
    try:
        msg = list(messages.values())
        total_msg = len(msg)
        no_messages = True if total_msg == 0 else False
        msg.reverse()
    except:
        msg = None
        total_msg = 0
        no_messages = True
    
    activate = NavbarActive()
    activate.set_message()
    return render_template('message.html', total=total_msg, messages=msg, no_msg=no_messages, activate=activate)



@app.route('/delete_review/<int:review_id>',methods=['GET','POST'])
def delete(review_id):

    item = {}
    all_rev = firebase.get('Reviews','')
    for i in all_rev:
        if all_rev[i]['ID'] == review_id:
            item = {
                'ID': i,
                'Image': all_rev[i]['Poster']
            }

    bucket = storage.bucket(app=app_fb)
    blob = bucket.blob(item['Image'])
    blob.delete()
    firebase.delete('Reviews/',item['ID'])
    notif = 'Review ID : ' + item['ID'] + ' of movie number : ' + str(review_id) + ' was deleted'
    flash(notif)
    return redirect(url_for('table'))



@app.route('/delete_message',methods=['GET','POST'])
def delete_msg():

    message_id = ''
    string = request.args.get('message_id')
    string1 = string.replace('+',' ')
    string2 = string1.replace('%3A',':')
    string3 = string2.replace('%2F','/')

    all_rev = firebase.get('Contact-Us','')
    for i in all_rev:
        if all_rev[i]['Subject'] == string3: 
            message_id = i

    firebase.delete('Contact-Us/',message_id)
    notif = 'Message ID: ' + message_id + ' was deleted'
    flash(notif)
    return redirect(url_for('message'))


@app.route('/add_to_IG/<int:review_id>',methods=['GET','POST'])
def IG_update(review_id):

    item = ''
    all_rev = firebase.get('Reviews','')
    for i in all_rev:
        if all_rev[i]['ID'] == review_id:
            item = i

    pathway = 'Reviews/' + str(item)
    firebase.put(pathway, 'Instagram', 1)
    
    notif = 'Review ID : ' + item + ' was updated to Instagram'
    flash(notif)
    return redirect(url_for('table'))



#Handling error 404 and displaying relevant web page
@app.errorhandler(404)
def not_found_error(error):
    activate = NavbarActive()
    er = '404 - Bad Request'
    er_msg = 'This page probably does not exist or has been removed'
    return render_template('error.html', activate=activate, error=er, error_message=er_msg),404
 
#Handling error 500 and displaying relevant web page
@app.errorhandler(500)
def internal_error(error):
    activate = NavbarActive()
    er = '500 - Internal Server Error'
    er_msg = 'There was an error accessing the server side files. Try again later'
    return render_template('error.html', activate=activate, error=er, error_message=er_msg),500