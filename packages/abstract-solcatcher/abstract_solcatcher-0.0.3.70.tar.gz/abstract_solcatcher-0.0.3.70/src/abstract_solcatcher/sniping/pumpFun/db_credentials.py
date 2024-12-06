from abstract_security import *
def get_dbConfig_keys():
  return ["dbname","user","password","host","port"]
def get_rabbitmq_keys():
  return ["user","password","host","queue"]
def get_db_env_key(key,dbProgram=None,dbType=None):
  dbProgram=dbProgram or 'solcatcher'
  dbType=dbType or 'database'
  return f"{dbProgram.upper()}_{dbType.upper()}_{key.upper()}"
def get_db_env_value(key,env_path=None):
  return get_env_value(key=key,path=env_path)
def get_env_data(keys,dbProgram=None,dbType=None,env_path=None):
  dbProgram=dbProgram or 'solcatcher'
  dbType=dbType or 'database'
  db_js = {}
  for key in keys:
    db_env_key = get_db_env_key(key=key,dbProgram=dbProgram,dbType=dbType)
    db_js[key]= get_db_env_value(key=db_env_key,env_path=env_path)
  return db_js
DB_CONFIG = get_env_data(get_dbConfig_keys(),dbProgram='solcatcher',dbType='database')
RABBIT_CONFIG = get_env_data(get_rabbitmq_keys(),dbProgram='solcatcher',dbType='rabbitmq')
