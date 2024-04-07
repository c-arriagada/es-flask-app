import awsgi
from flask import Flask
from flask import request
from flask_cors import CORS
import events
import bios
import boto3
import logging
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello World!"

@app.route("/events", methods=['GET'])
def allEvents():
    allEvents = events.get_events()
    return allEvents

@app.route("/events/<id>", methods=['GET'])
def getEvent(id):
    return events.get_event(id) # id is hardcoded for testing

@app.route("/events", methods=['POST'])
def addEvent():
    # event1 = {
    #     'start_date': '2024-01-13',
    #     'start_time': '2024-01-13T19:00:00Z',
    #     'venue': 'Great2 venue',
    #     'address': '2222 Great Street'
    #     }
    newEvent = request.json
    return events.create_event(newEvent)

@app.route("/events/<id>", methods=['PATCH'])
def updateEvent(id):
    # event2 = {
    #     'id': 11,
    #     'start_date': '2024-01-13',
    #     'start_time': '2024-01-13T19:00:00Z',
    #     'venue': 'Great venue 3',
    #     'address': '3333 Great Street'
    #     }
    event = request.json # request.json gives me access to the body in the http request
    if event.get("id"): # defensive programming to prevent someone from modifying an events id
        del event["id"]
    return events.update_event(event, id)

@app.route("/events/<id>", methods=['DELETE'])
def deleteEvent(id):
    result = events.delete_event(id)
    if result == 1:
        return "Success", 204
    else:
        return "Not found", 404
    
@app.route("/bios", methods=['GET'])
def getBios():
    return bios.get_bios()

@app.route("/bios/<id>", methods=['GET'])
def getBio(id):
    return bios.get_bio(id)

@app.route("/bios", methods=['POST'])
def createBio():
    newBio = request.json
    result = bios.create_bio(newBio)
    return result

@app.route("/bios/<id>", methods=['PATCH'])
def updateBio(id):
    bio = request.json
    if bio.get("id"): 
        del bio["id"]
    return bios.update_bio(bio, id)

@app.route("/bios/<id>", methods=['DELETE'])
def deleteBio(id):
    print(f"Received delete http request for id={id}")
    result = bios.delete_bio(id)
    print(f"Deleted {result} rows")
    if result == 1:
        return "Success", 204
    else:
        return "Not found", 404

@app.route("/upload", methods=['POST'])
def upload():
    file = request.files
    print(file["file"])
    s3_client = boto3.client('s3')
    # bucket = s3_client.list_objects_v2(Bucket='estilocalico-bucket')
    # s3_files = []
    # for obj in bucket['Contents']:
    #     s3_files.append(obj["Key"])
    # return {"s3 files": s3_files}
    print(request.form)
    s3_client.put_object(Body=file["file"], Bucket='estilocalico-bucket', Key=request.form["file_name"])
    return "Success", 200


def lambda_handler(event, context):
    return awsgi.response(app, event, context)