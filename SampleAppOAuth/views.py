from django.http import HttpResponse, HttpResponseRedirect
from .services import QBAuth
from django.shortcuts import redirect, render

qb_auth = QBAuth()

def index(request):
    return render(request, 'index.html')
    
def connectToQuickbooks(request):
    authorize_url = qb_auth.getRequestTokens()
    return redirect(authorize_url)

def authHandler(request):
    if request is None:
        return HttpResponse("Authorization denied.")
    request.session['realm_id'] = request.GET.get('realmId',None)
    oauth_verifier = request.GET.get('oauth_verifier',None)
    session_object = qb_auth.getAccessTokens(oauth_verifier)
    request.session['access_token'] = session_object.access_token
    request.session['access_token_secret'] = session_object.access_token_secret
    return redirect('index')


