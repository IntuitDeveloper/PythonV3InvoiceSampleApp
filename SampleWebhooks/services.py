from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode
import hashlib, hmac, base64
from mysite import settings


def isValidPayload(signature, payload):
	
	key = settings.webhooks_verifier
	key_to_verify = key.encode('ascii')
	hashed = hmac.new(key_to_verify, payload, hashlib.sha256).digest()
	hashed_base64 = base64.b64encode(hashed).decode()

	if signature == hashed_base64:
		return True
	return False
