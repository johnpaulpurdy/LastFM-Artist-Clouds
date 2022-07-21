import sqlite3
import json
import requests
import requests_cache
# import datetime
import time
import os
import UtilsLastFm

requests_cache.install_cache()
USER_AGENT = os.environ['UserAgent']
fetch_limit = 5
connection = sqlite3.connect("LastFMArtistClouds.db")
database = connection.cursor()


def lastfm_get(payload):
    #define headers and URL
    headers = { 'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = os.environ['lastFMApiKey']
    payload['format'] = 'json'
    response = requests.get(url, headers=headers, params=payload )
    return response

def getArtistStats(artist):
    r = lastfm_get({'method': 'artist.getInfo', 'artist': artist, 'limit': fetch_limit})
    print(r.status_code)
    similarArtists = [t['name'] for t in r.json()['artist']['similar']['artist']]
    listeners = r.json()['artist']['stats']['listeners']
    playcount = r.json()['artist']['stats']['playcount']
    return similarArtists, listeners, playcount

def pullArtists(artistList):
    database.execute("SELECT artist_name from artist_names")
    rows = database.fetchall()
    for artistName in rows:
        if (artistName[0] not in artistList):
            artistList.append(artistName[0])
    return artistList
    
def addArtist(artistAdd):
    artistList = []
    artistList = pullArtists(artistList)
    if artistAdd not in artistList:
        database.execute("INSERT INTO artist_names( artist_name ) VALUES (?)", (artistAdd, ))
    else:
        print(artistAdd)
        print('0000 Already in 0000')

def addStats(artistAdd, listeners, playcount):
    current_timestamp = time.time()  
    print([artistAdd, current_timestamp, listeners, playcount])
    database.execute("INSERT INTO stats_log( artist_name, timestamp, listeners, playcount) VALUES (?,?,?,?)", (artistAdd, current_timestamp, listeners, playcount, ))

def getRelated():
    database.execute("SELECT first_artist, second_artist from related_artist")
    relationList = []
    rows = database.fetchall()
    for artistRow in rows:
        if ({'firstArtist': artistRow[0], 'secondArtist': artistRow[1]} not in relationList):
            relationList.append({'firstArtist': artistRow[0], 'secondArtist': artistRow[1]})
        if ({'firstArtist': artistRow[1], 'secondArtist': artistRow[0]} not in relationList):
            relationList.append({'firstArtist': artistRow[1], 'secondArtist': artistRow[0]})
    return relationList
    
def addRelated(artistAdd, similarArtists):
    artistList = []
    artistList = pullArtists(artistList)
    relatedList = getRelated()
    for similarArtist in similarArtists:
        if similarArtist in artistList:
            relatedCandidate = {'firstArtist':artistAdd, 'secondArtist': similarArtist}
            if relatedCandidate not in relatedList:
                relatedList.append(relatedCandidate)
                database.execute("INSERT INTO related_artist (first_artist , second_artist) values (?,?)", (artistAdd, similarArtist, ))
            relatedCandidate = {'firstArtist': similarArtist, 'secondArtist': artistAdd}
            if relatedCandidate not in relatedList:
                relatedList.append(relatedCandidate)
                database.execute("INSERT INTO related_artist (first_artist , second_artist) values (?,?)", (similarArtist, artistAdd, ))
    return relatedList
    
artistAdd = input("Enter the artist name to add:")
addArtist(artistAdd)
similarArtists, listeners, playcount = getArtistStats(artistAdd)
addStats(artistAdd, listeners, playcount)
# print(similarArtists)
for relatedArtists in addRelated(artistAdd, similarArtists):
    print(relatedArtists)
connection.commit()
#Thouxanbanfauni woun't load similar
#Levi Carter nope
# yerbownik nope
# Moh Baretta
# Iayze
