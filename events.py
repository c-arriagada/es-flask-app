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
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    start_date, start_time, venue, address= eventObj.values()
    cur.execute('INSERT INTO events (start_date, start_time, venue, address)'
                'VALUES (%s, %s, %s, %s)'
                'RETURNING *',
                (start_date,
                 start_time,
                 venue,
                 address,
                 ))
    # return same event I just created from db 'RETURNING *'
    newEvent = cur.fetchone()
    print(newEvent)
    db.conn.commit()
    cur.close()
    return newEvent
    
def update_event(eventObj, eventId):
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # query
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
    return updatedEvent

def delete_event(id):
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('DELETE FROM events WHERE id=%s', (id,))
    rows_deleted = cur.rowcount
    db.conn.commit()
    cur.close()
    return rows_deleted


def get_events():
    cur = db.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM events')
    allEvents = cur.fetchall()
    cur.close()
    return allEvents
