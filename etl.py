import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''Processes song file and sets up song_data and artist_data tables'''
    # open song file
    df = pd.read_json(filepath, typ='series')

    # insert song record
    song_data = [df['song_id'], df['title'], df['artist_id'] , df['year'], df['duration']]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = [df['artist_id'], df['artist_name'], df['artist_location'], df['artist_latitude'], df['artist_longitude']]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    '''Processes each log file passed in filepath and populates songplays table. As the log file does not have song id or artist id, song's title and       duration are compared to corresponding entries in songs table, artist name is compared to corresponding entry in artist database to pick up
    song_id and artist_id. Also each line contains user id, first name, last name, which are used to populate user table'''
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong'] 
    # convert timestamp to series
    df1 = pd.Series(pd.to_datetime(df['ts'], unit='ms'))
    
    # convert timestamp column to datetime
    t = [pd.to_datetime(df['ts'], unit='ms'), df1.dt.hour, df1.dt.day, df1.dt.week, df1.dt.month, df1.dt.year, df1.dt.weekday]

    
    # insert time data records
    time_data = (df['ts'], df1.dt.hour, df1.dt.day, df1.dt.week, df1.dt.month, df1.dt.year, df1.dt.weekday)
    column_labels = {"start_time":df['ts'], "hour":t[1], "day":t[2], "week":t[3], "month":t[4], "year":t[5], "weekday":t[6]}
    time_df = pd.DataFrame.from_dict(column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # create user dictionary
    user_dict = {"user_id":df['userId'], "first_name":df['firstName'], "last_name":df['lastName'], "gender":df['gender'], "level":df['level']}
    # load user table
    user_df = pd.DataFrame.from_dict(user_dict)
     

    # insert user records
    for i, row in user_df.iterrows():
        if(row['user_id'] != ''):
            cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
        if(songid == "" or songid == None) :
            continue    

        # insert songplay record
        songplay_data = (row['ts'], row['userId'], row['level'], songid, artistid, row['sessionId'], row['location'], row['userAgent'])
        
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''process song data and log data. filepath might have log data file name or song data. Appropriate function to process this data is passed in parameter func'''
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