# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"
level_table_drop = "DROP TABLE IF EXISTS levels"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays(
        songplay_id bigserial,
        start_time bigint NOT NULL,
        user_id varchar NOT NULL,
        level varchar NOT NULL,
        song_id varchar,
        artist_id varchar,
        session_id bigint NOT NULL,
        location varchar,
        user_agent varchar,
        FOREIGN KEY (start_time) REFERENCES time(start_time)
        ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
        FOREIGN KEY (level) REFERENCES levels(level)
        On DELETE CASCADE,
        FOREIGN KEY (song_id) REFERENCES songs(song_id)
        ON DELETE CASCADE,
        FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
        ON DELETE CASCADE,
        PRIMARY KEY (start_time, user_id, session_id)
   )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users(
        user_id varchar PRIMARY KEY,
        first_name varchar,
        last_name varchar,
        gender varchar, 
        level varchar
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs(
        song_id varchar PRIMARY KEY,
        title varchar NOT NULL,
        artist_id varchar,
        year int,
        duration numeric
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists(
        artist_id varchar PRIMARY KEY,
        name varchar NOT NULL,
        location varchar,
        latitude numeric,
        longitude numeric
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time(
        start_time bigint PRIMARY KEY,
        hour double precision,
        day double precision,
        week double precision,
        month double precision,
        year double precision,
        weekday double precision
    )
""")

level_table_create = ("""
    CREATE TABLE IF NOT EXISTS levels(
        level varchar PRIMARY KEY
    )
""")

# INSERT RECORDS
songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time, user_id, session_id) DO NOTHING
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE SET 
    first_name=EXCLUDED.first_name,
    last_name=EXCLUDED.last_name,
    gender=EXCLUDED.gender,
    level=EXCLUDED.level
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO UPDATE SET 
    title=EXCLUDED.title,
    artist_id=EXCLUDED.artist_id,
    year=EXCLUDED.year,
    duration=EXCLUDED.duration
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO UPDATE SET 
    name=EXCLUDED.name,
    location=EXCLUDED.location,
    latitude=EXCLUDED.latitude,
    longitude=EXCLUDED.longitude
""")


time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time) DO UPDATE SET 
    hour=EXCLUDED.hour,
    day=EXCLUDED.day,
    week=EXCLUDED.week,
    month=EXCLUDED.month,
    year=EXCLUDED.year,
    weekday=EXCLUDED.weekday
""")

_level_free_value_insert = ("""
    INSERT INTO levels (level)
    VALUES ('free')
    ON CONFLICT (level) DO NOTHING
""")

_level_paid_value_insert = ("""
    INSERT INTO levels (level)
    VALUES ('paid')
    ON CONFLICT (level) DO NOTHING
""")

_songplay_index_insert = ("""
    CREATE UNIQUE INDEX index_songplays_on_start_time_and_user_id_and_session_id
    ON songplays
    USING btree
    (start_time, user_id, session_id);
""")

_song_index_insert = ("""
    CREATE UNIQUE INDEX index_songs_on_artist_id_and_title
    ON songs
    USING btree
    (artist_id, title);
""")
# FIND SONGS
song_select = ("""
    SELECT (songs.song_id, songs.artist_id)
    FROM songs
    JOIN artists ON songs.artist_id = artists.artist_id
    WHERE songs.title = (%s) AND artists.name = (%s) AND songs.duration = (%s)
""")

# QUERY LISTS
create_index_queries = [_songplay_index_insert, _song_index_insert]
insert_enum_queries = [_level_free_value_insert, _level_paid_value_insert]
create_table_queries = [level_table_create, user_table_create, time_table_create, artist_table_create, song_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop, level_table_drop]