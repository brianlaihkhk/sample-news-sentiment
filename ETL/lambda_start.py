from etl.etl import Etl, Aggregate
from process.sql_process import SqlProcess
from config.argv import load_options
import sys
import os
import logging
import boto3
from smart_open import open

class BucketContext:
    def __init__(self):
        self.s3_session = boto3.Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                                        aws_secret_access_key=os.environ['AWS_SECRET'])
        self.s3_client = self.s3_session.client('s3')
        self.s3_resource = self.s3_session.resource('s3')
        self.s3_bucket_name = os.environ['S3_BUCKET']
        self.source_folder = os.environ['SOURCE_FOLDER']
        self.target_folder = os.environ['TARGET_FOLDER']

    def start(self):

        list_folder = self.s3_client.list_objects_v2(Bucket = self.s3_bucket_name, Prefix=self.source_folder, Delimiter='/')
        folders = [item['Prefix'] for item in list_folder['CommonPrefixes']]
        for sub_folder in folders:
            category = sub_folder.replace(self.source_folder,'').replace('/','')
            self.process(sub_folder, category)

    def process(self, path, category):
        process = SqlProcess(path, category)

        list_folder = self.s3_client.list_objects_v2(Bucket = self.s3_bucket_name, Prefix=path)
        file_list = [ item['Key'] for item in list_folder['Contents']]

        for context in file_list :
            context_list = [ Etl(context, process.get_random_date(), self.get_context(context), category) ]
            aggregates = Aggregate(context_list)
            process.process_news(context_list)
            process.process_aggregate_category(aggregates.aggregate_category(context_list))
            process.process_aggregate_sentiment(aggregates.aggregate_sentiment(context_list))
            process.process_aggregate_topic(aggregates.aggregate_topic(context_list))
            process.process_aggregate_tags(aggregates.aggregate_tags(context_list))
            self.move_scanned_file([ context ], category)
            logging.info('Processed : ' + context)
            print('Processed : ' + context)

    def get_context(self, path):
        s3_path = 's3://' + self.s3_bucket_name + '/' + path
        lines = ['', '']
        with open(s3_path, 'r', transport_params={'client': self.s3_client}) as f:
            try:
                lines = f.readlines()
            except Exception as exc:
                logging.error(str(exc))
                raise Exception('Unable to load file : ' + path)
        return lines

    def move_scanned_file(self, file_list, category):
        for file in file_list : 
            filename = os.path.basename(file)
            copy_source = {
                'Bucket' : self.s3_bucket_name,
                'Key' : file
            }
            self.s3_client.copy(copy_source, self.s3_bucket_name, self.target_folder + category + '/' + filename)
            self.s3_client.delete_object(Bucket = self.s3_bucket_name, Key = file)

        return True

def handle(event, context):
    load_options(sys.argv[1:], 's3')
    BucketContext().start()

if __name__ == "__main__":
    load_options(sys.argv[1:], 's3')
    BucketContext().start()
