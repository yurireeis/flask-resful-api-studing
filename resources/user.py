from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel


class User(Resource):
    default_parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, username):

        user = UserModel.find_by_username(username)

        if user:
            return user.json(), 200

        return {'message': 'user not found'}, 404


class UserRegister(Resource):
    default_parser = reqparse.RequestParser()

    def post(self):

        parser = self.default_parser
        parser.add_argument('username', type=str, required=True, help="This field cannot be blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be blank")
        parser.add_argument('displayname', type=str, required=True, help="This field cannot be blank")
        parser.add_argument('position', type=str, required=True, help="This field cannot be blank")
        parser.add_argument('photo_url', type=str, required=True, help="This field cannot be blank")

        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400

        user = UserModel(**data)  # unpacking a dictionary

        if len(user.username) > 80:
            return {"message": "username can have 80 characters at maximum"}
        elif len(user.password) > 80:
            return {"message": "password can have 80 characters at maximum"}

        try:
            user.save_to_db()
        except Exception as e:
            return {
                'message': 'An error occurred during the process to create a new user.',
                'error': e.args,
                'code': 'db.4'
            }

        return {"message": "User created successfully"}, 201
