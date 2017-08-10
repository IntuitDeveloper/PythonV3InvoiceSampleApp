from mysite import settings
from .InvoiceDictUtils import Services
from mysite.utils import httpRequests, context
import json
import jsonpickle
from urllib.parse import quote

def createInvoice(context):
    # Passing a request dictionary for invoice request instead of building it like shown here will work. 
    invoice = {}
    customerId = Services.getExistingRef('customer', context)
    invoice['CustomerRef'] = {
        'value': customerId
    }
    invoice['TxnDate'] = "2017-12-12"
    invoice['PrivateNote'] = "This is a private note."
    invoice['CustomerMemo'] = {
        "value": "This is a customer memo."
    }
    invoice['BillAddr'] = {
        "Line1": "111 Orange St", 
        "City": "Mountain view",
        "Country": "USA", 
        "PostalCode":"11231"
    }
    classRefId = Services.getExistingRef('class', context)
    invoice['ClassRef'] = {'value': classRefId}
    item = Services.getExistingRef('item', context)
    line = [
        {
            'DetailType': 'SalesItemLineDetail',
            'Amount': 100,
            'SalesItemLineDetail': {
                'ItemRef': {
                    'value': item
                }
            }

        },
        {
            'DetailType': 'SalesItemLineDetail',
            'Amount': 50,
            'SalesItemLineDetail': {
                'ItemRef': {
                    'value': item
                }
            }

        },
    ]
    invoice['Line'] = line

    # get realm for OAuth1 from view session and OAuth2 from settings
    if settings.oauth_flag == 1:
        realm_id = context.realmId
    else:
        realm_id = settings.realm_id
    url=settings.base_url+realm_id+"/invoice?minorversion=4"
    request = Services.makeRequest(url, 'POST', context, invoice_obj=invoice)
    return request.json()

def queryInvoice(query, context):
    if settings.oauth_flag == 1:
        realm_id = context.realmId
    else:
        realm_id = settings.realm_id
    url = settings.base_url+realm_id+"/query?query="+quote(query)+"&minorversion=4"
    request = Services.makeRequest(url, 'GET', context)
    return request.json()['QueryResponse']['Invoice']

# Similar to create, need to provide Id, SyncToken and other updated fields
def updateInvoice(invoiceId, context):
    """
    Only sparse update is shown here. For full update, please follow the create method and include required fields: SyncToken, Id and sparse: False

    Sparse update will update only the field provided in the request and will not change any fields not provided in the request whereas full update will change all the field and if a full update is done on an invoice and some fields are not provided, then these field will reset to default.
    """
    # get realm for OAuth1 from view session and OAuth2 from settings
    if settings.oauth_flag == 1:
        realm_id = context.realmId
    else:
        realm_id = settings.realm_id
    url = settings.base_url+realm_id+'/invoice?minorversion=4'
    invoiceToUpdate = readInvoice(invoiceId, context)['Invoice']
    invoiceToUpdate['sparse'] = True
    invoiceToUpdate['PrivateNote'] = "Updated invoice with new private note."
    if isinstance(invoiceToUpdate, str):
        print('No invoice found with Id '+str(invoiceId))
    else:
        try:
            request = Services.makeRequest(url, 'POST', context, invoice_obj=invoiceToUpdate)
            return request.json()
        except IndexError:
            return 'No invoice found with Id '+str(invoiceId)

def deleteInvoice(invoiceId, context):
    # get realm for OAuth1 from view session and OAuth2 from settings
    if settings.oauth_flag == 1:
        realm_id = context.realmId
    else:
        realm_id = settings.realm_id
    url = settings.base_url+realm_id+'/invoice?operation=delete&minorversion=4'
    invoice = readInvoice(invoiceId, context)
    if isinstance(invoice, str):
        print('No invoice found with Id '+str(invoiceId))
    else:
        try:
            syncToken = invoice['Invoice']['SyncToken']
            payload = {
                        "Id": str(invoiceId),
                        "SyncToken": str(syncToken)
            }
            res = httpRequests.requestQBO('POST', url, context, payload=payload)
            response = res.json()
            return response
        except IndexError:
            return 'No invoice found with Id '+str(invoiceId)

def readInvoice(invoiceId, context):
    # get realm for OAuth1 from view session and OAuth2 from settings
    if settings.oauth_flag == 1:
        realm_id = context.realmId
    else:
        realm_id = settings.realm_id
    url=settings.base_url+realm_id+"/invoice/"+str(invoiceId)+"?minorversion=9"
    request = Services.makeRequest(url, 'GET', context)
    if request.status_code == 200:
        return request.json()
    else:
        return 'No invoice found with Id '+str(invoiceId)

"""
Please see delete operation to see how to implement void, only the URL will change, payload remains the same.
url = settings.base_url+settings.realm_id+'/invoice?operation=void&minorversion=4'
"""
def voidInvoice():
    pass
