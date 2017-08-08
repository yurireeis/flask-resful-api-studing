from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel
from models.store import StoreModel


class Item(Resource):
    default_parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, _id=None):
        item = ItemModel.find_by_id(_id)
        if item:
            return item.json(), 200

        return {'message': 'Item not found'.format(_id)}, 404

    @jwt_required()
    def post(self):
        parser = self.default_parser
        parser.add_argument('name', type=str, required=True, help='A item needs a name')
        parser.add_argument('store_id', type=int, required=True, help='A item needs a store')
        parser.add_argument('price', type=float, required=True, help='A item needs a price')
        data = parser.parse_args()

        if ItemModel.find_by_name(data.get('name')):
            return {'code': 1, 'message': 'An item with name {} already exists'.format(data['name'])}, 400

        if not StoreModel.find_by_id(data.get('store_id')):
            return {'message': 'You havent this store registered'}, 400

        item = ItemModel(**data)

        try:
            item.save_to_db()
        except Exception as e:
            return {'message': 'something goes wrong with your insert db action', 'error': e.args, 'code': 'db1'}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, _id):
        item = ItemModel.find_by_id(_id)
        if not item:
            return {'message': 'Item dont exists'.format(item)}, 404

        try:
            item.delete_to_db()
        except:
            return {'message': 'Sorry, we have a problem to perform this action'}

        return {'message': 'item {} deleted'.format(_id)}, 204

    @jwt_required()
    def put(self, _id):
        parser = self.default_parser
        parser.add_argument('name', type=str, required=True, help='No empty name')
        parser.add_argument('store_id', type=int, required=True, help='No empty store')
        parser.add_argument('price', type=float, required=True, help='No empty price')
        data = parser.parse_args()

        item = ItemModel.find_by_id(_id)

        if not item:
            return {'message': 'this item no longer exists'}, 400

        item = ItemModel(**data)
        item.save_to_db()
        return item.json(), 201


class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = ItemModel.all()

        if not items:
            return {'message': 'No items was found'}, 404

        return {'items': [item.json() for item in items]}, 200
