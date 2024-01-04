from flask import Flask
import events

app = Flask(__name__)

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
    event1 = {
        'start_date': '2024-01-13',
        'start_time': '2024-01-13T19:00:00Z',
        'venue': 'Great2 venue',
        'address': '2222 Great Street'
        }
    return events.create_event(event1)

@app.route("/events", methods=['PATCH'])
def updateEvent():
    event2 = {
        'id': 11,
        'start_date': '2024-01-13',
        'start_time': '2024-01-13T19:00:00Z',
        'venue': 'Great venue 3',
        'address': '3333 Great Street'
        }
    return events.update_event(event2)

@app.route("/events/<id>", methods=['DELETE'])
def deleteEvent(id):
    print(f"Received delete http request for id={id}")
    result = events.delete_event(id)
    print(f"Deleted {result} rows")
    if result == 1:
        return "Success", 204
    else:
        return "Not found", 404

