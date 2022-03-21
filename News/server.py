from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import yaml
import sys
import traceback
import response
from misc import load_env
from flask import Flask, request
from flask_cors import CORS
from handler import Handler
from query import Query
import logging

app = Flask(__name__)
CORS(app)
request_handler = None

@app.route('/news', methods=['GET'])
@app.route('/news/', methods=['GET'])
@app.route('/news/<category>', methods=['GET'])
@app.route('/news/<category>/', methods=['GET'])
@app.route('/news/<category>/<uuid>', methods=['GET'])
@app.route('/news/<category>/<uuid>/', methods=['GET'])
def news(category = None, uuid = None):
    try:
        event = {}
        event['query'] = request_handler.handle_news(category, uuid)
        logging.info(event)
        print(event)
        return response.success(request_handler.query.get_news(event))
    except Exception as e:
        print(traceback.format_exc())
        logging.error(str(traceback.format_exc()))
        return response.failure("Request failed. " + str(e))


@app.route('/topic', methods=['GET'])
@app.route('/topic/', methods=['GET'])
@app.route('/topic/<date>', methods=['GET'])
@app.route('/topic/<date>/', methods=['GET'])
@app.route('/topic/<date>/<topic>', methods=['GET'])
@app.route('/topic/<date>/<topic>/', methods=['GET'])
def topic(date = None, topic = None):
    try:
        event = {}
        event['query'] = request_handler.handle_query(date, topic, 'TOPIC')
        logging.info(event)
        print(event)
        return response.success(request_handler.query.get_topic(event))
    except Exception as e:
        print(traceback.format_exc())
        logging.error(str(traceback.format_exc()))
        return response.failure("Request failed. " + str(e))

@app.route('/category', methods=['GET'])
@app.route('/category/', methods=['GET'])
@app.route('/category/<date>', methods=['GET'])
@app.route('/category/<date>/', methods=['GET'])
@app.route('/category/<date>/<category>', methods=['GET'])
@app.route('/category/<date>/<category>/', methods=['GET'])
def category(date = None, category = None):
    try:
        event = {}
        event['query'] = request_handler.handle_query(date, category, 'CATEGORY')
        logging.info(event)
        print(event)
        return response.success(request_handler.query.get_category(event))
    except Exception as e:
        print(traceback.format_exc())
        logging.error(str(traceback.format_exc()))
        return response.failure("Request failed. " + str(e))

@app.route('/tag', methods=['GET'])
@app.route('/tag/', methods=['GET'])
@app.route('/tag/<date>', methods=['GET'])
@app.route('/tag/<date>/', methods=['GET'])
@app.route('/tag/<date>/<tag>', methods=['GET'])
@app.route('/tag/<date>/<tag>/', methods=['GET'])
def tag(date = None, tag = None):
    try:
        event = {}
        event['query'] = request_handler.handle_query(date, tag, 'TAG')
        logging.info(event)
        print(event)
        return response.success(request_handler.query.get_tag(event))
    except Exception as e:
        print(traceback.format_exc())
        logging.error(str(traceback.format_exc()))
        return response.failure("Request failed. " + str(e))

@app.route('/topic', methods=['GET'])
@app.route('/topic/', methods=['GET'])
@app.route('/topic/<date>', methods=['GET'])
@app.route('/topic/<date>/', methods=['GET'])
@app.route('/topic/<date>/<sentiment>', methods=['GET'])
@app.route('/topic/<date>/<sentiment>/', methods=['GET'])
def sentiment(date = None, sentiment = None):
    try:
        event = {}
        event['query'] = request_handler.handle_query(date, sentiment, 'SENTIMENT')
        logging.info(event)
        print(event)
        return response.success(request_handler.query.get_category(event))
    except Exception as e:
        print(traceback.format_exc())
        logging.error(str(traceback.format_exc()))
        return response.failure("Request failed. " + str(e))

@app.route('/search/', methods=['GET'])
def search():
    try:
        event = {}
        event['query'] = request_handler.handle_search(request.query_string.decode("utf-8") )
        logging.info(event)
        print(event)
        return response.success(request_handler.query.get_search(event))
    except Exception as e:
        print(traceback.format_exc())
        logging.error(str(traceback.format_exc()))
        return response.failure("Request failed. " + str(e))

@app.route('/rating', methods=['POST'])
@app.route('/rating/', methods=['POST'])
def rating():
    return

@app.route('/interaction', methods=['POST'])
@app.route('/interaction/', methods=['POST'])
def interaction():
    return

@app.errorhandler(Exception)
def handle_error(e):
    print(traceback.format_exc())
    logging.error(str(traceback.format_exc()))
    return response.failure("Request failed")

if __name__ == "__main__":
    load_env(sys.argv[1])
    db = Query(app)
    request_handler = Handler(db)
    app.run(host='127.0.0.1', port=8000)