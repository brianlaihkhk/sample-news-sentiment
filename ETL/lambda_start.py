from etl.etl import Etl, Aggregate
from process.sql_process import SqlProcess
import yaml
from config.argv import load_options
import sys
import os
import logging
import boto3
from smart_open import open

class BucketContext:
    def __init__(self):
        self.s3_session = boto3.Session(aws_access_key_id=os.environ['SCANNED_FILE'],
                                        aws_secret_access_key=os.environ['SCANNED_FILE'])
        self.s3_client = self.s3_session.client('s3')
        self.s3_resource = self.s3_session.resource('s3')
        self.s3_bucket = os.environ['S3_BUCKET']
        self.source_folder = os.environ['SOURCE_FOLDER']
        self.target_folder = os.environ['TARGET_FOLDER']

    def start(self):
        for category in self.get_file_list():
            print(str(category))
            self.process(self, 's3://' + self.s3_bucket + '/' + self.source_folder, category)

    def process(self, path, category):
        file_list = self.s3_client.objects.filter(Bucket=self.s3_bucket, Prefix=path)

        for context in file_list :
            context_list = [ Etl(context, self.sqlProcess.get_random_date(), self.get_context(context), category) ]
            aggregates = Aggregate(context_list)
            self.sqlProcess.process_news(context_list)
            self.sqlProcess.process_aggregate_category(aggregates.aggregate_category(context_list))
            self.sqlProcess.process_aggregate_sentiment(aggregates.aggregate_sentiment(context_list))
            self.sqlProcess.process_aggregate_topic(aggregates.aggregate_topic(context_list))
            self.sqlProcess.process_aggregate_tags(aggregates.aggregate_tags(context_list))
            self.move_scanned_file(self.scanned, [ context ])

    def get_context(self, path):
        lines = ['', '']
        with open(path, 'wb', transport_params={'client': self.s3_client}) as f:
            try:
                lines = f.readlines()
            except Exception as exc:
                logging.error(str(exc))
                raise Exception('Unable to load file : ' + path)
        return lines

    def get_context(self, path):
        lines = ['', '']
        with open(path, 'wb', transport_params={'client': self.s3_client}) as f:
            try:
                lines = f.readlines()
            except Exception as exc:
                logging.error(str(exc))
                raise Exception('Unable to load file : ' + path)
        return lines

    def move_scanned_file(self, file):
        copy_source = {
            'Bucket' : self.s3_bucket,
            'Key' : self.source_folder + file
        }
        self.s3_resource.meta.client.copy(copy_source, 's3://' + self.s3_bucket + '/', self.target_folder + file)
        return True

def handle(event, context):
    load_options(sys.argv[1:], 's3')
    BucketContext().start()