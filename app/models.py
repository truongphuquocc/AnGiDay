from app import db
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
   

    def __repr__(self):
        return f"Username is: {self.username}"

    def check_password(self, password):
        return self.password == password
    def set_password(self, password):
        self.password = password

class LoaiMon(db.Model):
    maloai = db.Column(db.String(128), primary_key=True)
    tenloai = db.Column(db.String(128))
    mamon = db.relationship('MonAn',backref="author", lazy=True)

class MonAn(db.Model):
    mamon = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maloai = db.Column(db.String(128), db.ForeignKey('loai_mon.maloai'))
    tenmon = db.Column(db.String(128))
    anh = db.Column(db.String(128))

    def __init__ (self, maloai, tenmon):
        self.maloai = maloai
        self.tenmon = tenmon
