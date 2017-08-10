# Get from settings
# The context class sets the realm id with the consumer tokens every time user authorizes an app for their QB company
from mysite import settings

# In production app, context is set after getting access tokens and realm ID along with app's consumer token and secret. Here, Context is just for demo purposes, it's getting hard coded tokens from settings.py
class Context:
    # For OAuth1 only
    def __init__(self, access_token=None, access_token_secret=None, realm_id=None):
        self.consumerToken = settings.consumer_key
        self.consumerSecret = settings.consumer_sec
        self.accessToken = access_token
        self.accessSecret = access_token_secret
        self.realmId = realm_id

