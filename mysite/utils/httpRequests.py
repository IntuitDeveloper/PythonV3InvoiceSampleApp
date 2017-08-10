import requests
from requests_oauthlib import OAuth1

# POST for qbo sandbox
from mysite import settings

def requestQBO(method, url, context, payload=None):
    
    if settings.oauth_flag == 2:
        headers = {'Accept': 'application/json', 'User-Agent': 'PythonSampleApp2.0', 'Authorization': 'Bearer '+settings.access_token_oauth2}
        req = requests.request(method,url, headers=headers, json=payload)
    else:
        headers = {'Accept': 'application/json', 'content-type': 'application/json; charset=utf-8', 'User-Agent': 'PythonSampleApp2.0'}
        auth=OAuth1(context.consumerToken, context.consumerSecret, 
        context.accessToken, context.accessSecret)
        req = requests.request(method,url, auth=auth, headers=headers, json=payload)
    return req



    
        
