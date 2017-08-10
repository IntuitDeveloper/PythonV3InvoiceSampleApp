import json
import jsonpickle
from mysite import settings
from mysite.utils import httpRequests

def toJson(obj):
    json_obj = jsonpickle.encode(obj, unpicklable=False)
    return json_obj

def makeRequest(url, method, reqContext, invoice_obj=None):
    if reqContext.accessToken is None:
        print('OAuth1 access token not found, please run the ')
    if invoice_obj is not None:
        json_str = toJson(invoice_obj)
        json_obj = json.loads(json_str)
        res = httpRequests.requestQBO(method, url, reqContext, payload=json_obj)
    else:
        res = httpRequests.requestQBO(method, url, reqContext) 
    return res

def getExistingRef(entity, reqContext):
    entityName = entity.title()
    if settings.oauth_flag == 1:
        realm_id = reqContext.realmId
    else:
        realm_id = settings.realm_id
    url = settings.base_url+realm_id+'/query?query='+'select * from '+entity
    res = makeRequest(url, 'GET', reqContext)
    response = res.json()
    result = response['QueryResponse']
    i=0
    if len(result) < 1:
        print("Empty query response for "+entity+".")
        return None
    else:
        if entity == 'item':
            for item in result[entityName]:
                try:
                    if item["Type"] in ["Category", "Inventory"]:
                        continue
                except (KeyError,NameError):
                    return int(item["Id"])
        return int(result[entityName][i]["Id"])