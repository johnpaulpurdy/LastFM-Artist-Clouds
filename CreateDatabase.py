import sqlite3
# Database connection
connection = sqlite3.connect("LastFMArtistClouds.db")
database = connection.cursor()

#check if database is created
database.execute("CREATE TABLE IF NOT EXISTS artist_names( artist_name VARCHAR NOT NULL, CONSTRAINT artist_pk PRIMARY KEY(artist_name))")
database.execute("CREATE TABLE IF NOT EXISTS related_artist( first_artist VARCHAR NOT NULL, second_artist VARCHAR NOT NULL, CONSTRAINT artists_pk PRIMARY KEY(first_artist, second_artist))")
database.execute("CREATE TABLE IF NOT EXISTS stats_log( artist_name VARCHAR NOT NULL, timestamp REAL, listeners INT(30), playcount INT(30), CONSTRAINT stats_pk PRIMARY KEY(artist_name, timestamp))") 
connection.commit()
database.execute("SELECT artist_name, timestamp, listeners, playcount from  stats_log ")
print(database.fetchall())