# sms_music_bot.py
# App that will call you with a song after you request it via text

# Author: Noah Momblanco
#         http://github.com/nmombo/sms_music_bot

# Wrtten on 3/28/2017 during MHakcs 9 using guide at http://twilioinc.wpengine.com/2017/03/building-python-web-apps-with-flask.html

import spotify # import the spotify module we wrote
from flask import Flask, request # import flask server and http request libraries
from twilio import twiml # the python twilio interface
from twilio.rest import TwilioRestClient # import Twilio's REST API
import urllib

# instantiate a Twilio REST API Client with my Twilio account credentials
# note that the twilio token has been regenerated since comitting to the public github repository
myTwilioSID = 'ACd7173182fbfbee0265e86f88929fb005'
myTwilioToken = 'secret'
client = TwilioRestClient(account=myTwilioSID, token=myTwilioToken) 
# instantiate a flask server
app = Flask(__name__)

# A route to respond to SMS messages and kick off a phone call
@app.route('/sms', methods=['POST'])
def inbound_sms():
	response = twiml.Response()
	response.message('Thanks for texting Noah\'s SMS music bot! We\'re Searching for your song now. '
					 'Please wait to receive a phone call.\n\nView source code at http://github.com/nmombo/sms_music_bot')

	# Grab the song title from the body of the text message
	song_title = urllib.quote(request.form['Body'])

	# Grab the relevant phone numbers
	from_number = request.form['From']
	to_number = request.form['To']

	# Create a phone call that uses our other route to play a song from Spotify
	ngrok_url = 'http://3d4162fa.ngrok.io'
	client.calls.create(to=from_number, from_=to_number,
						url= ngrok_url + '/call?track={}'
						.format(song_title))

	# respond to http request
	return str(response)

# A route to handle the logic for phone calls
@app.route('/call', methods=['POST'])
def outbound_call():
	# use spotify module to get the url of top song result form a spotify search
	song_title = request.args.get('track')
	track_url = spotify.get_track_url(song_title)

	# play the song at the spotify url over the phone
	response = twiml.Response()
	response.play(track_url)

	# return a string version to close the http request
	return str(response)

# begin running this app on the flask server
app.run(host='0.0.0.0', debug=True)