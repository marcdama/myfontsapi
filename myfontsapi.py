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


class Top(Resource):
        def get(self, table, tag):
            count = {}
            counter = 0
            for i in db[table].find():
                if not i[tag] in count:
                    count[i[tag]] = {}
                    count[i[tag]]['total'] = 1
                else:
                    count[i[tag]]['total'] += 1
                    count[i[tag]]['designer'] = i['designer']
                    count[i[tag]]['name'] = i['name']
                    count[i[tag]]['font_url'] = i['font_url']
            return count

api.add_resource(Top, '/<table>=<tag>')

if __name__ == '__main__':
    app.run()
