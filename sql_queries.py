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

songplay_table_create = ("""
""")

user_table_create = ("""
""")

song_table_create = ("""
""")

artist_table_create = ("""
""")

time_table_create = ("""
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events_table
    FROM 's3://udacity-dend/log_data/2018/11/2018-11'
    credentials 'aws_iam_role=arn:aws:iam::349696042462:role/myRedshiftRole'
    json 'auto'
    ;
    """).format()

staging_songs_copy = ("""
    COPY staging_songs_table
    FROM 's3://udacity-dend/song_data'
    credentials 'aws_iam_role=arn:aws:iam::349696042462:role/myRedshiftRole'
    json 'auto'
    ;
""").format()

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
