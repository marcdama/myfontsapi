from flask import Flask
from flask_restful import reqparse, Api, Resource
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
api = Api(app)

client = MongoClient()
db = client.myfonts_data

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


class Top(Resource):
        def get(self, table):
                g = list(db[table].find())

                return dumps(g)

api.add_resource(Top, '/<table>')

if __name__ == '__main__':
    app.run()
