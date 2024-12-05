import asyncio,requests
from abstract_solcatcher import *
from abstract_solcatcher import get_rate_limit,log_response,call_solcatcher_db_api
from abstract_apis import get_url,make_endpoint,get_headers,get_async_response
def getSolcatcherUrl():
  return 'http://solcatcher.io'
def getSolcatcherFlaskUrl():
  return 'http://solcatcher.io/flask'
def getSolcatcherTsUrl():
  return 'http://solcatcher.io/typescript'
def getEndpointUrl(endpoint=None,url=None):
  url = url or getSolcatcherUrl()
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
  url = getEndpointUrl(url,callType,endpoint)
  endpoint = eatAll(endpoint or '',['/'])
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
  return get_rate_limit(arg)
def postFlaskRequest(endpoint=None,data=None,headers=None,url=None,get_post=None,*args,**kwargs):
  datas = get_datas(endpoint=endpoint,data=data,headers=headers,url=url,get_post=get_post,*args,**kwargs)
  return make_request(**datas)
def postTypescriptRequest(endpoint=None,data=None,headers=None,url=None,get_post=None,*args,**kwargs):
  datas = get_datas(endpoint=endpoint,data=data,headers=headers,url=url,get_post=get_post,callType='typescript',*args,**kwargs)
  return make_request(**datas)
