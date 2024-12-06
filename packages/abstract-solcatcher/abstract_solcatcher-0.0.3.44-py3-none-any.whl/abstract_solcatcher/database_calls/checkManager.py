import logging
# Suppress logs below WARNING level
logging.basicConfig(level=logging.WARNING)
from abstract_utilities import SingletonMeta
from abstract_solana import abstract_solana_rate_limited_call,RateLimiter,get_insert_list
from .solcatcherCalls import *
from abstract_apis import get_async_response,get_json_response,make_request,get_url,make_endpoint,get_headers,get_async_response
from abstract_database import get_from_db,get_table,get_db_vars,connectionManager,get_first_row_as_dict
import json,asyncio
def get_method(method=None):
  return method or 'default_method'
def get_resp(response=None):
  response = response or {}
  if isinstance(response,dict):
    response = {"response":response}
  return response
def call_rate_limit(method=None,status_code=False):
  data={"method": get_method(method)}
  return postFlaskRequest(endpoint='rate_limit', data=json.dumps(data),response_result='url',status_code=status_code)
def call_log_response(method=None,response=None):
  data={"method": get_method(method),"response":get_resp(response=response)}
  return getFlaskRequest(endpoint='log_response',data=data ,status_code=status_code)
class CheckSolcatcher(metaclass=SingletonMeta):
  def __init__(self,env_path=None, dbType=None, dbName=None):
    if not hasattr(self, 'initialized'):
      self.rateLimiter = RateLimiter()
      self.initialized = True
      self.solcatcher_on = True
      
      url,self.status_code = call_rate_limit('test_method',True)
      self.env_path= env_path or get_env_path()
      if self.status_code != 200 and url == None:
        self.solcatcher_on=False
      self.solcatcher_db_on = True
      self.dbType = dbType or 'database'
      self.dbName = dbName or 'partners'
      self.tables=get_insert_list()
      #input(get_first_row_as_dict(tableName=self.tables[5].get('tableName'), rowNum=1))
      self.dbVars = get_db_vars(env_path=self.env_path, dbType=self.dbType, dbName=self.dbName)
      protocol = 'postgres'
      if 'rabbit' in self.dbType.lower():
        protocol = 'amqp'
      self.dbVars['dburl'] = f"{protocol}://{self.dbVars['user']}:{self.dbVars['password']}@{self.dbVars['host']}:{self.dbVars['port']}/{self.dbVars['dbname']}"
      #self.conn_mgr = connectionManager(env_path=self.env_path, dbType=self.dbType, dbName=self.dbName, tables=self.tables, dbVars=self.dbVars)
      #input('asdffawdssdf')
      #conn = self.conn_mgr.check_conn(env_path=self.env_path, dbType=self.dbType, dbName=self.dbName)
      #if conn in [None,False]:
      self.solcatcher_db_on=False
  def get_rate_url(self,method=None,status_code=False):
    method = get_method(method)
    if self.solcatcher_on:
      try:
        return call_rate_limit(method,status_code)
      except:
        pass
    return CheckSolcatcher().rateLimiter.get_url(method)
  def log_response(self,method=None,response=None,status_code=False):
    if self.solcatcher_on:
      try:
        return call_log_response(method=method,response=response)
      except:
        pass
    return CheckSolcatcher().rateLimiter.log_response(method=method,response=response)
  def connect_db(self,env_path=None, dbType=None, dbName=None):
     try:
       conn = create_connection(env_path=env_path, dbType=dbType, dbName=dbName)
       return conn
     except:
        pass
  def call_solcatcher_api(self,method,*args,**kwargs):
    if self.solcatcher_db_on:
      try:
        return call_solcatcher_db_api(method,*args,**kwargs)
      except:
        pass
    return abstract_solana_rate_limited_call(method,*args,**kwargs)
##    return abstract_solana_rate_limited_call(method,*args,**kwargs)
def call_solcatcher_api(method,*args,**kwargs):
  return CheckSolcatcher().call_solcatcher_api(method,*args,**kwargs)
def rate_limit(method=None,status_code=False):
  return CheckSolcatcher().get_rate_url(method=method,status_code=status_code)
def log_response(method=None,response=None,status_code=False):
  return CheckSolcatcher().log_response(method=method,response=response,status_code=status_code)
def rate_limit_solcatcher_api(method,*args,**kwargs):
  response = call_solcatcher_api(method,*args,**kwargs)
  logged_response = log_response(method=method,response=response,status_code=kwargs.get('status_code'))
  return response
def get_method(method=None):
  return method or 'default_method'
class clientMgr(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self.initialized = True
            self.client = Client()
            self.functions = {}

    def get_client_function(self, method):
        if method not in self.functions:
            self.functions[method] = getattr(self.client, method, None)
        return self.functions.get(method)
    def inspect_function(self, method_name):
        try:
            if hasattr(self.client, method_name):
                func = self.get_client_function(method)
               
                
                if func and callable(func):
                    try:
                        # Retrieve the signature without calling the method
                        signature = inspect.getargspec(func).args
                        parameters = list(signature.parameters.keys())

                        
                        return parameters
                    except ValueError:
                        return f"Could not retrieve signature for method {method_name}."
                else:
                    return f"{method_name} not found or not callable."
            else:
                return f"{method_name} not found in client."
        except:
            return f"couldnt get the signature for {method_name}"
    def get_body(self,method,*args,**kwargs):
        function = self.get_client_function(method)
        return function(*args,**kwargs)
    def get_partial_call(self,method,body):
        url = rate_limit(method)
        response = postRpcRequest(url=url,**body)
        log_response(method, response)
        return response
    def call_solana(self,method,*args,**kwargs):
        body = self.get_body(method,*args,**kwargs)
        response = self.get_partial_call(method,body)
        return response
def call_solcatcher_api(method,*args,**kwargs):
  return CheckSolcatcher().call_solcatcher_api(method,*args,**kwargs)
def call_solana(method,*args,**kwargs):
  return clientMgr().call_solana(method,*args,**kwargs)
def get_body(method,*args,**kwargs):
  return clientMgr().get_body(method,*args,**kwargs)
def partial_call_solana(method,body):
  return clientMgr().get_partial_call(method,body)
def fetch_from_db(*args,**kwargs):
    return get_async_response(getSolcatcherPost,'fetch_from_db',*args,**kwargs)
def insert_db(*args,**kwargs):
    return get_async_response(getSolcatcherPost,'insert_into_db',*args,**kwargs)
def get_db_params(method,*args,**kwargs):
    dbName=kwargs.get('dbName','solcatcher')
    insertTable = get_table(method,get_insert_list())
    if isinstance(insertTable,dict):
        freshCall = insertTable.get('freshCall')
        tableName=insertTable.get('tableName')
        insertName=insertTable.get('insertName')
        rpcCall = insertTable.get('rpcCall')
        return dbName,insertTable,freshCall,tableName,insertName,rpcCall
def call_solcatcher_db_api(method,*args,**kwargs):
    dbName,insertTable,freshCall,tableName,insertName,rpcCall = get_db_params(method,*args,**kwargs)
    if rpcCall:
        rpc_dict = get_body(method,*args,**kwargs)
        searchValue= rpc_dict.get('params')[0]
        insertValue  = get_from_db(freshCall,tableName,searchValue,fetch_from_db)
        if insertValue is None:
            insertValue = partial_call_solana(method,rpc_dict)
            rate_limit(method=method,response = {"result":insertValue})
            
            if isinstance(insertValue,dict) and insertValue.get('error'):
                return insertValue
            if isinstance(searchValue,dict):
                searchValue = generate_data_hash(insertName,insertValue)
            insert_db(dbName,insertTable,key=searchValue, value=insertValue,tableName=tableName)
    else:
        searchValue= args[0] if args else None
        insertValue  = get_from_db(freshCall,tableName,searchValue,fetch_from_db)
        if insertValue is None:
            insertValue = rate_limit_solcatcher_api(method,*args,**kwargs)
            rate_limit(method,insertValue)
            insert_db(dbName,insertTable,key=searchValue, value=insertValue,tableName=tableName)
    return insertValue
CheckSolcatcher()


