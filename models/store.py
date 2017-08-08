from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy='dynamic')  # retrieve a list of ItemModels related to the StoreModel

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return StoreModel.query.filter_by(name=name).first()  # SELECT * FROM __tablename__ WHERE name=name LIMIT 1

    @classmethod
    def find_by_id(cls, _id):
        return StoreModel.query.filter_by(id=_id).first()

    @classmethod
    def all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()
