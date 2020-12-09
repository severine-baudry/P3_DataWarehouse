# Schema for songplay analysis

This project creates a database of songs and of user activity on the Sparkify streaming app. It arranges the raw information in a star-schema database centered on song plays.


# Database structure

To simplify the database queries, we choose to follow a star design. The database thus contains a fact table, **songlays**, which contains information about each song played by users through Sparkify streaming app. The database also contains the following dimension tables :
- **users** : contains information about Sparkify users
- **songs** : contains song information
- **artists** : contains information about the songs' artists
- **time** : contains information about the playtime of songs through the app.

Sparkify analytics team is particularly interested in knowing what songs users are listening to. The **songplays** table is what is hence of interest to them, and is constantly updated as log data is retrieved from the streaming app. It is thus a fact table. The other tables gives more detail information about some elements of the fact table (i.e. users, songs, artist, and playtime). These are thus dimension tables.

![alt text](songplay_DB.png "Sparkify song play schema")

# Installation

## Prerequisites

This project uses python3 and postgresql.
Python libraries to install :
- `psycopg2`
- `configparser`
- `importlib`

## AWS redshift cluster
This project runs on a [AWS Redshift cluster](https://aws.amazon.com/redshift). Please follow instructions on [Udacity's redshift cluster tutorial](https://classroom.udacity.com/nanodegrees/nd027/parts/69a25b76-3ebd-4b72-b7cb-03d82da12844/modules/38c9fd5f-315b-4648-8b27-f3947c936a15/lessons/21d59f40-6033-40b5-81a2-4a3211d9f46e/concepts/fad03fb3-ce48-4a69-9887-4baf8751cae3)
to parametrise and launch the cluster.
Once the cluster created, enter your cluster parameters into a configuration file `dwh.cfg`. We provide you with a template `dwh_TEMPLATE.cfg` to fill (don't forget to move the file from `dwh_TEMPLATE.cfg` to `dwh.cfg` ).

**__BE CAREFUL TO KEEP dwh.cfg SECRET !!! IN PARTICULAR, DON'T PUT IT IN A PUBLIC REPOSITORY.__**

## Data
The data used to populate the database is stores in an S3 bucket :
`s3://udacity-dend/song_data`
`s3://udacity-dend/log_data`

## How to run the code


To create the sparkifydb database, open a terminal and run 

    python create_tables.py
    
To populate the database with data, run in the terminal :
    
    python etl.py
    
The `etl` phase will first copy raw data from S3 bucket into staging databases. Then, the staging 

### Example queries
The star database design makes the database queries easy. For instance, if the analytics teams want to know what songs in the database have been played through the app, they can issue a simple sql query :

    SELECT sp.song_id, songs.title FROM songplays sp JOIN songs ON sp.song_id = songs.song_id; 

Output :

    song_id            |     title      
    --------------------+----------------
    SOZCTXZ12AB0182364 | Setanta matins
    (1 row)

To retrieve more detailed information, i.e. the song's artist and the playtime, use a `JOIN`query :

    SELECT s.title AS song, a.name AS artist, t.hour,t.minute, t.second,
    u.first_name AS "user first name", u.last_name AS "user last name"
    FROM songplays sp JOIN songs s ON sp.song_id = s.song_id  
    JOIN artists a on s.artist_id = a.artist_id
    JOIN time t ON t.timestamp = sp.start_time 
    JOIN users u on u.user_id = sp.user_id;

Output :

          song      | artist | hour | minute | second | user first name | user last name 
    ----------------+--------+------+--------+--------+-----------------+------------
    Setanta matins | Elena  |   21 |     56 |     47 | Lily            | Koch
    (1 row)    

To retrieve all the paying users in the database :

    SELECT * from users WHERE users.level = 'paid';
    
Output :

     user_id | first_name | last_name | gender | level 
    ---------+------------+-----------+--------+-------
        29 | Jacqueline | Lynch     | F      | paid
        58 | Emily      | Benson    | F      | paid
        97 | Kate       | Harrell   | F      | paid
        73 | Jacob      | Klein     | M      | paid
      ...

To list all songs in the database :

    SELECT s.title, a.name, s.year, s.duration
    FROM songs s JOIN artists a
    ON s.artist_id = a.artist_id;
    
Output :

                  title               |      name      | year | duration 
    ----------------------------------+----------------+------+----------
    Ten Tonne                        | Chase & Status | 2005 |  337.684
    Get Your Head Stuck On Your Neck | Soul Mekanik   |    0 |  45.6616
    Sonnerie lalaleulé hi houuu      | Blingtones     |    0 |   29.544
    ...



# Changelog

# v1.0
First version submitted to Udacity platform.