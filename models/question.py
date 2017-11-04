from db import db


class QuestionModel(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, unique=True)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluations.id'))
    question = db.Column(db.String(80))
    author = db.Column(db.String(80))
    creation_date = db.Column(db.Date, default=db.func.now())
    evaluation = db.relationship('EvaluationModel')

    def __init__(self, evaluation_id, author, question):
        self.evaluation_id = evaluation_id
        self.author = author
        self.question = question

    def json(self):
        return dict(
            id=self.id,
            evaluation_id=self.evaluation_id,
            question=self.question,
            author=self.author,
            creation_date=self.creation_date
            )

    @classmethod
    def find_by_id(cls, _id):
        return QuestionModel.query.filter_by(id=_id).first()

    @classmethod
    def all(cls):
        return cls.query.all()  # set query to bring all questions that belong to specific evaluation_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
