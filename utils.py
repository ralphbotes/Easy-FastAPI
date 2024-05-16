from datetime import datetime
import inspect
from fastapi import Body, Request, HTTPException
import orjson
import os

def request_checker(request: Request, bod: dict = Body(...)):
    l_body = bod

    l_headers = request.headers
    if 'authorization' in l_headers:
        l_auth = orjson.loads(l_headers['authorization'])
        l_authorized = is_authorized(l_auth)
        if not l_authorized:
            raise HTTPException(
                status_code=401,
                detail={
                    "payload": {"message": "Not authorized"},
                    "error_code": 104
                }
            )
    else:
        raise HTTPException(
            status_code=401,
            detail={
                "payload": {"message": "No authorization header specified"
                },"error_code": 105
            }
        
        )
    if 'payload' in l_body:
        l_body = l_body['payload']
    else:
        raise HTTPException(
            status_code=401,
            detail={
                "payload": {"message": "Need payload object in body"},
                "error_code": 106
            }
        )
    return request, l_headers, l_body

def get_date_time(a_both = False):
    current_date = datetime.now()
    str_current_date = current_date.strftime("%Y%m%d%H%M%S")

    if a_both == False:
        return str_current_date

    return current_date, str_current_date

def get_line_info():
    print(f'Path: {inspect.stack()[1][1]}\nFunction: {inspect.stack()[1][3]}\nLine: {str(int(inspect.stack()[1][2])-1)}\n-------------------END-------------------\n')

def is_authorized(a_auth):
    configData = {}
    with open('./config/config.json') as json_file:
        l_json = json_file.read()
        configData = orjson.loads(l_json)

    if configData:
        if configData["user"] == a_auth["User"] and    \
            configData["password"] == a_auth["Password"]:
            return True

    return False

def pathCheck(a_path):
    if os.path.exists(a_path):
        return True
    else:
        return False