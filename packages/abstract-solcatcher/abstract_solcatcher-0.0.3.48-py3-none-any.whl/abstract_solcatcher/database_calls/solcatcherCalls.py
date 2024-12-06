import logging
# Suppress logs below WARNING level
logging.basicConfig(level=logging.WARNING)
from abstract_apis import make_request,asyncPostRequest
from abstract_security import get_env_path
import asyncio
def getSolcatcherUrl(callType=None):
  if callType == 'flask':
    return getSolcatcherFlaskUrl()
  if callType != None:
    return getSolcatcherTsUrl()
  return 'https://solcatcher.io'
def getSolcatcherFlaskUrl():
  return 'https://solcatcher.io/flask'
def getSolcatcherTsUrl():
  return 'https://solcatcher.io/typescript'
async def getSolcatcherPost(endpoint, *args, **kwargs):
    # Ensure that the arguments are fully resolved and not coroutines
    resolved_args = [await arg if asyncio.iscoroutine(arg) else arg for arg in args]
    
    # Check for coroutines in kwargs and resolve them without reusing
    resolved_kwargs = {}
    for k, v in kwargs.items():
        if asyncio.iscoroutine(v):
            resolved_kwargs[k] = await v
        else:
            resolved_kwargs[k] = v
    
    # Now pass resolved data into the request
    return await asyncPostRequest(
        url=getSolcatcherFlaskUrl(),
        endpoint=endpoint,
        data={"args": resolved_args, **resolved_kwargs}
    )
def makeSolcatcherRequest(url, endpoint, data=None,get_post='POST', *args, **kwargs):
    """
    Makes a request to a Solcatcher endpoint.
    """
    return make_request(url=url, endpoint=endpoint,  get_post='POST', data=data, *args, **kwargs)

def postSolcatcherRequest(url,endpoint, *args, **kwargs):
    """
    Makes a POST request to a Solcatcher endpoint.
    """

    return makeSolcatcherRequest(url=url, endpoint=endpoint, get_post='POST', *args, **kwargs)

def getSolcatcherRequest(endpoint, *args, **kwargs):
    """
    Makes a GET request to a Solcatcher endpoint.
    """
    url = getSolcatcherUrl()
    return makeSolcatcherRequest(url=url, endpoint=endpoint, get_post='GET', *args, **kwargs)

def postFlaskRequest(endpoint, *args, **kwargs):
    """
    Makes a POST request to a Flask endpoint.
    """
    url = getSolcatcherFlaskUrl()
    return postSolcatcherRequest(url=url, endpoint=endpoint, *args, **kwargs)

def getFlaskRequest(endpoint, *args, **kwargs):
    """
    Makes a GET request to a Flask endpoint.
    """
    url = getSolcatcherFlaskUrl()
    return getSolcatcherRequest(url=url, endpoint=endpoint, *args, **kwargs)

def postTypescriptRequest(endpoint, *args, **kwargs):
    """
    Makes a POST request to a Typescript endpoint.
    """
    url = getSolcatcherTsUrl()
    data = kwargs  # Collect all keyword arguments as data
    return makeSolcatcherRequest(url=url, endpoint=endpoint, data=data)


def postTypescriptRequest(endpoint, *args, **kwargs):
    """
    Makes a POST request to a Typescript endpoint.
    """
    url = getSolcatcherTsUrl()
    data = kwargs  # Collect all keyword arguments as data
    return makeSolcatcherRequest(url=url, endpoint=endpoint, data=data)

c
