from .request_utils import *
import logging
# Suppress logs below WARNING level
logging.basicConfig(level=logging.WARNING)
def make_request(url, data=None, headers=None, get_post=None, endpoint=None, status_code=False, raw_response=False, response_result=None, load_nested_json=True,auth=None):
    response = None
    values = get_values_js(url=url,data=data,headers=headers,endpoint=endpoint,auth=auth)
    get_post = str(get_post or ('GET' if data == None else 'POST')).upper()
    if get_post == 'POST':
        response = requests.post(**values)
    elif get_post == 'GET':
        response = requests.get(**values)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    if status_code:
        return get_response(response, raw_response=raw_response, response_result=response_result, load_nested_json=load_nested_json), get_status_code(response)
    return get_response(response, raw_response=raw_response, response_result=response_result, load_nested_json=load_nested_json)

def postRequest(url, data, headers=None, endpoint=None, status_code=False, raw_response=False, response_result=None, load_nested_json=True,auth=None):
    return make_request(url, data=data, headers=headers, endpoint=endpoint, get_post='POST', status_code=status_code, raw_response=raw_response, response_result=response_result, load_nested_json=load_nested_json,auth=auth)

def getRequest(url, data, headers=None, endpoint=None, status_code=False, raw_response=False, response_result=None, load_nested_json=True,auth=None):
    return make_request(url, data=data, headers=headers, endpoint=endpoint, get_post='GET', status_code=status_code, raw_response=raw_response, response_result=response_result, load_nested_json=load_nested_json,auth=auth)

def getRpcRequest(url, method=None,params=None,jsonrpc=None,id=None,headers=None, endpoint=None, status_code=False, raw_response=False, response_result=None, load_nested_json=True,auth=None):
    data = getRpcData(method=method,params=params,jsonrpc=jsonrpc,id=id)
    return getRequest(url, data, headers=headers, endpoint=endpoint, status_code=status_code, raw_response=raw_response, response_result=response_result, load_nested_json=load_nested_json,auth=auth)

def postRpcRequest(url, method=None,params=None,jsonrpc=None,id=None,headers=None, endpoint=None, status_code=False, raw_response=False, response_result=None, load_nested_json=True,auth=None):
    data = getRpcData(method=method,params=params,jsonrpc=jsonrpc,id=id)
    return postRequest(url, data, headers=headers, endpoint=endpoint, status_code=status_code, raw_response=raw_response, response_result=response_result, load_nested_json=load_nested_json,auth=auth)
