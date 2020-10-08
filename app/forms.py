from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import InputRequired, DataRequired

class UserForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])

class DatetimeForm(FlaskForm):
    id_nv = StringField('id_nv', validators=[InputRequired()])
    status = BooleanField('status', validators=[DataRequired()])
    checkin = StringField('checkin')