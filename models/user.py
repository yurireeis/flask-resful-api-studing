from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    displayname = db.Column(db.String(80))
    photo_url = db.Column(db.String(80))
    position = db.Column(db.String(80))

    def __init__(self, username, password, displayname, photo_url, position):
        self.username = username
        self.password = password
        self.displayname = displayname
        self.photo_url = photo_url
        self.position = position

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return dict(id=self.id, username=self.username, displayname=self.displayname, photo=self.photo_url,
                    position=self.position)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
