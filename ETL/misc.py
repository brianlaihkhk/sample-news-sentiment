import os
import configparser
import logging
import getopt

def load_options (argv):
   try:
      opts, _ = getopt.getopt(argv,"e:", ["env-file=", "env_file="])
      for opt, arg in opts:
         if opt in ['-e', '--env-file', '--env_file']:
               load_env(arg)
   except getopt.GetoptError as e:
      pass

   if not ('RDS_USERNAME' in os.environ):
        raise Exception("No environment variable of application config is detected, make sure the file (using --env-file=<file> or -e <file>) or pre-set in environment variables (docker run --env-file=<file> <docker-id>).")

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
         os.environ['SCANNED_FILE'] = parser.get('config', 'SCANNED_FILE')
      except Exception as exc:
         print(exc)
         logging.error(str(exc))