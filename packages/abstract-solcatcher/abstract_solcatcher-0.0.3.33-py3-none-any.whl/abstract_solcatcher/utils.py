import asyncio,requests,json
from abstract_utilities import *
from abstract_apis import make_request,get_url,make_endpoint,get_headers,get_async_response
def getSolcatcherUrl(callType=None):
  if callType == 'flask':
    return getSolcatcherFlaskUrl()
  if callType != None:
    return getSolcatcherTsUrl()
  return 'http://solcatcher.io'
def getSolcatcherFlaskUrl():
  return 'http://solcatcher.io/flask'
def getSolcatcherTsUrl():
  return 'http://solcatcher.io/typescript'
def getEndpointUrl(endpoint=None,callType=None,url=None):
  url = url or getSolcatcherUrl(callType=callType)
  endpoint = make_endpoint(endpoint or '/')
  return get_url(url,endpoint)
def updateData(data,**kwargs):
  data.update(kwargs)
  return data
def getCallArgs(endpoint):
  return {'getMetaData': ['signature'], 'getPoolData': ['signature'], 'getTransactionData': ['signature'], 'getPoolInfo': ['signature'], 'getMarketInfo': ['signature'], 'getKeyInfo': ['signature'], 'getLpKeys': ['signature'], 'process': ['signature']}.get(get_endpoint(endpoint))
def ifListGetSection(listObj,section=0):
    if isinstance(listObj,list):
        if len(listObj)>section:
            return listObj[section]
    return listObj
def try_json_dumps(data):
  if isinstance(data,dict):
    try:
      data = json.dumps(data)
    except:
      pass
    return data
def get_datas(endpoint=None,data=None,headers=None,url=None,get_post=None,callType=None,*args,**kwargs):
  data = data or kwargs
  if not isinstance(data,dict):
    data={"args":make_list(data)}
  data = try_json_dumps(data)
  callType=eatAll(callType or 'flask',['/'])
  get_post = get_post or 'POST'
  url = getEndpointUrl(url=url,callType=callType)
  return {"url":url,
    "endpoint":endpoint,
    "data":data,
    "headers":headers or get_headers(),
    "get_post":get_post}
def rate_limit(*args,**kwargs):
  arg = [arg for arg in args] or 'default_method'
  if arg and kwargs or len(args)>1:
    log_response(arg,**kwargs)
    return
  response = postFlaskRequest(endpoint='rate_limit',data=arg)
  if isinstance(response,dict):
    url = response.get('url',response)
  return url
def postFlaskRequest(endpoint=None,data=None,headers=None,url=None,get_post=None,*args,**kwargs):
  datas = get_datas(endpoint=endpoint,data=data,headers=headers,url=url,get_post=get_post,*args,**kwargs)
  return make_request(**datas)
def postTypescriptRequest(endpoint=None,data=None,headers=None,url=None,get_post=None,*args,**kwargs):
  datas = get_datas(endpoint=endpoint,data=data,headers=headers,url=url,get_post=get_post,callType='typescript',*args,**kwargs)
  return make_request(**datas)

