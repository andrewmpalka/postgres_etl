# Sparkify ETL

Sparkify ETL is a jupyter workspace for extracting JSON data, transforming it into database-ready chunks, and loading it into our Postgresql RDBMS.

# Goal
Sparkify ETL will read files from `data/songs` and `data/logs`, transform the data if necessary, and add them to the proper places in the schema.

# Raw Data
*Song data*
Song data comes from [Million Song Dataset](http://millionsongdataset.com/).
Below is an example of what Song data would looke like
```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

*Log data*
Log data comes from this [event simulator](https://github.com/Interana/eventsim).
Below is an example of what Log data would looke like
```
{"artist": "Pavement", "auth": "Logged In", "firstName": "Sylvie", "gender": "F", "itemInSession": "0", "lastName": "Cruz", "length": 277.15873, "level": "free", "location": "Washington-Arlington-Alexandria-DC-VA-MD-WV", "method": "PUT", "page": "NextSong", "registration": 1.540266e+12, "sessionId": 345, "song": "Mercy:The Laundromat", "status": 200, "ts": 1541990258796, "userAgent": "Mozilla/5.0(Macintosh;Intel MacOs...", "userId": 10}
```

# Schema Design
Star schema-style was chosen to provide easy to access analytics without the need for complex multi-joins.

*Levels*: tiers of paid user access
- level     -- allows us to have the flexibility of an enum with the added ability to remove or alter values

*Users*:  users in the app
- user_id -- Primary Key
- first_name
- last_name
- gender
- level -- Reference to `levels.level`

*Time*: timestamps of records in `songplays` broken down into specific units
- start_time -- Primary Key
- hour
- day
- week
- month
- year
- weekday

*Artists*: artists in music database
- artist_id -- Primary Key
- name
- location
- lattitude
- longitude

*Songs*: songs in music database
- song_id -- Primary Key
- title
- artist_id
- year
- duration
- index_songs_on_artist_id_and_title -- Unique index

*Songplays*: records in log data associated with song plays i.e. records with page `NextSong`
- songplay_id -- Primary Key
- start_time -- Reference to `times.start_time`
- user_id -- Reference to `users.user_id`
- level -- Reference to `levels.level`
- song_id -- Reference to `songs.song_id`
- artist_id
- session_id
- location
- user_agent
- index_songplays_on_start_time_and_user_id_and_session_id -- Unique Index

### Tech

Dillinger uses a number of open source projects to work properly:

* [Conda] - Because I didn't make the original workspace!
* [Pysopg2] - the holy grail of postgresql drivers for python

### Installation

Sparkify requires [Python3](https://www.python.org/downloads/release/python-363/) v3.6.3+ to run.

Install the dependencies and then:

Create the DB and tables 
```sh
$ python create_tables.py
```
Run the script
```sh
$ python etl.py
```

License
----

MIT