from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.question import QuestionModel


# TODO: fix all above comments
class Question(Resource):
    default_parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, _id=None):
        question = QuestionModel.find_by_id(_id)  # really (?)
        if question:
            return question.json(), 200

        return dict(message='Question not found'.format(_id)), 404

    @jwt_required()
    def post(self):
        parser = self.default_parser
        parser.add_argument('evaluation', type=int, required=True, help="A question needs an evaluation")
        parser.add_argument('author', type=str, required=True, help="A question needs an author")
        data = parser.parse_args()

        question = QuestionModel(**data)

        try:
            question.save_to_db()
        except Exception as e:
            return dict(message='something goes wrong with your insert db action', error=e.args)

        return question.json(), 201


class EvaluationList(Resource):
    @jwt_required()
    def get(self):
        questions = QuestionModel.all()

        if not questions:
            return dict(message='No questions was found'), 404  # maybe set key for internationalization

        return dict(evaluations=[question.json() for question in questions]), 200
