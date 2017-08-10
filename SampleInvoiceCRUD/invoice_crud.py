from .models import Invoice, Ref, Address 
from mysite import settings
from mysite.utils import httpRequests, context
from .InvoiceUtils import services, LineDetailHelper
import json
import jsonpickle
from urllib.parse import quote

def createInvoice(context):
    invoice = Invoice()
    invoice.CustomerRef = Ref(value=services.getExistingRef('customer', context))
    invoice.TxnDate = "2017-12-12"
    invoice.PrivateNote = "This is a private note."
    invoice.LinkedTxn = None
    invoice.CustomerMemo = {"value":"This is a customer memo."}
    invoice.BillAddr = Address("111 Orange St", "Mountain view", "USA", "11231")
    invoice.ClassRef = Ref(value=services.getExistingRef('class', context))
    invoice.Deposit = None
    item = {'value': services.getExistingRef('item', context)}
    LineDetailHelper.createSalesLineItem(invoice, 100, ItemRef=item)

    # get realm for OAuth1 from view session and OAuth2 from settings
    if settings.oauth_flag == 1:
        realm_id = context.realmId
    else:
        realm_id = settings.realm_id
    url=settings.base_url+realm_id+"/invoice?minorversion=4"
    request = services.makeRequest(url, 'POST', context, invoice_obj=invoice)
    return request.json()

def queryInvoice(query, context):
    # get realm for OAuth1 from view session and OAuth2 from settings
    if settings.oauth_flag == 1:
        realm_id = context.realmId
    else:
        realm_id = settings.realm_id
    url = settings.base_url+realm_id+"/query?query="+quote(query)+"&minorversion=9"
    request = services.makeRequest(url, 'GET', context)
    queryResponse = request.json()
    if len(queryResponse["QueryResponse"].keys()) > 0:
        invoiceList = []
        for each in queryResponse["QueryResponse"]['Invoice']:
            deserialize_obj_string = "py/object"
            each["py/object"] = "SampleInvoiceCRUD.models.Invoice"
            lines = each["Line"]
            for line in lines:
                line[deserialize_obj_string] = "SampleInvoiceCRUD.models.LineItem"
            invoice_json_str = json.dumps(each)
            invoice_obj = jsonpickle.decode(invoice_json_str)
            invoiceList.append(invoice_obj)
        return invoiceList
    else:
        message = "Your query returned empty response."
        return message

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
    url = settings.base_url+realm_id+'/invoice?minorversion=9'

    invoiceToUpdate = readInvoice(invoiceId, context)
    invoiceToUpdate.PrivateNote = "Updated invoice with new private note."
    invoiceToUpdate.sparse = True
    if isinstance(invoiceToUpdate, str):
        print('No invoice found with Id '+str(invoiceId))
    else:
        try:    
            request = services.makeRequest(url, 'POST', context, invoice_obj=invoiceToUpdate)
            return request.json()
        except IndexError:
            return 'No invoice found with Id '+str(invoiceId)

def deleteInvoice(invoiceId, context):
    # get realm for OAuth1 from view session and OAuth2 from settings
    if settings.oauth_flag == 1:
        realm_id = context.realmId
    else:
        realm_id = settings.realm_id
    url = settings.base_url+realm_id+'/invoice?operation=delete&minorversion=9'
    invoice = readInvoice(invoiceId, context)
    if isinstance(invoice, str):
        print('No invoice found with Id '+str(invoiceId))
    else:
        try:
            syncToken = invoice.SyncToken
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
    request = services.makeRequest(url, 'GET', context)
    invoice_json = request.json()
    if request.status_code == 200:
        # Add key value for jsonpickle to work
        deserialize_obj_string = "py/object"
        invoice_json["Invoice"][deserialize_obj_string] = "SampleInvoiceCRUD.models.Invoice"
        lines = invoice_json["Invoice"]["Line"]
        for line in lines:
            line[deserialize_obj_string] = "SampleInvoiceCRUD.models.LineItem"

        invoice = invoice_json["Invoice"]
        invoice_json_str = json.dumps(invoice)
        invoice_obj = jsonpickle.decode(invoice_json_str)
        if(type(invoice_obj)) == Invoice:
            return invoice_obj
        else:
            return "Could not deserialize invoice. Please use this object as a dictionary."
    else:
        return 'No invoice found with Id '+str(invoiceId)

"""
Please see delete operation to see how to implement void, only the URL will change, payload remains the same.
url = settings.base_url+settings.realm_id+'/invoice?operation=void&minorversion=4'
"""
def voidInvoice():
    pass


