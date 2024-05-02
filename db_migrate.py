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

cur.execute('CREATE TABLE IF NOT EXISTS bios (id serial PRIMARY KEY,'
                                        'first_name varchar NOT NULL,'
                                        'last_name varchar NOT NULL,'
                                        'bio varchar NOT NULL,'
                                        'bio_img text);'
                                        )

cur.execute('ALTER TABLE bios ADD img_pointer text;')

cur.execute('CREATE TABLE IF NOT EXISTS videos (id serial PRIMARY KEY,'
                                        'videos_name varchar NOT NULL,'
                                        'description varchar NOT NULL,'
                                        'pointer varchar NOT NULL);'
                                        )

db.conn.commit()