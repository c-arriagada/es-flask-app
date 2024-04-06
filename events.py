# eventObj example
# {start_date: 2024-01-05, start_time:'2024-01-05T18:00:00Z', venue:'Cool venue', address:'0000 Cool Street'}
import db
import psycopg2.extras

def get_event(id):
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM events WHERE id=%s', (id,))
    # fetchone returns a tuple but with cursor_factory=psycopg2.extras.RealDictCursor it returns a dictionary
    getEvent = cur.fetchone() 
    # close db cursor
    cur.close()
    return getEvent

def create_event(eventObj):
    print('Attempting to create new event', eventObj)
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('INSERT INTO events (title, start_date, start_time, venue, address)'
                'VALUES (%s, %s, %s, %s, %s)'
                'RETURNING *',
                (eventObj["title"],
                 eventObj["start_date"],
                 eventObj["start_time"],
                 eventObj["venue"],
                 eventObj["address"],
                 ))
    # return same event I just created from db 'RETURNING *'
    newEvent = cur.fetchone()
    db.conn.commit()
    cur.close()
    parsedEvent = transformData(newEvent)
    print('Created new event', parsedEvent)
    return parsedEvent
    
def update_event(eventObj, eventId):
    print('Attempting to update event', eventObj)
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # create query
    listOfStrings = [f'{key}' + '=' + '%s' for key in eventObj.keys()]
    data = ', '.join(listOfStrings)
    sqlQuery = 'UPDATE events SET {input} WHERE id=%s RETURNING *'.format(input=data)
    # values
    listOfValues = [val for val in eventObj.values()]
    listOfValues.append(eventId)
    cur.execute(sqlQuery,tuple(listOfValues))
    updatedEvent = cur.fetchone()
    db.conn.commit()
    cur.close()
    parsedEvent = transformData(updatedEvent)
    print('Successfully updated event', parsedEvent)
    return parsedEvent

def delete_event(id):
    print('Attempting to delete event with id', id)
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('DELETE FROM events WHERE id=%s', (id,))
    rows_deleted = cur.rowcount
    db.conn.commit()
    cur.close()
    print('Number of rows deleted', rows_deleted)
    return rows_deleted


def get_events():
    cur = db.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM events')
    # the method fetchall() returns an array of dictionaries when the property cursor_fatory=psycopg2.extras.RealDictCursor is added
    allEvents = cur.fetchall()
    cur.close()
    parsedEvents = [transformData(event) for event in allEvents]
    return parsedEvents

# Date parsing 
# from dateutil.parser import *
# x = parse("Fri, 05 Jan 2024 18:00:00 GMT")
# x.strftime("%Y-%m-%dT%H:%M:%SZ")
# # -> '2024-01-05T18:00:00Z'
# When you query using SELECT * FROM events to retrieve events in db psycopg2 returns a datetime object 
# for start_time and start_date when data type for that column is set to timestamp. Didn't need to use 
# dateutil to parse but did use datetime's strftime method to parse datetime object to iso-8601 format.

def transformData(obj):
    newObj = {
                'id':         obj['id'], 
                'title':      obj['title'],
                'start':      (obj['start_date']).strftime("%Y-%m-%dT%H:%M:%SZ"),
                'startTime':  (obj['start_time']).strftime("%Y-%m-%dT%H:%M:%SZ"),
                'extendedProps': {
                    'venue':      obj['venue'],
                    'address':    obj['address']
              }}

    return newObj
