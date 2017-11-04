from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.evaluation import EvaluationModel


class Evaluation(Resource):
    default_parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, _id=None):
        evaluation = EvaluationModel.find_by_id(_id)
        if evaluation:
            return evaluation.json(), 200

        return dict(message='Application not found'.format(_id)), 404

    @jwt_required()
    def post(self):

        parser = self.default_parser
        parser.add_argument('type', type=str, required=True, help="An app needs a name")
        parser.add_argument('owner', type=str, required=True, help="An app needs an owner")
        data = parser.parse_args()

        evaluation = EvaluationModel(**data)

        try:
            evaluation.save_to_db()
        except Exception as e:
            return dict(message='something goes wrong with your insert db action', error=e.args)

        return evaluation.json(), 201


class EvaluationList(Resource):
    @jwt_required()
    def get(self):
        evaluations = EvaluationModel.all()

        if not evaluations:
            return dict(message='No evaluations was found'), 404

        return dict(evaluations=[evaluation.json() for evaluation in evaluations]), 200
