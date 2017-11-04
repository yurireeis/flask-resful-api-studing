import os
from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from flask_restful import Api

from resources.application import Application, ApplicationList
from resources.user import UserRegister, User
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'develop')
CORS(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(Application, '/application', '/application/<int:_id>', endpoint='application')
api.add_resource(ApplicationList, '/applications', endpoint='applications')
api.add_resource(User, '/user/<string:username>', endpoint='user')
api.add_resource(UserRegister, '/register', endpoint='register')

# this validation assure that if you import this module in elsewhere don't accidentally starts this app!
if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(debug=True)
