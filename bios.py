import db
import psycopg2.extras

def get_bios():
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM bios')
    # the method fetchall() returns an array of dictionaries when the property cursor_fatory=psycopg2.extras.RealDictCursor is added
    allBios = cur.fetchall()
    cur.close()
    return allBios

def get_bio(id):
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM bios WHERE id=%s', (id,))
    # fetchone returns a tuple but with cursor_factory=psycopg2.extras.RealDictCursor it returns a dictionary
    bio = cur.fetchone()
    cur.close()
    return bio

def create_bio(bioObj):
    print(bioObj)
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('INSERT INTO bios (first_name,last_name, bio, bio_img)' 
                'VALUES (%s, %s, %s, %s)'
                'RETURNING *', 
                (bioObj["first_name"],
                bioObj["last_name"],
                bioObj["bio"],
                bioObj["bio_img"]
                ))
    # This was blowing up with an exception: "psycopg2.ProgrammingError: no results to fetch"
    # because I didn't have a 'RETURNING *' statement - so the db insert didn't
    # actually return any results you could fetch
    newBio = cur.fetchone()
    db.conn.commit()
    cur.close()
    return newBio

def update_bio(bioObj, id):
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # create query
    listOfStrings = [f'{key}' + '=' + '%s' for key in bioObj.keys()]
    data = ', '.join(listOfStrings)
    sqlQuery = 'UPDATE bios SET {input} WHERE id=%s RETURNING *'.format(input=data)
    # values
    listOfValues = [val for val in bioObj.values()]
    listOfValues.append(id)
    cur.execute(sqlQuery, tuple(listOfValues))
    updatedBio = cur.fetchone()
    db.conn.commit()
    cur.close()
    return updatedBio


def delete_bio(id):
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('DELETE FROM bios WHERE id=%s', (id,))
    rows_deleted = cur.rowcount
    db.conn.commit()
    cur.close()
    return rows_deleted