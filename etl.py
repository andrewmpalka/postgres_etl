import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    The Function accepts files in JSON format, reads song details and artist details; 
    finally inserts records to songs and artists tables.

    Args:
        cur: Database cursor.
        filepath: JSON file's location.

    Returns:
        None
    """
    
    df = pd.read_json(filepath, typ='series')
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values
    song_data.tolist()
    artist_data.tolist()
    cur.execute(song_table_insert, song_data)
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    The Function accepts files in JSON format, reads time details and user details; 
    inserts records to songs and artists tables; finally inserts records to songplays table.

    Args:
        cur: Database cursor.
        filepath: JSON file's location.

    Returns:
        None
    """
    
    df = pd.read_json(filepath, lines=True)
    df = df.loc[df['page'] == 'NextSong']
    t = pd.Series(pd.to_datetime(df['ts'], unit='ms'))
    time_data = (df['ts'].values, t.dt.hour.values, t.dt.day.values, t.dt.week.values, t.dt.month.values, t.dt.year.values, t.dt.weekday.values)
    column_labels = ['timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame({
                        column_labels[0]: time_data[0],
                        column_labels[1]: time_data[1],
                        column_labels[2]: time_data[2],
                        column_labels[3]: time_data[3],
                        column_labels[4]: time_data[4],
                        column_labels[5]: time_data[5],
                        column_labels[6]: time_data[6]
                       })

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    for index, row in df.iterrows():
        
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        try:
            songid, artistid = results
        except ValueError as ve:
            songid, artistid = None, None
        except TypeError as te:
            songid, artistid = None, None

        songplay_data = (int(row.ts//1000), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    The Function accepts the proper psycopg2 parameters for the database, the base filepath
    for the selected directory and the appropriate function to call on an individual file
    in said directory; used to iteratively call a function to process and store data within
    the associated filepath;

    Args:
        cur: Database cursor.
        conn: Database connection.
        filepath: JSON file's location.
        func: Function to call on the json data within the filepath.

    Returns:
        None
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()