CREATE TABLE IF NOT EXISTS videos (id serial PRIMARY KEY,
    videos_name varchar NOT NULL,
    description varchar NOT NULL,
    pointer varchar NOT NULL);

CREATE TABLE IF NOT EXISTS events (id serial PRIMARY KEY,
    title varchar NOT NULL,
    start_date timestamp NOT NULL,
    start_time timestamp NOT NULL,
    venue varchar NOT NULL,
    address varchar NOT NULL);

CREATE TABLE IF NOT EXISTS bios (id serial PRIMARY KEY,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    bio varchar NOT NULL,
    img_pointer text);          

INSERT INTO bios (first_name, last_name, bio, img_pointer)
    VAlUES ('Cuixi', 'Aguilar', E'Cuixi is a multi-instrumentalist who grew up on Chicago\'s South Side. His passion for music began when he discovered music\'s special ability to bring people together and open portals to different emotions, periods in time, and particular human perspectives. Cuixi brings a lot of musical diversity, from his Latin American roots, his classical guitar training at the Chicago High School for the Arts and DePaul University, and his love for classic rock. While at DePaul, Cuixi ventured into new waters by fulfilling one of his lifelong dreams of starting a rock band. “Where\'s Fernando?” played at venues like Cubby Bear, Subterranean, Martyrs, and Tonic Room. Cuixi has since pursued singing/songwriting and is currently playing frontman for his latest project, “Rolling Stop”. Cuixi knows the power of music and has always seen it as a tool for social change. He is very passionate about helping students find their voice and is currently doing it through the Intonation Music & School of Rock.', 'Cuixi.jpg'),
    ('Amon', 'Sahelijo', 'Amon has been making music for over 10 years in rock bands, jazz ensembles, and as a solo classical guitarist. He graduated from DePaul University in 2020 with a Bachelor’s degree in Performing Arts Management and Guitar Performance. Amon wants to support artists in today’s ever-changing, increasingly accessible music industry. In addition to playing, Amon loves to help others begin their musical journey through teaching. Some of his biggest inspirations are Eric Johnson, Jimi Hendrix, and Paco de Lucía.', 'Amon.jpg'),
    ('Ryan', 'Norris', 'Ryan started playing guitar at 13 years old and playing with bands in clubs by age 15. When he was 20 years old, Ryan relocated to Murfreesboro, TN to pursue a music industry degree at MTSU and moved the short distance to Nashville soon after. Over 15 years in Music City, he became known as a keyboard player, multi-instrumentalist, and electronic musician. Ryan was a staple on stages and in studios, and toured the world, performing in over 25 countries on four continents. He has scored films, collaborated with visual artists, made music for podcasts, and worked with creatives on the bleeding edge of machine learning.', 'Ryan.jpg');

INSERT INTO videos (videos_name, description, pointer)
    VALUES ('Me Llaman Calle Cover', 'song by Manu Chao', 'Calle.mp4'),
    ('Lobo Hombre en Paris Cover', 'song by La Unión', 'HombreLobo.mp4'),
    ('Passionfruit Cover', 'song by Drake', 'PassionFruit.mp4');
