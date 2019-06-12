from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import request, jsonify
from flask_api import status
from flask_cors import CORS, cross_origin
import pprint
import json
import datetime

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = Flask(__name__)
CORS(app)
client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client['diary']

@app.route('/notes', methods=['GET', 'POST'])
def notes():

    if request.method == 'POST':

        return createNote(request.data)

    else:

        return getNoteList()

@app.route('/notes/<string:noteID>', methods=['GET', 'PUT'])
def noteSpecific(noteID):

    if request.method == 'GET':

        return getNote(noteID)

    else:

        return updateNote(noteID, request.data)

def getNote(noteID):

    result = None

    try:

        result = db.notes.find_one({'_id' : ObjectId(noteID)}, {'title':1, 'body' : 1, 'created' : 1, '_id' : 0})

    except:

        pass

    if result:

        return createResponse({'data': result}, 200)

    else:

        return createResponse({'data': 'Object not found'}, 404)

def updateNote(noteID, note):

    note = json.loads(note.decode('utf8'))
    note["created"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if invalidData(note):

        return createResponse({'data' : 'Invalid data posted'}, 400)

    else:

        result = db.notes.find_one_and_replace({'_id': ObjectId(noteID)}, note, {'title':1, 'body' : 1, 'created' : 1, '_id' : 0})

        if result:

            return createResponse({'data' : result}, 201)

        else:

            return createResponse({'data': 'Object not found'}, 404)

def createNote(note):

    note = json.loads(note.decode('utf8'))
    note["created"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if invalidData(note):

        return createResponse({'data': 'Invalid data posted'}, 400)

    else:

        return createResponse({'data': str(db.notes.insert_one(note).inserted_id)}, 201)

def invalidData(data):

    return not data or 'title' not in data or not data['title'] or 'body' not in data

def getNoteList():

    noteList = []

    for note in db.notes.find({}, {'title':1, 'created' : 1}):

        noteList.append({'id' : str(note['_id']), 'title' : note['title'], 'created' : note['created']})

    return createResponse({'data': noteList}, 200)

def createResponse(data, statusCode):

    response = jsonify(data)
    response.status_code = statusCode
    return response


if __name__ == '__main__':
    
    app.run(debug=True)