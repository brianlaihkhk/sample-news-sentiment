from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import yaml
import sys
import traceback
import response
from misc import load_options
from flask import Flask, request
from flask_cors import CORS
from handler import Handler
from db import Database
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
        query = request_handler.handle_news(category, uuid)
        logging.info(query)
        print(query)
        return response.success(request_handler.query.get_news(query))
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
        query = request_handler.handle_query(date, topic, 'TOPIC')
        logging.info(query)
        print(query)
        return response.success(request_handler.query.get_topic(query))
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
        query = request_handler.handle_query(date, category, 'CATEGORY')
        logging.info(query)
        print(query)
        return response.success(request_handler.query.get_category(query))
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
        query = request_handler.handle_query(date, tag, 'TAG')
        logging.info(query)
        print(query)
        return response.success(request_handler.query.get_tag(query))
    except Exception as e:
        print(traceback.format_exc())
        logging.error(str(traceback.format_exc()))
        return response.failure("Request failed. " + str(e))

@app.route('/sentiment', methods=['GET'])
@app.route('/sentiment/', methods=['GET'])
@app.route('/sentiment/<date>', methods=['GET'])
@app.route('/sentiment/<date>/', methods=['GET'])
@app.route('/sentiment/<date>/<sentiment>', methods=['GET'])
@app.route('/sentiment/<date>/<sentiment>/', methods=['GET'])
def sentiment(date = None, sentiment = None):
    try:
        query = request_handler.handle_query(date, sentiment, 'SENTIMENT')
        logging.info(query)
        print(query)
        return response.success(request_handler.query.get_sentiment(query))
    except Exception as e:
        print(traceback.format_exc())
        logging.error(str(traceback.format_exc()))
        return response.failure("Request failed. " + str(e))

@app.route('/search', methods=['GET'])
@app.route('/search/', methods=['GET'])
def search():
    try:
        query = request_handler.handle_search(request.query_string.decode("utf-8") )
        logging.info(query)
        print(query)
        return response.success(request_handler.query.get_search(query))
    except Exception as e:
        print(traceback.format_exc())
        logging.error(str(traceback.format_exc()))
        return response.failure("Request failed. " + str(e))

@app.errorhandler(Exception)
def handle_error(e):
    print(traceback.format_exc())
    logging.error(str(traceback.format_exc()))
    return response.failure("Request failed")

if __name__ == "__main__":
    load_options(sys.argv[1:])
    db = Database(app).db
    request_handler = Handler(db)
    app.run(host=os.environ['SERVER_HOST'], port=int(os.environ['SERVER_PORT']))