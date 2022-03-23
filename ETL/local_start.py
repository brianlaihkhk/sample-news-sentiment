from etl.etl import Etl, Aggregate
from process.sql_process import SqlProcess
import yaml
from config.argv import load_options
import sys
import os
import logging

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

class FileContext:
    def __init__(self, path, category):
        self.sqlProcess = SqlProcess(path, category)
        self.scanned = os.environ['SCANNED_FILE']
        self.start_folder = os.environ['SCAN_FOLDER']

    def start(self):
        for folder in [x[0] for x in os.walk(self.start_folder)] :
            self.process(folder , os.path.basename(folder))

    def process(self, path, category):
        file_list = list(set(self.get_file_list(path)) - set(self.get_scanned_file(self.scanned)))
        for context in file_list :
            context_list = [ Etl(context, self.sqlProcess.get_random_date(), self.get_context(context), category) ]
            aggregates = Aggregate(context_list)
            self.sqlProcess.process_news(context_list)
            self.sqlProcess.process_aggregate_category(aggregates.aggregate_category(context_list))
            self.sqlProcess.process_aggregate_sentiment(aggregates.aggregate_sentiment(context_list))
            self.sqlProcess.process_aggregate_topic(aggregates.aggregate_topic(context_list))
            self.sqlProcess.process_aggregate_tags(aggregates.aggregate_tags(context_list))
            self.save_scanned_file(self.scanned, [ context ])

    def get_context(self, path):
        lines = ['', '']
        with open(path) as f:
            try:
                lines = f.readlines()
            except Exception as exc:
                logging.error(str(exc))
                raise Exception('Unable to load file : ' + path)
        return lines

    def get_scanned_file(self, file):
        file_list = []
        with open(file) as f:
            try:
                file_list = yaml.safe_load(f)
                if file_list is None:
                    file_list = []
            except yaml.YAMLError as exc:
                logging.error(str(exc))
                raise Exception('Unable to open scanned list' + file)
        return file_list

    def save_scanned_file(self, file, context):
        if context != None and len(context) > 0 :
            try:
                file = open(file, 'a', buffering=1)
                yaml.dump(context, file, Dumper=NoAliasDumper)
                file.close()
            except Exception as exc:
                logging.error(str(exc))
                raise Exception('Unable to save scanned list' + file)
        else:
            return False
        return True

    def get_file_list(self, path):
        file_list = []
        for file in os.listdir(path):
            if file.endswith(".txt"):
                file_list.append(os.path.join(path, file))
        return file_list


if __name__ == "__main__":
    load_options(sys.argv[1:], 'file')
    FileContext().start()
