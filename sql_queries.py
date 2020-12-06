import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = ""
staging_songs_table_drop = ""
songplay_table_drop = ""
user_table_drop = ""
song_table_drop = ""
artist_table_drop = ""
time_table_drop = ""

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events_table (
    artist     VARCHAR(200),
    auth       VARCHAR(15),
    firstName  VARCHAR(20),
    gender     VARCHAR(1),
    itemInSession INTEGER,
    lastName      VARCHAR(20),
    length        FLOAT,
    level         VARCHAR(10),
    location      VARCHAR(50),
    method        VARCHAR(10),
    page          VARCHAR(20),
    registration  VARCHAR(50),
    sessionId     INTEGER,
    song          TEXT,
    status        SMALLINT,
    ts            BIGINT,
    userAgent     VARCHAR(200),
    userId        INTEGER
);
""")

staging_songs_table_create = ("""
""")

#songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (songplay_id SERIAL,
    start_time bigint references time(timestamp),
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
    CREATE TABLE IF NOT EXISTS time
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
    credentials '{}'
    json 'auto'
    ;
    """).format( config.get("IAM_ROLE", "ARN") )

staging_songs_copy = ("""
    COPY staging_songs_table
    FROM 's3://udacity-dend/song_data'
    credentials 'ARN'
    json 'auto'
    ;
""").format( config.get("IAM_ROLE", "ARN") )

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
