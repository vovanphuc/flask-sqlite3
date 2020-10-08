from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<User %r>' % self.name

class Date_time(db.Model):
    __tablename__ = 'date_time'
    id = db.Column(db.Integer, primary_key = True)
    id_nv = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    time_checkin = db.Column(db.String(255))

    def __init__(self, id_nv, status, time_checkin):
        self.id_nv = id_nv
        self.status = status
        self.time_checkin = time_checkin

    def __repr__(self):
        return '<Time %r>' % self.time_checkin

