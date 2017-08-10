from django.shortcuts import render, redirect
from django.template import Context, Template
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from .services import isValidPayload
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# Create your views here.
#from .models import WebhooksContext
@csrf_exempt
@require_POST
def index(request):
	payload = request.body
	signature = request.META.get('HTTP_INTUIT_SIGNATURE')

	if signature is None:
		return HttpResponseForbidden('Permission denied.')
	
	if isValidPayload(signature, payload):	
		print(payload.decode())
		request.session['WebhooksPayload'] = (payload.decode(), None)
		return HttpResponse(payload.decode())

	else:
		return HttpResponseBadRequest('Payload not validated.')



