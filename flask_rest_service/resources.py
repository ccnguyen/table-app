import json
from flask import request, abort
#from flask import restful
from flask_restful import Resource,reqparse
from flask_rest_service import app, api, mongo
from bson.objectid import ObjectId

class ReadingList(Resource):
    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('reading', type=str)
        super(ReadingList, self).__init__()

    # will return all readings when receiving an HTTP GET
    def get(self):
        return  [x for x in mongo.db.readings.find()]

    # CREATE NEW READING WHEN RECEIVING AN HTTP POST
    def post(self):
        args = self.parser.parse_args()
        if not args['reading']:
            abort(400)

        jo = json.loads(args['reading'])
        reading_id =  mongo.db.readings.insert(jo)
        return mongo.db.readings.find_one({"_id": reading_id})


class Reading(Resource):
    # gets objectID as a param and returns reading with that id when receiving an HTTP GET
    # deletes reading with that ID when receiving an HTTP DELETE
    def get(self, reading_id):
        return mongo.db.readings.find_one_or_404({"_id": reading_id})

    def delete(self, reading_id):
        mongo.db.readings.find_one_or_404({"_id": reading_id})
        mongo.db.readings.remove({"_id": reading_id})
        return '', 204


class Root(Resource):
    # returns dictionary with info on MongoDB connection
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }

api.add_resource(Root, '/')
api.add_resource(ReadingList, '/readings/')
api.add_resource(Reading, '/readings/<ObjectId:reading_id>')