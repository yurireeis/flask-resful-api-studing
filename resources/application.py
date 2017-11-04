from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.application import ApplicationModel


class Application(Resource):
    default_parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, _id=None):
        app = ApplicationModel.find_by_id(_id)
        if app:
            return app.json(), 200

        return {'message': 'Application not found'.format(_id)}, 404

    @jwt_required()
    def post(self):

        parser = self.default_parser
        parser.add_argument('name', type=str, required=True, help="An app needs a name")
        parser.add_argument('photo', type=str)
        parser.add_argument('description', type=str)
        data = parser.parse_args()

        app = ApplicationModel.find_by_name(data.get('name'))

        if app:
            return {'message': 'Application is already registered with id {}'.format(app.id)}

        app = ApplicationModel(**data)

        try:
            app.save_to_db()
        except Exception as e:
            return {'message': 'something goes wrong with your insert db action', 'error': e.args}

        return app.json(), 201


class ApplicationList(Resource):
    @jwt_required()
    def get(self):
        apps = ApplicationModel.all()

        if not apps:
            return {'message': 'No applications was found'}, 404

        return {'applications': [application.json() for application in apps]}, 200
