import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS timestamps;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events_table (
    artist     TEXT,
    auth       VARCHAR(15),
    firstName  TEXT,
    gender     VARCHAR(1),
    itemInSession INTEGER,
    lastName      TEXT,
    length        FLOAT,
    level         VARCHAR(10),
    location      TEXT,
    method        VARCHAR(10),
    page          TEXT,
    registration  TEXT,
    sessionId     INTEGER,
    song          TEXT,
    status        SMALLINT,
    ts            BIGINT,
    userAgent     TEXT,
    userId        INTEGER
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs_table (
  num_songs INTEGER, 
  artist_id VARCHAR(30),
  artist_latitude FLOAT, 
  artist_longitude FLOAT, 
  artist_location TEXT, 
  artist_name TEXT, 
  song_id VARCHAR(30), 
  title TEXT, 
  duration FLOAT, 
  year  SMALLINT
);
""")

#songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (songplay_id BIGINT IDENTITY(0,1),
    start_time bigint references timestamps(start_time),
    user_id int references users(user_id),
    level varchar,
    song_id varchar references songs(song_id),
    artist_id varchar references artists(artist_id),
    session_id int,
    location varchar(200),
    useragent varchar(200),
    PRIMARY KEY(user_id, song_id, start_time)
    );
""")

#user_id, first_name, last_name, gender, level
user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    ( user_id int PRIMARY KEY,
    first_name varchar,
    last_name varchar,
    gender char,
    level varchar
    );
""")

#song_id, title, artist_id, year, duration
song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
    (
    song_id varchar PRIMARY KEY,
    title varchar(200),
    artist_id varchar references artists(artist_id),
    year int,
    duration real
    );
""")

#artist_id, name, location, lattitude, longitude
artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
    (
    artist_id varchar PRIMARY KEY,
    name varchar,
    location varchar,
    latitude real,
    longitude real
    );
""")

#start_time, hour, day, week, month, year, weekday
time_table_create = ("""
    CREATE TABLE IF NOT EXISTS timestamps
    (
    start_time bigint PRIMARY KEY,
    hour int,
    day int,
    weekofyear int,
    month int,
    year int,
    dayofweek int
    );
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events_table
    FROM 's3://udacity-dend/log_data/2018/11/2018-11'
    credentials {}
    json 's3://udacity-dend/log_json_path.json'
    ;
    """).format( config.get("IAM_ROLE", "ARN") )

staging_songs_copy = ("""
    COPY staging_songs_table
    FROM 's3://udacity-dend/song_data'
    credentials {}
    json 'auto'
    ;
""").format( config.get("IAM_ROLE", "ARN") )

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender, level)
SELECT DISTINCT    userId AS user_id,
    firstName AS first_name,
    lastName AS last_name,
    gender,
    level
FROM staging_events_table
WHERE userId IS NOT NULL;
;
""")

song_table_insert = ("""
INSERT INTO songs()
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id, name, location, latitude, longitude)
SELECT 
    DISTINCT artist_id,
    artist_name AS name,
    artist_location AS location,
    artist_latitude AS latitude,
    artist_longitude AS longitude
FROM staging_songs_table;
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]

# create only final star-schema tables
#create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create ]


drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

# drop only star-schema tables
#drop_table_queries = [ songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, artist_table_insert, song_table_insert, time_table_insert]
# test insert table
#insert_table_queries = [user_table_insert]
#insert_table_queries = [artist_table_insert]
insert_table_queries = [song_table_insert]