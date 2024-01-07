import db

# open cursor to perform database operations
cur = db.conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS events (id serial PRIMARY KEY,'
                                'title varchar NOT NULL,'
                                'start_date timestamp NOT NULL,'
                                'start_time timestamp NOT NULL,'
                                'venue varchar NOT NULL,'
                                'address varchar NOT NULL);'
                                )

cur.execute('INSERT INTO events (title, start_date, start_time, venue, address)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('Concert',
            '2024-01-05T18:00:00Z',
            '2024-01-05T18:00:00Z',
            'Cool venue',
            '0000 Cool Street'
            ))

db.conn.commit()