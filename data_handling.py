from utils import pathCheck
from fastapi import HTTPException
import orjson

def getFirstTen(a_data):
    return list(a_data["todos"])[:10]

def getWhereIDIsFive(a_data):
    return [todo for todo in a_data["todos"] if todo["userId"] == 5]

def getRequestData(a_request_type):
    
    # Check if dir exists
    file_path = f'./data/my_data.json'
    path_exists = pathCheck(file_path)
    if not path_exists:
        raise HTTPException(
            status_code=401,
            detail={
                "payload": {"message": "Request type not supported."},
                "error_code": 102
            }
        )
    
    config_data = {}
    with open(file_path) as json_file:
        l_json = json_file.read()
        config_data = orjson.loads(l_json)

    match a_request_type:
        case "first_10_todos":
            config_data = getFirstTen(config_data)
        case "where_id_5":
            config_data = getWhereIDIsFive(config_data)
    
    if config_data:
        return {
            "payload": config_data,
            "error_code": 200
        }
    else:
        raise HTTPException(
            status_code=401,
            detail={
                "payload": {"message": "Request data corrupted."},
                "error_code": 103
            }
        )