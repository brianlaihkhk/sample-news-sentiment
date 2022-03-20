from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import yaml
import sys
import traceback
import response
from query import Query
from misc import load_env

class LocalServerRouter(BaseHTTPRequestHandler):

    def do_GET(self):
        return_response = response.failure("Error or unsupported operations")
        event = {"headers" : self.headers}
        query = Query()

        try:
            if self.path.startswith('/news'):
                event['query'] = self.handle_news(self.path)
                print(event)
                return_response = response.success(query.get_news(event))
                self.send_response(200)
            elif self.path.startswith('/category'):
                event['query'] = self.handle_query(self.path, 'CATEGORY')
                return_response = response.success(query.get_category(event))
                self.send_response(200)
            elif self.path.startswith('/topic'):
                event['query'] = self.handle_query(self.path, 'TOPIC')
                return_response = response.success(query.get_topic(event))
                self.send_response(200)
            elif self.path.startswith('/sentiment'):
                event['query'] = self.handle_query(self.path, 'SENTIMENT')
                return_response = response.success(query.get_sentiment(event))
                self.send_response(200)
            elif self.path.startswith('/tag'):
                event['query'] = self.handle_query(self.path, 'TAG')
                return_response = response.success(query.get_tag(event))
                self.send_response(200)
            else :
                self.send_response(500)
        except Exception:
            traceback.print_exc()       
            self.send_response(500)

        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Credentials', True)
        self.end_headers()
        self.wfile.write(return_response["body"].encode())
        
    def do_POST(self):
        return_response = response.failure("Error or unsupported operations")
        event = {"headers" : self.headers}
        context = {}
        try:
            if self.path.startswith('/interaction'):
                self.send_response(200)
            else :
                self.send_response(500)
        except Exception:
            traceback.print_exc()       
            self.send_response(500)

        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Credentials', True)
        self.end_headers()
        self.wfile.write(return_response["body"].encode())

    def do_OPTIONS(self):
        return_response = response.success("Success")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Credentials', True)
        self.send_header('Access-Control-Allow-Methods', 'GET,POST')
        self.send_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Session, Authorization')
        self.end_headers()
        self.wfile.write(return_response["body"].encode())

    def handle_date(self, day_string):
        filter = {}

        week_data = day_string.split('-')

        if len(week_data) == 4 and str(week_data[0]):
            filter['WEEK_DAY'] = week_data[0]

        if len(week_data) == 4 and str(week_data[3]) and str(week_data[2]) and str(week_data[1]):
            filter['DATE'] = str(week_data[1]) + str(week_data[2]) + str(week_data[3])
            filter['YEAR'] = str(week_data[1])
            filter['MONTH'] = str(week_data[2])
            filter['DAY'] = str(week_data[3])
        elif len(week_data) == 4 and str(week_data[2]) and str(week_data[1]):
            filter['DATE'] = str(week_data[1]) + str(week_data[2]) + "%"
            filter['YEAR'] = str(week_data[1])
            filter['MONTH'] = str(week_data[2])
        elif len(week_data) == 4 and str(week_data[1]):
            filter['DATE'] = str(week_data[1]) + "%"
            filter['YEAR'] = str(week_data[1])
        elif len(week_data) == 4 and not str(week_data[3]) and not str(week_data[2]) and not str(week_data[1]) :
            filter['DATE'] = "%"
        else :
            raise Exception('Unsupported date query format')

        return filter

    def handle_query(self, path, key):
        path_data = path.split('/')[1:]
        if len(path_data) >= 3:
            query = {key : path_data[2] if path_data[2] else '%' }
            query.update(self.handle_date(path_data[1]))
            print(query)
            return query 
        elif len(path_data) >= 2:
            query = {key : '%'}
            query.update(self.handle_date(path_data[1]))
            return query 
        else :
            raise Exception('Unsupported path query format')

    def handle_news(self, path):
        path_data = path.split('/')[1:]
        print(str(path_data))
        if len(path_data) >= 3 and path_data[1] and path_data[2]:
            query = {'CATEGORY' : path_data[1], 'NEWS_UUID' : path_data[2]}
            return query 
        elif len(path_data) >= 2 and path_data[1]:
            query = {'CATEGORY' : path_data[1]}
            return query
        return {}

if __name__ == "__main__":
    load_env(sys.argv[1])
    httpd = HTTPServer(('localhost', 8081), LocalServerRouter)
    httpd.serve_forever()