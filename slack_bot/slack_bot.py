'''MOdule that tells python jokes'''

import slack
import pyjokes
from config import OAUTH_TOKEN

oauth_token = OAUTH_TOKEN

client = slack.WebClient(token=oauth_token)
joke = pyjokes.get_joke()

response = client.chat_postMessage(channel='#random', text=f"Here is a Python joke: {joke}")
