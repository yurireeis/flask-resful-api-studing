import os
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.store import Store, StoreList
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'develop')
api = Api(app)


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, '/item', '/item/<int:_id>', endpoint='item')
api.add_resource(ItemList, '/items', endpoint='items')
api.add_resource(UserRegister, '/register', endpoint='register')
api.add_resource(Store, '/store', '/store/<int:_id>', endpoint='store')
api.add_resource(StoreList, '/stores', endpoint='stores')

# this validation assure that if you import this module in elsewhere don't accidentally starts this app!
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
