"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import UserForm, DatetimeForm
from app.models import User, Date_time
import datetime # import sqlite3

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/users')
def show_users():
    users = db.session.query(User).all()
    return render_template('show_users.html', users=users)



@app.route('/add-user', methods=['POST', 'GET'])
def add_user():
    user_form = UserForm()

    if request.method == 'POST':
        if user_form.validate_on_submit():
            # Get validated data from form
            name = user_form.name.data # You could also have used request.form['name']

            # save user to database
            user = User(name)
            db.session.add(user)
            db.session.commit()

            flash('User successfully added')
            return redirect(url_for('show_users'))

    flash_errors(user_form)
    return render_template('add_user.html', form=user_form)

@app.route('/remove/checkin/<int:id>', methods=['DELETE', 'POST', 'GET'])
def remove_checkin(id):
    db.session.query(Date_time).filter_by(id=id).delete()
    db.session.commit()
    flash('Checkin successfully removed')
    return redirect(url_for('show_checkin'))

@app.route('/remove/user/<int:id>', methods=['DELETE', 'POST', 'GET'])
def remove_user(id):
    db.session.query(User).filter_by(id=id).delete()
    db.session.commit()
    flash('User successfully removed')
    return redirect(url_for('show_users'))

@app.route('/checkin', methods=['POST', 'GET'])

def checkin():
    checkin = DatetimeForm()

    if request.method == 'POST':
        if checkin.validate_on_submit():
            id_nv = checkin.id_nv.data
            status = checkin.status.data
            time_checkin = str(datetime.datetime.now())[:19]

            checkin = Date_time(id_nv, status, time_checkin)

            db.session.add(checkin)
            db.session.commit()

            flash('User successfully added')
            return redirect(url_for('show_checkin'))

    flash_errors(checkin)
    return render_template('checkin.html', form=checkin)

# Flash errors from the form if validation fails
@app.route('/showcheckin')
def show_checkin():

    checkin = db.session.query(Date_time.id, Date_time.id_nv, Date_time.status, Date_time.time_checkin, User.id, User.name).filter_by(id_nv= User.id).all()
    # checkin = db.session.query(Date_time).all()
    return render_template('show_checkin.html', users=checkin)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
