"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from sqlalchemy import and_

from app import app, db
from flask import render_template, request, redirect, url_for, flash, Response, session
from app.forms import UserForm, CheckinForm
from app.models import User, Check_in
import datetime # import sqlite3
import cv2
import io
###
# Routing for your application.
###

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.clear()
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']


        if username =='admin' and password == 'password':
            session['user_id'] = '_islogin'

            return redirect(url_for('show_checkin'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/')
def index():
    if (len(session) != 0):
        return redirect(url_for('show_checkin'))

    else:
        return redirect(url_for('login'))

@app.route('/logout')

def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/users')
def show_users():
    if (len(session) != 0):
        users = db.session.query(User).all()
        return render_template('show_users.html', users=users)
    else :
        return redirect(url_for('login'))


@app.route('/add-user', methods=['POST', 'GET'])
def add_user():

    if (len(session) != 0):
        user_form = UserForm()

        if request.method == 'POST':
            if user_form.validate_on_submit():
                # Get validated data from form
                id = str(user_form.id.data)
                name = user_form.name.data # You could also have used request.form['name']

                print(id, name)
                # save user to database
                user = User(id, name)
                db.session.add(user)
                db.session.commit()

                flash('User successfully added')
                return redirect(url_for('show_users'))

        flash_errors(user_form)
        return render_template('add_user.html', form=user_form)
    else :
        return redirect(url_for('login'))

@app.route('/remove/checkin/<int:id>', methods=['DELETE', 'POST', 'GET'])
def remove_checkin(id):
    if (len(session) != 0):

        db.session.query(Check_in).filter_by(id=id).delete()
        db.session.commit()
        flash('Checkin successfully removed')
        return redirect(url_for('show_checkin'))
    else :
        return redirect(url_for('login'))

@app.route('/remove/user/<int:id>', methods=['DELETE', 'POST', 'GET'])
def remove_user(id):
    if (len(session) != 0):

        db.session.query(User).filter_by(id=id).delete()
        db.session.commit()
        flash('User successfully removed')
        return redirect(url_for('show_users'))
    else :
        return redirect(url_for('login'))

@app.route('/checkin', methods=['POST', 'GET'])

def checkin():

    if (len(session) != 0):

        checkin = CheckinForm()
        if request.method == 'POST':
            if checkin.validate_on_submit():
                id_nv = checkin.id_nv.data
                status = checkin.status.data
                date = str(datetime.datetime.now())[:10]
                time = str(datetime.datetime.now())[10:19]

                check = db.session.query(Check_in).filter(and_(Check_in.id_nv==id_nv, Check_in.date==date)).all()
                # print(len(check))
                if(len(check)==0):
                    checkin = Check_in(id_nv, status, date, time)
                    db.session.add(checkin)
                    db.session.commit()
                    flash('User successfully added')

                return redirect(url_for('show_checkin'))

        flash_errors(checkin)
        return render_template('checkin.html', form=checkin)
    else :
        return redirect(url_for('login'))

@app.route('/showcheckin', methods=['POST', 'GET'])
def show_checkin():
    print('SESSION SHOW CHECKIN ', session)

    if (len(session) != 0):

        checkin = db.session.query(Check_in.id, Check_in.id_nv, Check_in.status, Check_in.date,Check_in.time, User.name).\
                    filter(and_(Check_in.id_nv== User.id)).all()

        if request.method == 'POST':
            name_search = request.form['name_search']
            date_search = request.form['date_search']
            search = "%{}%".format(date_search)

            if len(date_search) == 7 and name_search != '':
                checkin = db.session.query(Check_in.id, Check_in.id_nv, Check_in.status, Check_in.date, Check_in.time,
                                       User.name).filter(and_(Check_in.id_nv == User.id, Check_in.date.like(search),
                                                              User.name == name_search)).all()
            if len(date_search) == 7 and name_search == '':
                checkin = db.session.query(Check_in.id, Check_in.id_nv, Check_in.status, Check_in.date, Check_in.time,
                                       User.name).filter(and_(Check_in.id_nv == User.id, Check_in.date.like(search))).all()

            if name_search == '' and len(date_search) == 10:
                checkin = db.session.query(Check_in.id, Check_in.id_nv, Check_in.status, Check_in.date, Check_in.time,
                                           User.name).filter(and_(Check_in.id_nv == User.id, Check_in.date==date_search)).all()

            if date_search == '' and name_search != '':
                checkin = db.session.query(Check_in.id, Check_in.id_nv, Check_in.status, Check_in.date, Check_in.time,
                                           User.name).filter(and_(Check_in.id_nv == User.id, User.name==name_search)).all()

            if name_search == '' and date_search == '':
                checkin = db.session.query(Check_in.id, Check_in.id_nv, Check_in.status, Check_in.date, Check_in.time,
                                           User.name).filter(and_(Check_in.id_nv == User.id)).all()

            if len(date_search) == 10 and name_search != '':
                checkin = db.session.query(Check_in.id, Check_in.id_nv, Check_in.status, Check_in.date, Check_in.time,
                                           User.name).filter(and_(Check_in.id_nv == User.id, Check_in.date==date_search,
                                                                  User.name == name_search)).all()
            return render_template('show_checkin.html', users=checkin)
        return render_template('show_checkin.html', users=checkin)

    else :
        return redirect(url_for('login'))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

@app.route('/live')
def live():
    return render_template('live.html')

def gen():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
