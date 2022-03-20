import json

def build_response(statusCode, success, payload):

    body = {
        "success": success,
        "payload": payload
    }

    response = {
        "statusCode": statusCode,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
            "Content-type": "application/json"
        },
        "body": json.dumps(body)
    }

    return response

def success(return_body) :
    return build_response(200, True, return_body)

def failure(return_body) :
    return build_response(500, False, return_body)
