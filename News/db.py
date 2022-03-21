from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import jwt
import os

class Database:
    def __init__(self, app):
        print(os.environ['RDS_USERNAME'])
        # Obtain encrypt key
        encrypt_key = str(os.environ['RDS_ENCRYPT_KEY']).encode() if 'RDS_ENCRYPT_KEY' in os.environ else None
        env_username = os.environ['RDS_USERNAME']
        env_password = os.environ['RDS_PASSWORD']

        # MySql datebase
        db_url = os.environ['RDS_HOST']
        db_username = jwt.decode(env_username, encrypt_key, algorithms=["HS256"])["body"] if encrypt_key is not None else env_username
        db_password = jwt.decode(env_password, encrypt_key, algorithms=["HS256"])["body"] if encrypt_key is not None else env_password
        db_target = os.environ['RDS_DEFAULT_DB']

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        if (os.environ['RDS_DB_TYPE'].upper() == "MYSQL"):
            app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + db_username + ":" + db_password + "@" + db_url + "/" + db_target + "?charset=utf8"
        elif (os.environ['RDS_DB_TYPE'].upper() == "REDSHIFT"):
            app.config['SQLALCHEMY_DATABASE_URI'] = "redshift+psycopg2://" + db_username + ":" + db_password + "@" + db_url + "/" + db_target
        else:
            raise Exception("Missing RDS_DB_TYPE, only MYSQL or REDSHIFT is allowed")

        self.db = SQLAlchemy(app)