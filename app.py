from flask import Flask
from flask import request
from flask_cors import CORS
import events

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
    print('newEvent', newEvent)
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
    print(f"Received delete http request for id={id}")
    result = events.delete_event(id)
    print(f"Deleted {result} rows")
    if result == 1:
        return "Success", 204
    else:
        return "Not found", 404

