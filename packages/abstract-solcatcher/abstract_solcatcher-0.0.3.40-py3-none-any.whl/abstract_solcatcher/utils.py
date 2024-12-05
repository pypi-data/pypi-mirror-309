import asyncio,requests,json
from abstract_utilities import *
from abstract_solana import RateLimiter
from abstract_apis import make_request,get_url,make_endpoint,get_headers,get_async_response
def get_method(method=None):
  return method or 'default_method'
def get_resp(response=None):
  response = response or {}
  if isinstance(response,dict):
    response = {"response":response}
  return response
def try_solcatcher_io(method = None):
  method = get_method(method=method)
  try:
    url,status_code = postFlaskRequest(url=getSolcatcherFlaskUrl(),endpoint='get_rate_limit',data=json.dumps({"method":method}),status_code=True)
    return url,status_code 
  except:
    pass
  return None,500
def try_log_response(method = None,response=None):
  method = get_method(method=method)
  response = get_resp(response=response)
  try:
    response = postFlaskRequest(url=getSolcatcherFlaskUrl(),endpoint='log_response',data=json.dumps({"method":method,"response":response}),status_code=True)
    return response 
  except:
    pass
def get_url(url=None):
    if isinstance(url,dict):
      url = url.get('url',url)
    return url
class CheckSolcatcher(metaclass=SingletonMeta):
  def __init__(self):
    if not hasattr(self, 'initialized'):
      self.initialized = True
      self.solcatcher_on = True
      url,self.status_code = try_solcatcher_io()
      if self.status_code != 200 and get_url(url=url) == None:
        self.solcatcher_on=False
      self.rateLimiter = RateLimiter()
      
  def get_rate_url(self,method=None):
    
    if self.solcatcher_on:
      url,response_code = try_solcatcher_io(method = method)
    if self.solcatcher_on == False or self.status_code != 200:
       self.solcatcher_on = False
       method = get_method(method=method)
       url = self.rateLimiter.get_url(method=method)
    return get_url(url=url)
  
  def log_response(method=None,response=None):
    if self.solcatcher_on:
       try_log_response(method = method,response=response)
    if self.solcatcher_on == False:
      method = get_method(method=method)
      response = get_resp(response=response)
      self.rateLimiter.log_response(method=method)  
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

def rate_limit(method=None,response=None):
  if response is not None:
      CheckSolcatcher().log_response(method=method,response=response)
      return
  return CheckSolcatcher().get_rate_url(method=method)
def postFlaskRequest(endpoint=None,data=None,headers=None,url=None,get_post=None,*args,**kwargs):
  datas = get_datas(endpoint=endpoint,data=data,headers=headers,url=url,get_post=get_post,*args,**kwargs)
  return make_request(**datas)
def postTypescriptRequest(endpoint=None,data=None,headers=None,url=None,get_post=None,*args,**kwargs):
  datas = get_datas(endpoint=endpoint,data=data,headers=headers,url=url,get_post=get_post,callType='typescript',*args,**kwargs)
  return make_request(**datas)

