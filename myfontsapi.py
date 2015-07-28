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


class Track(Resource):
    def get(self, table):

        font_track = {}

        for i in db[table].find():
            if not i['name'] in font_track:
                font_track[i['name']] = {}
                font_track[i['name']][i['date']] = i['rank']
            else:
                font_track[i['name']][i['date']] = i['rank']

        l = []
        for i in font_track:
            l.append({'name': i,
                      'date': font_track[i]})
        return l


api.add_resource(Count, '/count/<table>=<tag>=<time>')
api.add_resource(Track, '/track/<table>')

if __name__ == '__main__':
    app.run()
