#!/bin/sh
rm -rf build/
mkdir build/
chmod 777 build/

cp -rf serverless/ build/
cp -rf ../../News/ build/

pip3 install -I -t build/ -r ../requirements.txt

cd build/
npm install serverless@1.73.1
npm install serverless-python-requirements
npm install serverless-prune-plugin
npm install serverless-scriptable-plugin

if [[ $(type -a mysql) =~ "not found" ]]; then
    brew install mysql
fi
if [[ $(type -a openssl) =~ "not found" ]]; then
    brew install openssl
fi
LDFLAGS=-L/usr/local/opt/openssl/lib pip3 install mysqlclient

case "$2" in
    -g|--group)
        if [[ $3 -eq "all" ]]
        then
            serverless deploy function --function etl
        elif [[ $3 -eq "etl" ]]
        then
            serverless deploy function --function etl
        else
            serverless $1 $2 $3 $4 $5 
        fi
        ;;
    *)
        serverless $1 $2 $3 $4 $5

        ;;
  esac

rm -rf build/
