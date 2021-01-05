from flask import render_template, url_for, redirect, flash
from modules.functions import DatabaseOperations
from modules.frame import NavbarActive, return_node, GetData
from modules.forms import ReviewForm
from modules import app

db_crud = DatabaseOperations()
db_data = GetData()





@app.route('/')
def home():
    activate = NavbarActive()
    activate.set_home()
    return render_template('home.html', info=db_data.get_numbers(), activate=activate)



@app.route('/write',methods=['GET','POST'])
def entry():

    input_data = ReviewForm()
    if input_data.validate_on_submit():
        db_crud.upload_review(input_data)
        flash('New review entry was added to the database!')
        return redirect(url_for('table'))

    activate = NavbarActive()
    activate.set_write() 
    return render_template('dashboard.html', form=input_data, activate=activate)



@app.route('/Edit/<int:review_id>',methods=['GET','POST'])
def update(review_id):

    update_id, data = return_node(review_id, 'Reviews', 'ID', nodeValue=True)[0]
    update_data = ReviewForm()
    activate = NavbarActive()

    if update_data.validate_on_submit():
        db_crud.update_review(update_data, update_id)
        flash(f'Movie ID {update_id} was succesfully updated')
        return redirect(url_for('table'))
    return render_template('update.html', review=data, form=update_data, update_id=update_id, review_id=review_id, activate=activate)



@app.route('/table')
def table():
    activate = NavbarActive()
    activate.set_table()
    return render_template('tables.html', reviews=db_data.get_reviews(), total=len(db_data.get_reviews()), activate=activate)



@app.route('/messages')
def message():    
    activate = NavbarActive()
    activate.set_message()
    no_messages = (len(db_data.get_messages()) == 0)
    return render_template('message.html', total=len(db_data.get_messages()), messages=db_data.get_messages(), no_msg=no_messages, activate=activate)



@app.route('/delete_review/<int:review_id>',methods=['GET','POST'])
def delete(review_id):
    flash(db_crud.delete_review(review_id))
    return redirect(url_for('table'))



@app.route('/delete_message',methods=['GET','POST'])
def delete_msg():
    flash(db_crud.delete_message())
    return redirect(url_for('message'))



@app.route('/add_to_IG/<int:review_id>',methods=['GET','POST'])
def IG_update(review_id):
    flash(db_crud.update_ig(review_id))
    return redirect(url_for('table'))





@app.errorhandler(404)
def not_found_error(error):
    activate = NavbarActive()
    er = '404 - Bad Request'
    er_msg = 'This page probably does not exist or has been removed'
    return render_template('error.html', activate=activate, error=er, error_message=er_msg),404
 
@app.errorhandler(500)
def internal_error(error):
    activate = NavbarActive()
    er = '500 - Internal Server Error'
    er_msg = 'There was an error accessing the server side files. Try again later'
    return render_template('error.html', activate=activate, error=er, error_message=er_msg),500