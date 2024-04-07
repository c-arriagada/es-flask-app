import db
import psycopg2.extras
from flask import request
import boto3

def get_videos():
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM videos')
    allVideos = cur.fetchall() #[{}, {}]
    cur.close()
    return allVideos

def create_videos(file, metadata):
    print("Attempting to create new vidoe", file)
    s3_client = boto3.client('s3')
    s3_client.put_object(Body=file, Bucket='estilocalico-bucket', Key=metadata["file_name"])
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('INSERT INTO videos (videos_name, description, pointer)' 
                'VALUES (%s, %s, %s)'
                'RETURNING *', 
                (metadata["video_name"],
                metadata["description"],
                metadata["file_name"]
                ))
    newVideo = cur.fetchone()
    print('New video created', newVideo)
    db.conn.commit()
    cur.close()
    return newVideo

# def update_videos(bioObj, id):
#     cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     # create query
#     listOfStrings = [f'{key}' + '=' + '%s' for key in bioObj.keys()]
#     data = ', '.join(listOfStrings)
#     sqlQuery = 'UPDATE bios SET {input} WHERE id=%s RETURNING *'.format(input=data)
#     # values
#     listOfValues = [val for val in bioObj.values()]
#     listOfValues.append(id)
#     cur.execute(sqlQuery, tuple(listOfValues))
#     updatedBio = cur.fetchone()
#     db.conn.commit()
#     cur.close()
#     return updatedBio


def delete_video(id):
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('DELETE FROM videos WHERE id=%s', (id,))
    rows_deleted = cur.rowcount
    db.conn.commit()
    cur.close()
    return rows_deleted