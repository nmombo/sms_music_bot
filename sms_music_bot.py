import spotify # import the spotify module we wrote
from flask import Flask, request
from twilio import twiml # the python twilio interface
from twilio.rest import TwilioRestClient # import Twilio's REST API
import urllib

# instantiate a Twilio REST API Client with my Twilio account credentials
client = TwilioRestClient(account='ACd7173182fbfbee0265e86f88929fb005',
						  token='ebc21124ac89fcca882a10812496c374') 
app = Flask(__name__)

# A route to respond to SMS messages and kick off a phone call
@app.route('/sms', methods=['POST'])
def inbound_sms():
	response = twiml.Response()
	response.message('Thanks for texting! Searching for your song now.'
					 'Wait to receive a phone call :)')

	# Grab the song title from the body of the text message
	song_title = urllib.quote(request.form['Body'])

	# Grab the relevant phone numbers
	from_number = request.form['From']
	to_number = request.form['To']

	# Create a phone call that uses our other route to play a song from Spotify
	client.calls.create(to=from_number, from_=to_number,
						url='http://f3a87bee.ngrok.io/call?track={}'
						.format(song_title))

	return str(response)

# A route to handle the logic for phone calls
@app.route('/call', methods=['POST'])
def outbound_call():
	song_title = request.args.get('track')
	track_url = spotify.get_track_url(song_title)

	response = twiml.Response()
	response.play(track_url)
	return str(response)

app.run(host='0.0.0.0', debug=True)