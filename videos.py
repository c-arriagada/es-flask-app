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

def create_videos(metadata):
    print("Attempting to create new video")
    s3_client = boto3.client('s3')
    # s3_client.put_object(Body=file, Bucket='estilocalico-bucket', Key=metadata["file_name"])
    url = s3_client.generate_presigned_url(
        ClientMethod = 'put_object',
        Params={'Bucket': 'estilocalico-bucket', 'Key':"videos/" + metadata["file_name"]},
        ExpiresIn=3600
    )
    print(url)
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('INSERT INTO videos (videos_name, description, pointer)' 
                'VALUES (%s, %s, %s)'
                'RETURNING *', 
                (metadata["video_name"],
                metadata["description"],
                metadata["file_name"]
                ))
    newVideo = cur.fetchone()
    newVideo['upload_url'] = url
    print('New video created', newVideo)
    db.conn.commit()
    cur.close()
    return newVideo

def update_videos(videoObj, id):
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # create query
    listOfStrings = [f'{key}' + '=' + '%s' for key in videoObj.keys()]
    data = ', '.join(listOfStrings)
    sqlQuery = 'UPDATE videos SET {input} WHERE id=%s RETURNING *'.format(input=data)
    # values
    listOfValues = [val for val in videoObj.values()]
    listOfValues.append(id)
    cur.execute(sqlQuery, tuple(listOfValues))
    updatedBio = cur.fetchone()
    db.conn.commit()
    cur.close()
    return updatedBio


def delete_videos(id):
    cur = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('DELETE FROM videos WHERE id=%s', (id,))
    rows_deleted = cur.rowcount
    db.conn.commit()
    cur.close()
    return rows_deleted