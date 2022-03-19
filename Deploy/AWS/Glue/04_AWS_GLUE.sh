#!/bin/bash
# please download the wheel files using
# python3 -m pip download --only-binary :all: --dest . -r requirements.txt
# and upload the wheels to S3

S3_BUCKET="s3://aws-glue-scripts-123456789012-us-east-1"
ETL_SCRIPT="${S3_BUCKET}/ETL/etl_glue.py"
WHEEL_LIST='[
"${S3_BUCKET}/ETL/whl/Flask-2.0.3-py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/Flask_SQLAlchemy-2.5.1-py2.py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/Jinja2-3.0.3-py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/MarkupSafe-2.1.1-cp39-cp39-macosx_10_9_x86_64.whl", 
"${S3_BUCKET}/ETL/whl/PyJWT-2.3.0-py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/PyMySQL-1.0.2-py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/PyYAML-5.4.1-cp39-cp39-macosx_10_9_x86_64.whl", 
"${S3_BUCKET}/ETL/whl/SQLAlchemy-1.4.32-cp39-cp39-macosx_10_15_x86_64.whl", 
"${S3_BUCKET}/ETL/whl/Werkzeug-2.0.3-py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/click-8.0.4-py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/greenlet-1.1.2-cp39-cp39-macosx_10_14_x86_64.whl", 
"${S3_BUCKET}/ETL/whl/itsdangerous-2.1.1-py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/joblib-1.1.0-py2.py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/nltk-3.7-py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/packaging-21.3-py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/psycopg2_binary-2.9.3-cp39-cp39-macosx_10_14_x86_64.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl", 
"${S3_BUCKET}/ETL/whl/pyparsing-3.0.7-py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/regex-2022.3.15-cp39-cp39-macosx_10_9_x86_64.whl", 
"${S3_BUCKET}/ETL/whl/sqlalchemy_redshift-0.8.9-py2.py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/textblob-0.17.1-py2.py3-none-any.whl", 
"${S3_BUCKET}/ETL/whl/tqdm-4.63.0-py2.py3-none-any.whl"
]'

aws glue create-job --name python-job-cli --role Role --command '{"Name" :  "pythonshell", "ScriptLocation" : "${ETL_SCRIPT}"}' --default-arguments '{"--extra-py-files" : ${WHEEL_LIST}}'
