# DROP TABLES

songplay_table_drop = ""
user_table_drop = ""
song_table_drop = ""
artist_table_drop = ""
time_table_drop = ""

# CREATE TABLES

songplay_table_create = """create table if not exists songplays(song_play_id SERIAL PRIMARY KEY, start_time bigint, user_id bigint NOT NULL, level varchar(64), song_id varchar(100) NOT NULL, artist_id varchar(100) NOT NULL, session_id varchar(256), location varchar(256), user_agent varchar(256))"""

user_table_create = """create table if not exists users (user_id bigint PRIMARY KEY, first_name varchar(256), last_name varchar(256), gender varchar(8), level varchar(64))"""

song_table_create = """create table if not exists songs (song_id varchar(100) PRIMARY KEY, title varchar(256), artist_id varchar(100) NOT NULL, year int, duration numeric(30, 10))"""

artist_table_create = """create table if not exists artists (artist_id varchar(100) PRIMARY KEY, name varchar(256), location varchar(256), latitude float, longitude float)"""

time_table_create = """create table if not exists time (start_time bigint PRIMARY KEY, hour int, day int, week int, month int, year int, weekday int)"""


songplay_table_drop = """drop table if exists songplay"""

users_table_drop = """drop table if exists users"""

song_table_drop = """drop table if exists songs"""

artist_table_drop = """drop table if exists artists"""

time_table_drop = """drop table if exists time"""

# INSERT RECORDS
