from flask import Flask
from flask_restful import reqparse, Api, Resource
from pymongo import MongoClient
from bson.json_util import dumps
from collections import Counter
import json

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
    def get(self, table, tag):

        font_track = {}

        for i in db[table].find({'name': tag}):
            if not tag in font_track:
                font_track[tag] = {}
                font_track[tag][i['date']+'-'+i['time']] = int(i['rank'])
            else:
                font_track[tag][i['date']+'-'+i['time']] = int(i['rank'])

        return str(font_track)


class Fonts(Resource):
    def get(self, table):

        fonts = {}

        for i in db[table].find():
            if not i['name'] in fonts:
                fonts[i['name']] = i
        return json.loads(dumps([fonts[i] for i in fonts]))


class Summary(Resource):
    def get(self, table):

        d = {}
        d['total_families'] = len(set([i['name'] for i in db[table].find()]))
        d['total_designers'] = len(set([i['designer'] for i in db[table].find()]))

        #avercage cost
        def avg_cost(tag):
            w_cost = []
            for i in db[table].find():
                if len(i[tag]) == 1:
                    w_cost.append(i[tag])
                else:
                    w_cost.append(i[tag][1:])

            q = sum(len(i) for i in w_cost)
            t = sum(float(i.replace(",",".")) for a in w_cost for i in a)
            return format(t / q, '.2f')

        d['average_cost_per_weight'] = avg_cost('rrp_cost')
        return d


api.add_resource(Count, '/count/<table>=<tag>=<time>')
api.add_resource(Track, '/track/<table>=<tag>')
api.add_resource(Fonts, '/fonts/<table>')
api.add_resource(Summary, '/summary/<table>')

if __name__ == '__main__':
    app.run()
