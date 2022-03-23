import os
import configparser
import logging
import getopt

def load_options (argv, type):
   try:
      opts, _ = getopt.getopt(argv,"e:", ["env-file=", "env_file="])
      for opt, arg in opts:
         if (opt in ['-e', '--env-file', '--env_file'] and type == "file"):
            load_env(arg)
         elif (opt in ['-e', '--env-file', '--env_file'] and type == "s3"):
            load_s3(arg)

   except getopt.GetoptError as e:
      pass

def load_env (file):
   with open(file, "r") as stream:
      try:
         parser = configparser.RawConfigParser()
         parser.read(file)
         os.environ['RDS_USERNAME'] = parser.get('config', 'RDS_USERNAME')
         os.environ['RDS_PASSWORD'] = parser.get('config', 'RDS_PASSWORD')
         os.environ['RDS_HOST'] = parser.get('config', 'RDS_HOST')
         os.environ['RDS_DEFAULT_DB'] = parser.get('config', 'RDS_DEFAULT_DB')
         os.environ['RDS_DB_TYPE'] = parser.get('config', 'RDS_DB_TYPE')
         os.environ['SCANNED_FILE'] = parser.get('file', 'SCANNED_FILE')
         os.environ['SCAN_FOLDER'] = parser.get('file', 'SCAN_FOLDER')

      except Exception as exc:
         print(exc)
         logging.error(str(exc))

   if not ('SCANNED_FILE' in os.environ):
        raise Exception("No environment variable of application config is detected, make sure the file (using --env-file=<file> or -e <file>) or pre-set in environment variables (docker run --env-file=<file> <docker-id>).")


def load_s3 (file):
   with open(file, "r") as stream:
      try:
         parser = configparser.RawConfigParser()
         parser.read(file)
         os.environ['RDS_USERNAME'] = parser.get('config', 'RDS_USERNAME')
         os.environ['RDS_PASSWORD'] = parser.get('config', 'RDS_PASSWORD')
         os.environ['RDS_HOST'] = parser.get('config', 'RDS_HOST')
         os.environ['RDS_DEFAULT_DB'] = parser.get('config', 'RDS_DEFAULT_DB')
         os.environ['RDS_DB_TYPE'] = parser.get('config', 'RDS_DB_TYPE')
         os.environ['AWS_ACCESS_KEY'] = parser.get('s3', 'AWS_ACCESS_KEY')
         os.environ['AWS_SECRET'] = parser.get('s3', 'AWS_SECRET')
         os.environ['S3_BUCKET'] = parser.get('s3', 'S3_BUCKET')
         os.environ['SOURCE_FOLDER'] = parser.get('s3', 'SOURCE_FOLDER')
         os.environ['TARGET_FOLDER'] = parser.get('s3', 'TARGET_FOLDER')

      except Exception as exc:
         print(exc)
         logging.error(str(exc))

   if not ('S3_BUCKET' in os.environ):
        raise Exception("No environment variable of application config is detected, make sure the file (using --env-file=<file> or -e <file>) or pre-set in environment variables (docker run --env-file=<file> <docker-id>).")
