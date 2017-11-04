from db import db


class ApplicationModel(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    photo = db.Column(db.String(100))
    description = db.Column(db.String(200))

    def __init__(self, name, photo, description):
        self.name = name
        self.photo = photo
        self.description = description

    def json(self):
        return dict(id=self.id, name=self.name, photo=self.photo, description=self.description)

    @classmethod
    def find_by_id(cls, _id):
        return ApplicationModel.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return ApplicationModel.query.filter_by(name=name).first()

    @classmethod
    def all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
