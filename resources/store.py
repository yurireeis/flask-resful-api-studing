from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):

    default_parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, _id):
        store = StoreModel.find_by_id(_id)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self):

        parser = self.default_parser
        parser.add_argument('name', type=str, required=True, help='Store needs a name')
        data = parser.parse_args()

        if StoreModel.find_by_name(data.get('name')):
            return {'message': 'A store with name {} already exists'.format(data.get('name'))}, 400

        store = StoreModel(**data)

        try:
            store.save_to_db()
        except Exception as e:
            return {'message': 'An error occurred when user tried to create a new store', 'error': e.args}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, _id):

        store = StoreModel.find_by_id(_id)

        if not store:
            return {'message': 'this store dont exists'}, 404

        try:
            store.delete_to_db()
        except:
            return {'message': 'something goes wrong with the delete operation'}

        return {'message': 'item deleted'}, 204


class StoreList(Resource):

    @jwt_required()
    def get(self):
        stores = StoreModel.all()

        if not stores:
            return {'message': 'theres no stores indexed'}, 404

        return {'stores': [store.json() for store in stores]}, 200
