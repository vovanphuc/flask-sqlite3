from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import InputRequired, DataRequired

class UserForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])

class CheckinForm(FlaskForm):
    id_nv = StringField('id_nv', validators=[InputRequired()])
    status = BooleanField('status', validators=[DataRequired()])
    date = StringField('date')
    time = StringField('time')