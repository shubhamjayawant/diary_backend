from flask import Flask
from pymongo import MongoClient
from flask import request, jsonify
import pprint
import json

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
ALLOWED_CONTENT = ['text', 'video', 'image']

app = Flask(__name__)
client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client['diary']

@app.route('/notes', methods=['GET', 'POST'])
def notes():

    if request.method == 'POST':

        return jsonify(createNote(request.data))

    else:

        return jsonify(getNoteList())

def createNote(note):

    note = json.loads(note.decode('utf8').replace("'", '"'))

    if invalidData(note):

        return 'invalid data posted'

    else:

        return str(db.notes.insert_one(note).inserted_id)

def invalidData(data):

    return not data or 'title' not in data or not data['title'] or 'body' not in data or invalidContent(data['body'])

def invalidContent(content):

    if type(content) is not list:

        return True

    for c in content:

        if 'content_type' not in c or c['content_type'] not in ALLOWED_CONTENT or 'content' not in c or c['content'].strip() == '':

            return True

    return False

def getNoteList():

    noteList = []

    for note in db.notes:

        pprint.pprint(note)
        # noteList.append({'id' : note['id'], 'title' : note['title']})

    return noteList


if __name__ == '__main__':
    
    app.run(debug=True)