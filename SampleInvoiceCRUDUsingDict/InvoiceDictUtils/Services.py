from mysite import settings
from mysite.utils import httpRequests, context
import json

def makeRequest(url, method, reqContext, invoice_obj=None):
    # reqContext = context.Context()
    if invoice_obj is not None:
        json_str = json.dumps(invoice_obj)
        json_obj = json.loads(json_str)
        res = httpRequests.requestQBO(method, url, reqContext, payload=json_obj)
    else:
        res = httpRequests.requestQBO(method, url, reqContext) 
    return res

def getExistingRef(entity, context):
    entityName = entity.title()
    if settings.oauth_flag == 1:
        realm_id = context.realmId
    else:
        realm_id = settings.realm_id
    url = settings.base_url+realm_id+'/query?query='+'select * from '+entity
    res = makeRequest(url, 'GET', context)
    response = res.json()
    result = response['QueryResponse']
    i=0
    if len(result) < 1:
        print("Empty query response.")
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

	
