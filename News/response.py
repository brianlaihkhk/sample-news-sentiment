import json
from flask import Response

def build_response(success, payload):

    body = {
        "success": success,
        "payload": payload
    }

    return json.dumps(body)

def success(return_body) :
    return Response(build_response(True, return_body), status=200, mimetype='application/json')

def failure(return_body) :
    return Response(build_response(False, return_body), status=500, mimetype='application/json')
