from flask import Flask
from flask_restful import reqparse, Api, Resource
from pymongo import MongoClient
from bson.json_util import dumps
from collections import Counter

app = Flask(__name__)
api = Api(app)

client = MongoClient()
db = client.myfonts_data

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


class Count(Resource):
        def get(self, table, tag, time):
            t = {
            'hour': 1,
            'day': 24,
            'week': 168,
            'month': 744,
            'year': 8760
            }

            g = Counter(i[tag] for i in db[table].find())

            l = []
            for i in g:
                l.append({'name': i, 'total': int(g[i]) / float(t[time])})
            return l

api.add_resource(Count, '/<table>=<tag>=<time>')

if __name__ == '__main__':
    app.run()
