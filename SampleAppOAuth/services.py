from rauth import OAuth1Service
from mysite import settings

class QBAuth(object):
	qbo=OAuth1Service(
		name="qbo",
		consumer_key=settings.consumer_key,
		consumer_secret=settings.consumer_sec,
		request_token_url=settings.request_token_url,
		access_token_url=settings.access_token_url,
		authorize_url=settings.authorize_url,
		base_url=settings.base_url)

	def getRequestTokens(self):
		request_token, request_token_secret = self.qbo.get_request_token(params={'oauth_callback': "http://localhost:8000/oauth/authHandler"})
		self.request_token = request_token
		self.request_token_secret = request_token_secret
		print(request_token)
		authorize_url = self.qbo.get_authorize_url(request_token)
		return authorize_url
		
	def getAccessTokens(self, oauth_verifier):
		session_obj = self.qbo.get_auth_session(self.request_token, self.request_token_secret, data={'oauth_verifier': oauth_verifier})
		return session_obj
		
		# These tokens should be persisted in the database, this is just for this sample that a session is used.
		





		
	





