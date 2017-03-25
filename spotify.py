import requests

def get_track_url(song_title):
	spotify_url = 'https:///api.spotify.com/v1/search'
	params = {'q': song_title, 'tpye': 'track'}

	# request a JSON from Spotify from a search of the song title
	spotify_response = requests.get(spotify_url, params=params).json()
	# parse the JSON file to only use the url of the desired track
	track_url = spotify_response['tracks']['items'][0]['preview_url']
	return track_url