import db

# open cursor to perform database operations
cur = db.conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS events (id serial PRIMARY KEY,'
                                'start_date date NOT NULL,'
                                'start_time timestamp NOT NULL,'
                                'venue varchar NOT NULL,'
                                'address varchar NOT NULL);'
                                )

cur.execute('INSERT INTO events (start_date, start_time, venue, address)'
            'VALUES (%s, %s, %s, %s)',
            ('2024-01-05',
             '2024-01-05T18:00:00Z',
             'Cool venue',
            '0000 Cool Street'
            ))

db.conn.commit()