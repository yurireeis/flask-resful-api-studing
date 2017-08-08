from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400

        user = UserModel(**data)  # unpacking a dictionary

        try:
            user.save_to_db()
        except Exception as e:
            return {
                'message': 'An error occurred during the process to create a new user.',
                'error': e.args,
                'code': 'db.4'
            }

        return {"message": "User created successfully"}, 201
