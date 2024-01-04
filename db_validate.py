import db 

cur = db.conn.cursor()

cur.execute('SELECT version();')
version = cur.fetchone()[0]
print(version)
# testing that we connected to db and got version
assert version.startswith('PostgreSQL 11.19'), f"Wanted version 11.19 got {version} " 

# create event, get event by id, assert retrieve event is the same as we tried to create

cur.execute('SELECT * from events')
events = cur.fetchall()
print(events)

