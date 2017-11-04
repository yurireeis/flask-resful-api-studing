from db import db


class EvaluationModel(db.Model):
    __tablename__ = 'evaluations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    creation_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    application = db.relationship('ApplicationModel')

    def __init__(self, application_id, owner):
        self.application_id = application_id
        self.owner = owner

    def json(self):
        return dict(
            id=self.id,
            owner=self.owner,
            initial_date=self.creation_date,
            expiration_date=self.expiration_date
            )

    @classmethod
    def find_by_id(cls, _id):
        return EvaluationModel.query.filter_by(id=_id).first()

    @classmethod
    def all(cls):
        return cls.query.all()  # set query to bring all evaluations related to the application and team

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
