"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from sqlalchemy import and_

from app import app, db
from flask import render_template, request, redirect, url_for, flash, Response
from app.forms import UserForm, CheckinForm
from app.models import User, Check_in
import datetime # import sqlite3
import cv2
import io
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
    db.session.query(Check_in).filter_by(id=id).delete()
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

# Flash errors from the form if validation fails
@app.route('/showcheckin')
def show_checkin():

    checkin = db.session.query(Check_in.id, Check_in.id_nv, Check_in.status, Check_in.date,Check_in.time, User.name).filter_by(id_nv= User.id).all()
    # checkin = db.session.query(Date_time).all()
    return render_template('show_checkin.html', users=checkin)

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
    cap = cv2.VideoCapture('rtsp://admin:Artintlab123@10.10.46.69/8000')

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')

    # while True:
    #     read_return_code, frame = cap.read()
    #     encode_return_code, image_buffer = cv2.imencode('.jpg', frame)
    #     io_buf = io.BytesIO(image_buffer)
    #     yield (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
