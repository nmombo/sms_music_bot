# spotify.py
# Module for the sms_music_bot.py app that interfaces with Spotify API's search

# Author: Noah Momblanco
#         http://github.com/nmombo/sms_music_bot

# Wrtten on 3/28/2017 during MHacks 9 using guide at http://twilioinc.wpengine.com/2017/03/building-python-web-apps-with-flask.html

import requests

def get_track_url(song_title):
	spotify_url = 'https://api.spotify.com/v1/search'
	params = {'q': song_title, 'type': 'track'}

	# request a JSON from Spotify from a search of the song title
	spotify_response = requests.get(spotify_url, params=params).json()
	# parse the JSON file to only use the url of the desired track
	track_url = spotify_response['tracks']['items'][0]['preview_url']
	return track_url