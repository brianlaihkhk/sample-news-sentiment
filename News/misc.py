import os
import yaml
import logging

def convert(input):
    output = {}
    for i in range(0, len(input)):
        split = input[i].split("=")
        output = {**output, split[0]: split[1]}
    return output

def load_env (file):
    with open(file, "r") as stream:
        try:
            env = yaml.safe_load(stream)
            env = convert(env["web"]["environment"])
            os.environ['RDS_USERNAME'] = env['RDS_USERNAME']
            os.environ['RDS_PASSWORD'] = env['RDS_PASSWORD']
            os.environ['RDS_HOST'] = env['RDS_HOST']
            os.environ['RDS_DEFAULT_DB'] = env['RDS_DEFAULT_DB']
            os.environ['RDS_DB_TYPE'] = env['RDS_DB_TYPE']
            os.environ['APPLICATION_PREFIX'] = env['APPLICATION_PREFIX']
        except yaml.YAMLError as exc:
            print(exc)
            logging.error(str(exc))